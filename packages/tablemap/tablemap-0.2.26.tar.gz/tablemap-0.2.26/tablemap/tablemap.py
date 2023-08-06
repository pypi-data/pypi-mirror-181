"""A data wrangling tool which requires no knowledge of Pandas or SQL.
"""

import os
import signal
import sqlite3
import tempfile
from collections import deque
from contextlib import contextmanager
from copy import copy
from itertools import (chain, dropwhile, groupby, islice, product, takewhile,
                       zip_longest)
from pathlib import Path, PurePath


class Conn:
    """Connection to a SQL database file.

    Example:
        conn = Conn('sample.db')
    """

    def __init__(self, dbfile):
        # dbfile must be a filename(str), can't be :memory:
        if PurePath(dbfile).is_absolute():
            self._dbfile = dbfile
        else:
            self._dbfile = os.path.join(os.getcwd(), dbfile)

        self._dbconn = None

    def __getitem__(self, tname):
        return Rows((self, tname))

    def __setitem__(self, tname, val):
        with _connect(self._dbfile) as dbconn:
            self._dbconn = dbconn
            _delete(dbconn, tname)
            _insert(dbconn, tname, _rows2iter(val))


# TODO: Not sure whether to check the syntax for each method.
# for example, `fold` must be preceded by grouping methods (by, windowed, group)
class Rows:
    """Contains a table source (database connection or list of dicts) and
    builds instructions as methods growing in chained

    Rows object can be instantiated in two ways.
        1. to pass a table name to Conn.__getitem__, for example,
            conn['table_name']
        2. Directly pass a list of dicts or dicts yielding iterator to Rows
            Rows([d1, d2, ...])
    """

    def __init__(self, src):
        if isinstance(src, tuple):
            conn, tname = src

            self._src = src
            self._history = [{
                'cmd': 'fetch',
                'conn': conn,
                'tname': tname,
                'genfn': _build_initgen(conn, tname, [])

            }]

        else:
            self._src = list(src)

            def gen():
                yield from self._src

            self._history = [{
                'cmd': 'read',
                'genfn': gen
            }]

    def __str__(self):
        return "\n".join(str(r) for r in self._iter())

    def __getitem__(self, key):
        if isinstance(key, str):
            return [r[key] for r in self._iter()]
        if isinstance(key, slice):
            return self._islice(key.start, key.stop, key.step)
        raise ValueError("Must pass a str(column name) or a slice")

    def zip(self, other):
        """Attach two Rows side by side until either one is depleted

        Args:
            other (Rows or list of dicts or dicts yielding iterator)

        Returns:
            Rows
        """
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen1():
            for row1, row2 in zip(pgen(), _rows2iter(other)):
                yield {**row1, **row2}

        # if the source is the database, it's safe to update rows directly
        # because tablemap creates new rows every time you iterate rows
        def gen2():
            for row1, row2 in zip(pgen(), _rows2iter(other)):
                row1.update(row2)
                yield row1

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'zip',
            'genfn': gen2 if self._history[0]['cmd'] == 'fetch' else gen1
        }]

        return newself

    def zip_longest(self, other):
        """Attach two Rows side by side as long as any of them remained

        Empty columns (with values of '') generated

        Args:
            other (Rows or list of dicts or dicts yielding iterator)

        Returns:
            Rows
        """

        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen1():
            row1, rows1 = _spy(pgen())
            row2, rows2 = _spy(_rows2iter(other))
            empty1 = {field: '' for field in row1.keys()}
            empty2 = {field: '' for field in row2.keys()}

            for row1, row2 in zip_longest(rows1, rows2):
                if row1 and row2:
                    yield {**row1, **row2}
                elif row1 and not row2:
                    yield {**row1, **empty2}
                elif not row1 and row2:
                    yield {**empty1, **row2}

        def gen2():
            row1, rows1 = _spy(pgen())
            row2, rows2 = _spy(_rows2iter(other))
            # using the same object over and over is SAFE
            empty1 = {field: '' for field in row1.keys()}
            empty2 = {field: '' for field in row2.keys()}

            for row1, row2 in zip_longest(rows1, rows2):
                if row1 and row2:
                    row1.update(row2)
                    yield row1
                elif row1 and not row2:
                    row1.update(empty2)
                    yield row1
                elif not row1 and row2:
                    empty1.update(row2)
                    yield empty1

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'zip_longest',
            'genfn': gen2 if self._history[0]['cmd'] == 'fetch' else gen1
        }]
        return newself

    def chain(self, other):
        """Concatenate Rows to the other

        Args:
            other (Rows or list of dicts or dicts yielding iterator)

        Returns:
            Rows
        """
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen():
            for row in pgen():
                yield row
            for row in _rows2iter(other):
                yield row

        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'chain',
            'genfn': gen
        }]
        return newself

    # each column may contain asc or desc
    # ex) 'col1 desc', 'col2 asc'
    def order(self, *fields_maybe_with_desc):
        """Sort according to columns

        Args:
            *cols (str): column names

        Returns:
            Rows object
        """
        newself = copy(self)

        # pylint: disable=protected-access
        if len(newself._history) == 1\
                and newself._history[-1]['cmd'] == 'fetch':
            # pylint: disable=protected-access
            prehist = newself._history[-1]
            # pylint: disable=protected-access
            newself._history = [{
                **prehist,
                'genfn': _build_initgen(prehist['conn'], prehist['tname'],
                                        fields_maybe_with_desc)
            }]
            return newself

        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen_from_sql():
            try:
                tmpdbfd, tmpdb = tempfile.mkstemp()
                with _connect(tmpdb) as dbconn:
                    temp_table_name = "temp"
                    _insert(dbconn, temp_table_name, pgen())
                    yield from _fetch(dbconn, temp_table_name,
                                      fields_maybe_with_desc)

            # TODO: possible errors must be dealt with.
            finally:
                # must close the file descriptor to delete it
                os.close(tmpdbfd)
                if Path(tmpdb).is_file():
                    os.remove(tmpdb)

        def gen_simp():
            list_of_dicts = list(pgen())
            # multiple column sorting needs an idea.
            for field_mwd in reversed(fields_maybe_with_desc):
                reverse_flag = False
                field_mwd_tuple = field_mwd.split()
                if len(field_mwd_tuple) == 2:
                    field, desc = field_mwd_tuple
                    if desc.lower() == 'desc':
                        reverse_flag = True
                else:
                    field = field_mwd_tuple[0]
                # pylint: disable=cell-var-from-loop
                list_of_dicts\
                    .sort(key=lambda row: row[field], reverse=reverse_flag)
            yield from list_of_dicts

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'order',
            'cols': fields_maybe_with_desc,
            'genfn': gen_from_sql if newself._history[0]['cmd'] == 'fetch'
            else gen_simp
        }]

        return newself

    # End-users might not be able to pass proper functions.
    def _apply(self, func):
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen_single():
            for row in pgen():
                yield from func(row)

        def gen_group():
            for key, rows in pgen():
                yield from func(key, rows)

        def gen_windowed():
            for rows in pgen():
                yield from func(rows)

        genfn = None
        # pylint: disable=protected-access
        if newself._history[-1]['cmd'] == 'group':
            genfn = gen_group
        # pylint: disable=protected-access
        elif newself._history[-1]['cmd'] == 'windowed':
            genfn = gen_windowed
        else:
            genfn = gen_single

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': '_apply',
            'genfn': genfn
        }]
        return newself

    def group(self, *fields):
        """Group consecutive rows with the same values for given fields

        Args:
            *fields (list of str)

        Returns:
            Rows
        """
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen():
            yield from groupby(pgen(), _keyfn(fields))

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'group',
            'cols': fields,
            'genfn': gen
        }]

        return newself

    # TODO: not sure 'join' can completely replace this one.
    def _merge(self, func, other):
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen():
            yield from _step(func, pgen(), _rows2iter(other))

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': '_merge',
            'genfn': gen
        }]

        return newself

    def map(self, func):
        """Applies func to each row or Rows (when grouped)

        Args:
            func: args: row(dict) when not grouped or
                        Rows when grouped
                             (preceded by 'by', 'windowed', 'group')
                  returns: row (dict) or
                           Rows or
                           None

        Returns:
            Rows
        """
        if self._history[-1]['cmd'] == 'group':
            def _fn2gen(func):
                def gen(_key, rows):
                    val = func(Rows(rows))
                    if isinstance(val, dict):
                        yield val
                    elif isinstance(val, Rows):
                        # pylint: disable=protected-access
                        yield from val._iter()
                return gen
            return self._apply(_fn2gen(func))

        if self._history[-1]['cmd'] == 'windowed':
            def _fn2gen1(func):
                def gen(rows):
                    val = func(Rows(rows))
                    if isinstance(val, dict):
                        yield val
                    elif isinstance(val, Rows):
                        # pylint: disable=protected-access
                        yield from val._iter()
                return gen

            return self._apply(_fn2gen1(func))

        # single row
        def _fn2gen_single(func):
            def gen(row):
                val = func(row)
                if isinstance(val, dict):
                    yield val
                elif isinstance(val, Rows):
                    # pylint: disable=protected-access
                    yield from val._iter()
            return gen
        return self._apply(_fn2gen_single(func))

    # pylint: disable=invalid-name
    def by(self, *fields_maybe_with_desc):
        """Group rows with fields

        order columns first and then group

        Args:
            *fields_maybe_with_desc: "col1" or "col1 desc"

        Returns:
            Rows
        """
        # need to cut out 'desc', 'asc'
        grouping_fields = [field.split()[0]
                           for field in fields_maybe_with_desc]
        return self.order(*fields_maybe_with_desc).group(*grouping_fields)

    def filter(self, pred):
        """Filter rows that the predicate function returns True

        Args:
            pred: function that takes a row(dict) as arg and returns True/False

        Returns:
            Rows
        """
        def gen(row):
            if pred(row):
                yield row

        return self._apply(gen)

    def update(self, **kwargs):
        """Updates each row with new ones

        Does not mutate rows. Creates new rows.
        kwargs are applied one by one. The next key value pair uses the
        previously updated row

        Args:
            **kwargs: key = new field name
                      value = 1. function
                                    args: row(dict)
                                    returns: str or number
                              2. str or number

        Returns:
            Rows

        """

        def updatefn1(row):
            newrow = row.copy()
            for field, val in kwargs.items():
                newrow[field] = val(newrow) if callable(val) else val
            yield newrow

        # row mutating version
        def updatefn2(row):
            for field, val in kwargs.items():
                row[field] = val(row) if callable(val) else val
            yield row

        if self._history[0]['cmd'] == 'fetch':
            return self._apply(updatefn2)
        return self._apply(updatefn1)

    # pretty expensive for what it actually does
    # but this version does not depend on the order of rows.
    def rename(self, **kwargs):
        """Rename fields with new ones

        Args:
            **kwargs: key = new field name
                      value = old field name (str)

        Returns:
            Rows
        """
        kwargs_rev = {oldkey: newkey for newkey, oldkey in kwargs.items()}

        def renamefn(row):
            yield {kwargs_rev.get(oldkey, oldkey): val
                   for oldkey, val in row.items()}

        return self._apply(renamefn)

    def fold(self, **kwargs):
        """n rows to 1 row

        fold must be preceded by grouping methods (group, by, windowed) and
        each group is shrunken to 1

        Args:
            **kwargs: key = new field name
                      value = 1. function
                                    args: Rows
                                    returns: str or number
                              2. str or number
        Returns:
            Rows
        """
        # fold must be preceded by `by`
        grouping_fields = []
        if self._history[-1]['cmd'] == 'group':
            grouping_fields = self._history[-1]['cols']

        # TODO: not sure whether to check if func returns a proper value
        # (a str or a number)
        def foldfn1(rows):
            rows = Rows(rows)
            row = {}
            for newfield, val in kwargs.items():
                row[newfield] = val(rows) if callable(val) else val
            yield row

        def foldfn2(keys, rows):
            # keys: values for grouping fields (itertools.groupby)
            rows = Rows(rows)
            row = dict(zip(grouping_fields, keys))
            for newfield, val in kwargs.items():
                row[newfield] = val(rows) if callable(val) else val
            yield row

        if self._history[-1]['cmd'] == 'windowed':
            return self._apply(foldfn1)
        if self._history[-1]['cmd'] == 'group':
            return self._apply(foldfn2)
        raise ValueError("fold must be preceded by grouping processes")

    def select(self, *fields):
        """select fields discarding others

        Args:
            *fields(list of str): field names to select

        Returns:
            Rows
        """
        def selectfn(row):
            yield {field: row[field] for field in fields}

        return self._apply(selectfn)

    def deselect(self, *fields):
        """Deselect fields

        Args:
            *fields(list of str): field names to deselect

        Returns:
            Rows
        """
        fields_set = set(fields)

        def deselectfn(row):
            yield {field: val for field, val in row.items()
                   if field not in fields_set}

        return self._apply(deselectfn)

    def join(self, other, join_type="left"):
        """Joins two Rows in SQL style

        Args:
            Other: Rows or a list of rows(dicts) or row(dict) yielding iterator
            join_type: one of 'inner', 'left', 'right', 'full',
                each representing SQL style join types. 'left' is the default

        Returns:
            Rows
        """
        if join_type.lower() == "inner":
            return self._inner_join(other)
        if join_type.lower() == "left":
            return self._left_join(other)
        if join_type.lower() == "right":
            return self._right_join(other)
        if join_type.lower() == "full":
            return self._full_join(other)
        raise ValueError("Unknown join_type", join_type)

    def _inner_join(self, other):
        def innerjoin_fn1(rows1, rows2, _left, _right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    row1.update(row2)
                    yield row1

        def innerjoin_fn2(rows1, rows2, _left, _right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    yield {**row1, **row2}

        if self._history[0]['cmd'] == 'fetch':
            return self._merge(innerjoin_fn1, other)
        return self._merge(innerjoin_fn2, other)

    def _left_join(self, other):
        def leftjoin_fn1(rows1, rows2, _left, right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    row1.update(row2)
                    yield row1

            elif rows1 != [] and rows2 == []:
                for row1 in rows1:
                    row1.update((field, '') for field in right_only)
                    yield row1

        def leftjoin_fn2(rows1, rows2, _left, right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    yield {**row1, **row2}

            elif rows1 != [] and rows2 == []:
                for row1 in rows1:
                    yield {**row1, **{field: '' for field in right_only}}

        if self._history[0]['cmd'] == 'fetch':
            return self._merge(leftjoin_fn1, other)
        return self._merge(leftjoin_fn2, other)

    def _right_join(self, other):
        def rightjoin_fn1(rows1, rows2, left, _right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    row1.update(row2)
                    yield row1

            elif rows1 == [] and rows2 != []:
                empty_left = {field: '' for field in left}
                for row2 in rows2:
                    empty_left.update(row2)
                    yield empty_left

        def rightjoin_fn2(rows1, rows2, left, _right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    yield {**row1, **row2}

            elif rows1 == [] and rows2 != []:
                for row2 in rows2:
                    yield {**{field: '' for field in left}, **row2}

        if self._history[0]['cmd'] == 'fetch':
            return self._merge(rightjoin_fn1, other)
        return self._merge(rightjoin_fn2, other)

    def _full_join(self, other):
        def fulljoin_fn1(rows1, rows2, left, right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    # TODO: updating on the same object multiple times.
                    # Still works, why ?!!,
                    # yielding and returning a appended list is different.
                    # later modifications do not affect previous yielded object
                    # So anyway, these updates in all joining methods
                    # are perfectly safe.
                    row1.update(row2)
                    yield row1

            elif rows1 != [] and rows2 == []:
                for row1 in rows1:
                    row1.update((field, '') for field in right_only)
                    yield row1

            elif rows1 == [] and rows2 != []:
                empty_left = {field: '' for field in left}
                for row2 in rows2:
                    empty_left.update(row2)
                    yield empty_left

        def fulljoin_fn2(rows1, rows2, left, right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    yield {**row1, **row2}

            elif rows1 != [] and rows2 == []:
                for row1 in rows1:
                    yield {**row1, **{field: '' for field in right_only}}

            elif rows1 == [] and rows2 != []:
                for row2 in rows2:
                    yield {**{field: '' for field in left}, **row2}

        if self._history[0]['cmd'] == 'fetch':
            return self._merge(fulljoin_fn1, other)
        return self._merge(fulljoin_fn2, other)

    def distinct(self, *fields):
        """Returns a Rows with only the first row in each group.

        Order and group with fields drop all the others except for the first
        in each group (remove duplicates)

        Args:
            *fields (list of str):

        Returns:
            Rows
        """
        def distinctfn(_k, rows):
            # impossible to raise stop iteration here
            # pylint: disable=stop-iteration-return
            yield next(rows)

        # pylint: disable=protected-access
        return self.by(*fields)._apply(distinctfn)

    def windowed(self, chunk_size, step=1):
        """Returns a Rows of a sliding window(rows) with chunk_size skipping
        every step size rows

        Args:
            chunk_size (int)
            step (int):  1 is the default

        Returns:
            Rows
        """
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen():
            yield from _windowed(pgen(), chunk_size, step)

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'windowed',
            'n': chunk_size,
            'step': step,
            'genfn': gen
        }]
        return newself

    def _islice(self, *args):
        newself = copy(self)
        pgen = self._history[-1]['genfn']

        def gen():
            yield from islice(pgen(), *args)

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': '_islice',
            'args': args,
            'genfn': gen
        }]
        return newself

    def takewhile(self, pred):
        """Returns a Rows that would generate rows(dicts) as long as the pred
        is true

        Args:
            pred: predicate func that takes a row(dict) as an argument

        Returns:
            Rows
        """
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen():
            yield from takewhile(pred, pgen())

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'takewhile',
            'genfn': gen
        }]
        return newself

    def dropwhile(self, pred):
        """Returns a Rows that would drop rows as long as the pred
        is true

        Args:
            pred: predicate func that takes a row(dict) as an argument

        Returns:
            Rows
        """

        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen():
            yield from dropwhile(pred, pgen())

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'dropwhile',
            'genfn': gen
        }]
        return newself

    def size(self):
        "Returns the number(size) of rows"
        # There are rooms for this to be more efficient because some of the
        # methods do not affect the size of the Rows but
        # don't think it's worth the trouble.
        if len(self._history) == 1 and self._history[0]['cmd'] == 'fetch':
            origin = self._history[0]
            return _get_size(origin['conn'], origin['tname'])
        if len(self._history) == 1 and self._history[0]['cmd'] == 'read':
            return len(self._src)
        return sum(1 for _ in self._iter())

    # iter is not safe to end-users, because the generator might not be
    # terminated after the database connection is closed.
    # This should be used in a controlled manner.
    def _iter(self):
        yield from self._history[-1]['genfn']()

    # list is safe, because it completes the iteration.
    def list(self):
        "Returns a list of rows(dicts)"
        # pylint: disable=protected-access
        return list(self._iter())


