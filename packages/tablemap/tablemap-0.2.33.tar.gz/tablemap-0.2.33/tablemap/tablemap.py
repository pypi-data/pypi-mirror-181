"""A data wrangling tool which requires no knowledge of Pandas or SQL.

*** Type definitions ***

RowVal = str | int | float
Row = dict[str, RowVal]
    Row represents a row in a table, str is a column name (field)
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

    Examples

    >>> conn = Conn('sample.db')
    """

    def __init__(self, dbfile):
        # dbfile must be a filename(str), can't be :memory:
        if PurePath(dbfile).is_absolute():
            self._dbfile = dbfile
        else:
            self._dbfile = os.path.join(os.getcwd(), dbfile)

        self._dbconn = None

    def __getitem__(self, table_name):
        """Returns a Rows object to fetch a table from the database

        Parameters
        ----------
        table_name: str

        Returns
        -------
        Rows
        """
        return Rows((self, table_name))

    def __setitem__(self, table_name, val):
        """Insert the table content to the database

        Parameters
        ----------
        table_name: str

        val: Rows | list[Row] | Iterable[Row]
            where Row = dict[str, str | int | float]
        """

        with _connect(self._dbfile) as dbconn:
            self._dbconn = dbconn
            _delete(dbconn, table_name)
            _insert(dbconn, table_name, _rows2iter(val))