def _insert_statement(table_name, row):
    """insert into foo values (:a, :b, :c, ...)

    Notice the colons.
    """
    key_fields = ', '.join(":" + field.strip() for field in row)
    return f"insert into {table_name} values ({key_fields})"


def _create_statement(table_name, fields):
    """Create table if not exists foo (...)

    Note:
        Every type is numeric.
    """
    schema = ', '.join([field + ' ' + 'numeric' for field in fields])
    return f"create table if not exists {table_name} ({schema})"


def _dict_factory(cursor, row):
    return {col[0]: val for col, val in zip(cursor.description, row)}


def _keyfn(fields):
    if len(fields) == 1:
        field = fields[0]
        return lambda r: r[field]
    return lambda r: [r[field] for field in fields]


def _delete(dbconn, table_name):
    dbconn.cursor().execute(f'drop table if exists {table_name}')


def _insert(dbconn, table_name, rows):
    irows = iter(rows)
    try:
        first_row = next(irows)
    except StopIteration:
        raise ValueError(f"No row to insert in {table_name}") from None
    else:
        fields = list(first_row)

        dbconn.cursor().execute(_create_statement(table_name, fields))
        istmt = _insert_statement(table_name, first_row)
        dbconn.cursor().executemany(istmt, chain([first_row], rows))


def _fetch(dbconn, table_name, fields):
    if fields:
        query = f"select * from {table_name} order by {','.join(fields)}"
    else:
        query = f"select * from {table_name}"

    yield from dbconn.cursor().execute(query)


def _spy(iterator):
    val = next(iterator)
    return val, chain([val], iterator)


def _step(func, key_rows1, key_rows2):
    empty = object()
    try:
        key1, rows1 = next(key_rows1)
        key2, rows2 = next(key_rows2)

        row1, rows1 = _spy(rows1)
        row2, rows2 = _spy(rows2)

        # all of left fields
        left = list(row1)
        right_only = [field for field in list(row2) if field not in list(row1)]

        while True:
            if key1 == key2:
                yield from func(rows1, rows2, left, right_only)
                key1 = key2 = empty
                key1, rows1 = next(key_rows1)
                key2, rows2 = next(key_rows2)
            elif key1 < key2:
                yield from func(rows1, [], left, right_only)
                key1 = empty
                key1, rows1 = next(key_rows1)
            else:
                yield from func([], rows2, left, right_only)
                key2 = empty
                key2, rows2 = next(key_rows2)

    except StopIteration:
        # unconsumed
        if key1 is not empty:
            yield from func(rows1, [], left, right_only)
        if key2 is not empty:
            yield from func([], rows2, left, right_only)

        for _, rows1 in key_rows1:
            yield from func(rows1, [], left, right_only)
        for _, rows2 in key_rows2:
            yield from func([], rows2, left, right_only)