class Rows:
    """Contains a table source (database connection or list of dicts) and
    builds instructions as methods growing in chained

    Rows object can be instantiated in two ways.

        1. to pass a table name to Conn.__getitem__, for example,

            >>> conn['table_name']

        2. Directly pass a list of dicts(list[Row]) or dicts yielding iterator
        (Iterable[Row])

            >>> Rows([d1, d2, ...])
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
        """Two different ways of getting items

        Parameters
        ----------
        key: str | slice

        Returns
        -------
        list[RowVal] | Rows

            if isinstance(key, str) returns list[RowVal]

            if isinstance(key, slice) returns Rows

            slicing here is the same as list slicing except that negative values
            cannot be used
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

        if isinstance(key, str):
            return [r[key] for r in self._iter()]
        if isinstance(key, slice):
            return self._islice(key.start, key.stop, key.step)
        raise ValueError("Must pass a str(column name) or a slice")

    def zip(self, other):
        """Attach two Rows side by side until either one is depleted

        Parameters
        ----------
        other: Rows | list[Row] | Iterable[Row]

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        if isinstance(other, Rows):
            _raise_exception_if_preceded_by_grouping_methods(other)

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

    def merge(self, other, merge_type="inner"):
        """Merges two Rows with zip_longest

        If there are rows with the same column names,
        'self' column values remain.

        Parameters
        ----------
        other: Rows

        join_type: str

            'inner', 'left', 'right', 'full'
            default: 'inner'

        Returns
        -------
        Rows
        """
        _raise_exception_if_not_preceded_by_order_and_group(self)
        _raise_exception_if_not_preceded_by_order_and_group(other)

        merge_type = merge_type.lower()

        def mergefn_new_row_ver(rows1, rows2, left, right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in zip_longest(rows1, rows2):
                    if row1 and row2:
                        yield {**row1, **row2}
                    elif row1 and not row2:
                        yield {**row1, **{field: '' for field in right_only}}
                    elif not row1 and row2:
                        yield {**{field: '' for field in left}, **row2}

            elif rows1 != [] and rows2 == []:
                if merge_type in ("left", "full"):
                    for row1 in rows1:
                        yield {**row1, **{field: '' for field in right_only}}

            elif rows1 == [] and rows2 != []:
                if merge_type in ("right", "full"):
                    for row2 in rows2:
                        yield {**{field: '' for field in left}, **row2}

        def mergefn_update_row_ver(rows1, rows2, left, right_only):
            empty_left = {field: '' for field in left}
            empty_right_only = {field: '' for field in right_only}

            if rows1 != [] and rows2 != []:
                for row1, row2 in zip_longest(rows1, rows2):
                    if row1 and row2:
                        row1.update(row2)
                        yield row1
                    elif row1 and not row2:
                        row1.update(empty_right_only)
                        yield row1
                    elif not row1 and row2:
                        empty_left.update(row2)
                        yield empty_left

            elif rows1 != [] and rows2 == []:
                if merge_type in ("left", "full"):
                    for row1 in rows1:
                        row1.update(empty_right_only)
                        yield row1

            elif rows1 == [] and rows2 != []:
                if merge_type in ("right", "full"):
                    for row2 in rows2:
                        empty_left.update(row2)
                        yield empty_left

        if self._history[0]['cmd'] == 'fetch':
            return self._merge(mergefn_update_row_ver, other)
        return self._merge(mergefn_new_row_ver, other)

    def zip_longest(self, other):
        """Attach two Rows side by side as long as any of them remained

        Empty columns (with values of '') generated

        Parameters
        ----------
        other: Rows | list[Row] | Iterable[Row]

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        if isinstance(other, Rows):
            _raise_exception_if_preceded_by_grouping_methods(other)

        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen_new_row_ver():
            row1, rows1 = _spy(pgen())
            row2, rows2 = _spy(_rows2iter(other))

            left = set(row1)
            right_only = [field for field in list(row2) if field not in left]

            empty_left = {field: '' for field in row1}
            empty_right_only = {field: '' for field in right_only}

            for row1, row2 in zip_longest(rows1, rows2):
                if row1 and row2:
                    yield {**row1, **row2}
                elif row1 and not row2:
                    yield {**row1, **empty_right_only}
                elif not row1 and row2:
                    yield {**empty_left, **row2}

        def gen_update_row_ver():
            row1, rows1 = _spy(pgen())
            row2, rows2 = _spy(_rows2iter(other))

            # fields
            left = set(row1)
            right_only = [field for field in list(row2) if field not in left]

            # using the same object over and over is SAFE
            empty_left = {field: '' for field in row1}
            empty_right_only = {field: '' for field in right_only}

            for row1, row2 in zip_longest(rows1, rows2):
                if row1 and row2:
                    row1.update(row2)
                    yield row1
                elif row1 and not row2:
                    row1.update(empty_right_only)
                    yield row1
                elif not row1 and row2:
                    empty_left.update(row2)
                    yield empty_left

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'zip_longest',
            'genfn': gen_update_row_ver if self._history[0]['cmd'] == 'fetch'
            else gen_new_row_ver
        }]
        return newself

    def chain(self, other):
        """Concatenate Rows to the other

        Parameters
        ----------
        other: Rows | list[Row] | Iterable[Row]

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        if isinstance(other, Rows):
            _raise_exception_if_preceded_by_grouping_methods(other)

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
    def order(self, fields_maybe_with_desc):
        """Sort according to columns

        Parameters
        ----------
        fields_maybe_with_desc: str | list[str]

            comma separated str
            each field can be with `desc` keyword, for example,
            'col desc'

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        fields_maybe_with_desc = _listify(fields_maybe_with_desc)
        newself = copy(self)

        # when fetching ordered table from the database.
        # pylint: disable=protected-access
        if len(newself._history) == 1\
                and newself._history[-1]['cmd'] == 'fetch':
            # pylint: disable=protected-access
            prehist = newself._history[-1]
            # pylint: disable=protected-access
            newself._history = [{
                **prehist,
                'cmd_sub': 'order',
                'genfn': _build_initgen(prehist['conn'], prehist['tname'],
                                        fields_maybe_with_desc),
            }]
            return newself

        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen_from_sql():
            tmpdbfd, tmpdb = None, None
            try:
                tmpdbfd, tmpdb = tempfile.mkstemp()
                with _connect(tmpdb) as dbconn:
                    temp_table_name = "temp"
                    _insert(dbconn, temp_table_name, pgen())
                    yield from _fetch(dbconn, temp_table_name,
                                      fields_maybe_with_desc)
            # Nothing to insert, from _insert
            except ValueError:
                yield from []

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
            'fields': fields_maybe_with_desc,
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

    def group(self, fields):
        """Group consecutive rows with the same values for given fields

        Parameters
        ----------
        fields: str | list[str]

            comma separated str

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        fields = _listify(fields)
        newself = copy(self)
        # pylint: disable=protected-access
        pgen = newself._history[-1]['genfn']

        def gen():
            yield from groupby(pgen(), _keyfn(fields))

        # Do not use += operator here, it modifies the object
        # pylint: disable=protected-access
        newself._history = newself._history + [{
            'cmd': 'group',
            'fields': fields,
            'genfn': gen
        }]

        return newself

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

        Parameters
        ----------
        func: Row | Rows -> Row | Rows | None

            takes row (dict(str, int/float/str) when not grouped
            takes Rows when grouped by methods such as by, group, windowed

        Returns
        -------
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
                    # if it's neither dict nor Rows simply ignored.
                    # no Nonetype check
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

    # name 'by' is inevitable
    # pylint: disable=invalid-name
    def by(self, fields_maybe_with_desc):
        """Group rows with fields

        order columns first and then group

        Parameters
        ----------
        fields_maybe_with_desc: str | list[str]

            comma separated str
            each field can be with `desc` keyword, for example,
            'col desc'

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        fields_maybe_with_desc = _listify(fields_maybe_with_desc)
        # need to cut out 'desc', 'asc'
        grouping_fields = [field.split()[0]
                           for field in fields_maybe_with_desc]
        return self.order(fields_maybe_with_desc).group(grouping_fields)

    def filter(self, pred):
        """Filter rows that the predicate function returns True

        Parameters
        ----------
        pred: Row -> bool

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

        def gen(row):
            if pred(row):
                yield row

        return self._apply(gen)

    def update(self, **kwargs):
        """Updates each row with new ones

        Does not mutate rows. Creates new rows.
        kwargs are applied one by one. The next key value pair uses the
        previously updated row

        Parameters
        ----------
        **kwargs: dict[str, Row -> RowVal]

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

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

        Parameters
        ----------
        **kwargs: dict[str, str]

            key str(new field name), value str(old field name)

            >>> rows.rename(new_field_name='old_field_name')

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

        kwargs_rev = {oldkey: newkey for newkey, oldkey in kwargs.items()}

        def renamefn(row):
            yield {kwargs_rev.get(oldkey, oldkey): val
                   for oldkey, val in row.items()}

        return self._apply(renamefn)

    def fold(self, **kwargs):
        """n rows to 1 row

        fold must be preceded by grouping methods (group, by, windowed) and
        each group is shrunken to 1

        Parameters
        ----------
        **kwargs: dict[str, Rows -> RowVal]

        Returns
        -------
        Rows
        """
        _raise_exception_if_not_preceded_by_grouping_methods(self)

        # fold must be preceded by `by`
        grouping_fields = []
        if self._history[-1]['cmd'] == 'group':
            grouping_fields = self._history[-1]['fields']

        # func type unchecked, it's too expensive.
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
        # then self._history[-1]['cmd'] must be 'group', it's check above
        return self._apply(foldfn2)

    def select(self, fields):
        """select fields discarding others

        Parameters
        ----------
        fields: str | list[str]

            comma separated str

        Returns:
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        fields = _listify(fields)

        def selectfn(row):
            yield {field: row[field] for field in fields}

        return self._apply(selectfn)

    def deselect(self, fields):
        """Deselect fields

        Parameters
        ----------
        fields: str | list[str]

            comma separated str

        Returns:
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        fields = _listify(fields)

        fields_set = set(fields)

        def deselectfn(row):
            yield {field: val for field, val in row.items()
                   if field not in fields_set}

        return self._apply(deselectfn)

    def join(self, other, join_type="inner"):
        """Joins two Rows in SQL style

        If there are rows with the same column names,
        'self' column values are updated with 'other' column values.

        Parameters
        ----------
        other: Rows

        join_type: str

            'inner', 'left', 'right', 'full'
            default: 'inner'
        Returns
        -------
        Rows
        """
        _raise_exception_if_not_preceded_by_order_and_group(self)
        _raise_exception_if_not_preceded_by_order_and_group(other)

        # Actually, if it's neither 'left', 'right', nor 'full',
        # all the other strings are considered 'inner',
        # however, this is not a feature.
        # Specifically pass 'inner' if you want inner join
        join_type = join_type.lower()

        def joinfn_update_row_ver(rows1, rows2, left, right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    # updating on the same object multiple times.
                    # Still works, why ?!!,
                    # yielding and returning a appended list is different.
                    # later modifications do not affect previous yielded object
                    # So anyway, these updates in all joining methods
                    # are perfectly safe.
                    row1.update(row2)
                    yield row1

            elif rows1 != [] and rows2 == []:
                if join_type in ("left", "full"):
                    for row1 in rows1:
                        row1.update((field, '') for field in right_only)
                        yield row1

            elif rows1 == [] and rows2 != []:
                if join_type in ("right", "full"):
                    empty_left = {field: '' for field in left}
                    for row2 in rows2:
                        empty_left.update(row2)
                        yield empty_left

        def joinfn_new_row_ver(rows1, rows2, left, right_only):
            if rows1 != [] and rows2 != []:
                for row1, row2 in product(rows1, rows2):
                    yield {**row1, **row2}

            elif rows1 != [] and rows2 == []:
                if join_type in ("left", "full"):
                    for row1 in rows1:
                        yield {**row1, **{field: '' for field in right_only}}

            elif rows1 == [] and rows2 != []:
                if join_type in ("right", "full"):
                    for row2 in rows2:
                        yield {**{field: '' for field in left}, **row2}

        if self._history[0]['cmd'] == 'fetch':
            return self._merge(joinfn_update_row_ver, other)
        return self._merge(joinfn_new_row_ver, other)

    def distinct(self, fields):
        """Returns a Rows with only the first row in each group.

        Order and group with fields drop all the others except for the first
        in each group (remove duplicates)

        Parameters
        ----------
        fields: str | list[str]

            comma separated str

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)
        fields = _listify(fields)

        def distinctfn(_k, rows):
            # impossible to raise stop iteration here
            # pylint: disable=stop-iteration-return
            yield next(rows)

        # pylint: disable=protected-access
        return self.by(fields)._apply(distinctfn)

    def windowed(self, chunk_size, step=1):
        """Returns a Rows of a sliding window(rows) with chunk_size skipping
        every step size rows

        Parameters
        ----------
        chunk_size: int

            positive integer

        step: int

            positive integer, default 1

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

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

        Parameters
        ----------
        pred: Row -> bool

        Returns
        -------
        Rows

        """
        _raise_exception_if_preceded_by_grouping_methods(self)

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

        Parameters
        ----------
        pred: Row -> bool

        Returns
        -------
        Rows
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

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
        """Returns the number(size) of rows

        Returns
        -------
        int
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

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
        """Returns a list of rows(dicts)

        Returns
        -------
        list[Row]
        """
        _raise_exception_if_preceded_by_grouping_methods(self)

        if self._history[0]['cmd'] == 'fetch':
            # no need to copy, becaused it's fetched from the database.
            # pylint: disable=protected-access
            return list(self._iter())
        # pylint: disable=protected-access
        return [row.copy() for row in self._iter()]


def _listify(fields):
    if isinstance(fields, str):
        return [field.strip() for field in fields.split(',')]
    return fields


def _insert_statement(table_name, row):
    """insert into foo values (:a, :b, :c, ...)

    Notice the colons.
    """
    key_fields = ', '.join(":" + field.strip() for field in row)
    return f"insert into {table_name} values ({key_fields})"


def _create_statement(table_name, fields):
    """Create table if not exists foo (...)

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
        right_only = [field for field in list(row2) if field not in set(row1)]

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


def _raise_exception_if_preceded_by_grouping_methods(rows_obj):
    # pylint: disable=protected-access
    cmd = rows_obj._history[-1]['cmd']
    if cmd in ("group", "windowed"):
        raise ValueError("Must not be preceded by grouping methods")


def _raise_exception_if_not_preceded_by_grouping_methods(rows_obj):
    # pylint: disable=protected-access
    cmd = rows_obj._history[-1]['cmd']
    if cmd not in ("group", "windowed"):
        raise ValueError("Must be preceded by grouping methods")


def _raise_exception_if_not_preceded_by_order_and_group(rows_obj):
    # pylint: disable=protected-access
    history = rows_obj._history
    if len(history) < 2:
        raise ValueError("Must be ordered and grouped before")

    # when fetching ordered table from the database.
    if len(history) == 2 and history[0].get('cmd_sub') == 'order':
        return

    cmd1 = history[-2]['cmd']
    cmd2 = history[-1]['cmd']
    if not (cmd1 == 'order' and cmd2 == 'group'):
        raise ValueError("Must be ordered and grouped before")


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