def _rows2iter(obj):
    # pylint: disable=protected-access
    return obj._iter() if isinstance(obj, Rows) else iter(obj)


def _build_initgen(conn, table_name, fields):
    def initgen():
        try:
            # pylint: disable=protected-access
            yield from _fetch(conn._dbconn, table_name, fields)
        # in case conn._dbconn is either None or closed connection
        except (AttributeError, sqlite3.ProgrammingError):
            # pylint: disable=protected-access
            with _connect(conn._dbfile) as dbconn:
                conn._dbconn = dbconn
                yield from _fetch(dbconn, table_name, fields)
    return initgen


def _get_size(conn, table_name):
    try:
        # pylint: disable=protected-access
        res = conn._dbconn.cursor()\
            .execute(f"select count(1) from {table_name}")
        return res.fetchone()['count(1)']
    except (AttributeError, sqlite3.ProgrammingError):
        # pylint: disable=protected-access
        with _connect(conn._dbfile) as dbconn:
            res = dbconn.cursor().execute(f"select count(1) from {table_name}")
            return res.fetchone()['count(1)']


def _windowed(seq, chunk_size, step):
    if chunk_size < 0:
        raise ValueError('n must be >= 0')
    if chunk_size == 0:
        yield []
        return
    if step < 1:
        raise ValueError('step must be >= 1')

    window = deque(maxlen=chunk_size)
    i = chunk_size
    for _ in map(window.append, seq):
        i -= 1
        if not i:
            i = step
            yield list(window)

    size = len(window)
    if size == 0:
        return
    if size < chunk_size:
        yield list(window)
    elif 0 < i < min(step, chunk_size):
        yield list(window)[i:]


@contextmanager
def _connect(dbfile):
    dbconn = sqlite3.connect(dbfile)
    dbconn.row_factory = _dict_factory
    try:
        yield dbconn
    finally:
        # If users enter ctrl-c during the database commit,
        # db might be corrupted. (won't work anymore)
        with _delayed_keyboard_interrupts():
            dbconn.commit()
            dbconn.close()


@contextmanager
def _delayed_keyboard_interrupts():
    signal_received = []

    def handler(sig, frame):
        nonlocal signal_received
        signal_received = (sig, frame)
    # Do nothing but recording something has happened.
    old_handler = signal.signal(signal.SIGINT, handler)

    try:
        yield
    finally:
        # signal handler back to the original one.
        signal.signal(signal.SIGINT, old_handler)
        if signal_received:
            # do the delayed work
            old_handler(*signal_received)
