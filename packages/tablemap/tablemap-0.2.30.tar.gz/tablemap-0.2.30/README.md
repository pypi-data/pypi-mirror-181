# About

Tablemap is a handy little Python data wrangling tool for whom Pandas or SQL feel clunky when problems
touch just one small step further than their routine, ordinary circle.

While a table is nothing but a list of dictionaries, oftentimes Pandas looks like a long way around. 
It can wait for what it's really made.

Some people might be happy if only they can easily chain up some processes they do on tables 
without worrying too much about memory. Less on stackoverflow.com for arcane Pandas spells. This is for those. 

# Installation

Requires only built-in Python libraries. No dependencies.

```
pip install tablemap
```


# Tutorial

## Saving tables in the database

Let's create a table `t1` in `sample.db`. 

```python
from tablemap import Conn, Rows

t1 = [
    {'col1': 'a', 'col2': 4},
    {'col1': 'a', 'col2': 5},
    {'col1': 'b', 'col2': 1},
]

conn = Conn('sample.db')
conn['t1'] = t1
```

The right-hand side of the assignment can be a list of dictionaries, an iterator that yields dictionaries, or an object fetched from the connection (`Rows` object, shows up soon), for example, `conn['t1']` on which you can chain up table-manipulating methods such as `map`, `update`, `by`, `chain`, and so on.

Each dictionary represents a row in a table. For instance `{'col1': 'a', 'col2': 4}` is a row with two columns, `col1` and `col2`.

Opening and closing the database is safely handled in the background. 


To browse tables in the database,

```python
rs = conn['t1']
print(rs)

# to turn it into a familiar data structure,
print(rs.list())

# to see only part of it 
rs1 = rs[1:]
print(rs1)

# rs[1:] creates a new object, rs is not modified.
print(rs.size(), rs1.size())
```

If you prefer GUI, you can open up the file `sample.db` with software like [SQLiteStudio](https://sqlitestudio.pl/) or [DB Browser for SQLite](https://sqlitebrowser.org/). 

Once you clean up the table, you may wish to begin the analysis with Pandas.

```python
import pandas as pd

df = pd.DataFrame(conn['t1'].list())
conn['t1_copy'] = df.to_dict('records')
```

## Rows objects
`conn['t1']` is a `Rows` object. Rows objects can be created in two ways

1. Pass a table name to Conn object, `conn['t1']` 
2. Directly pass a list of dictionaries or a dictionary yielding iterator to the class `Rows`, for example, `Rows(t1)`

Passing a column name to a `Rows` object returns a list of elements for the column, `Rows(t1)['col1'] == ['a', 'a', 'b']`

A `Rows` object represents a list of dictionaries and they have a few methods to chain up to transform a table.

*** 

## Methods for table manipulation

+ ### `chain`

To concatenate `t1` with itself,  

```python
conn['t1_double'] = conn['t1'].chain(conn['t1'])
```

A list of dictionaries or an iterator that yields dictionaries can be passed as an argument as well.

```python
conn['t1_double'] = conn['t1'].chain(t1)

```

Tables for concatenation must have the same columns. The order of the columns is not important.


+ #### A few to brag about. 

    Some of the properties of this module that make data-wrangling easier 
        
    1. All the methods in this section create a new `Rows` object.  

        ```python
        rs = conn['t1']
        rs1 = rs.chain(t1)
        ```

        `rs` and `rs1` are different objects, so `rs` is not `chain`ed.

    2. `rs` (or `rs1`) does not contain any data in the table, yet. It simply holds instructions and is executed when it's needed. (when you want it to be saved in the database, to be printed out, to be listed up, or simply to get the size of it)

        So you can easily combine all the methods safely and freely, for example, (`filter` is not covered yet, hopefully, it's self-evident.)

        ```python
        rs = conn['t1']
        high = rs.filter(lambda r: r['col2'] > 4)
        low = rs.filter(lambda r: r['col2'] < 2)
        rs2 = high.chain(low)
        ```

        Since `rs2` simply holds instructions without actually performing operations, the above code requires very little computing power unless you want to save it in the database or see the result for yourself.  

    3. Memory requirement is minimal. 

        ```python
        conn['t1_1'] = rs2
        ```

        Now it actually works because you are trying to save the rows `rs2` generates in the table `t1_1`. Still, `tablemap` does not load up all of `rs2` on memory. It loads and saves one-by-one. 

    4. Opens and closes the database automatically and safely. Users don't have to worry about it. Even the keyboard interrupts (like ctrl-c) during the table insertion do not corrupt the database.

 

+ ### `filter` and `update`
Each row is simply a dictionary with column names as keys, so you can access a column value by passing a column name to the row(dictionary). To create new columns or update the existing ones,

```python
# \ for line-continuation
conn['t1_1'] = conn['t1']\
    .filter(lambda r: r['col2'] > 2)\
    .update(
        col2=lambda r: r['col2'] + 1,
        col3=lambda r: r['col1'] + str(r['col2'])
    )
```

A lambda expression is a nameless function. In the expression `lambda r: r['col2'] > 2`, the parameter `r` represents a single dictionary and the whole expression returns an evaluated value of `r['col'] > 2` for each iteration.

Columns are updated sequentially, so `col3` has `a5` and `a6`, not `a4` and `a5`.


+ ### `by` and `fold`

To sum up `col2` grouped by `col1`,

```python
conn['t1_col2sum_groupby_col1'] = conn['t1'].by('col1')\
    .fold(
        col2_sum=lambda rs: sum(rs['col2']),
        col2_min=lambda rs: min(rs['col2']),
        col2_max=lambda rs: max(rs['col2']),
    )
```

`by` takes columns as arguments (multiple args for multiple columns) for grouping and the next process (`fold` in this case) takes on each group (a `Rows` object).

In the expression `lambda rs: sum(rs['col2'])`, the parameter `rs` represents a `Rows` object. So `rs['col2']` returns a list of elements in the column `col2`. And of course for that reason, you may chain up all the methods in this section.

While `update` works on a dictionary, `fold` does on a `Rows` object. (`fold` folds n rows to one row. So the lambda expression in `fold` must return a single value, like a string or a number.)

`fold` must be preceded by grouping methods such as `by` or `windowed` which shows up soon.

+ ### `rename`

To replace old column names with new ones,

```python
conn['t1_1'].rename(
    c2min='col2_min',
    c2max='col2_max'
)
```

+ ### `join`

To merge tables,

```python
conn['t2'] = [
    {'col1': 'b', 'col3': -1},
    {'col1': 'c', 'col3': 3},
    {'col1': 'b', 'col3': ''},
]

conn['t1_col3'] = conn['t1'].by('col1')\
    .join(conn['t2'].by('col1'), 'full')
```

There are 4 join types, 'inner', 'left', 'right', and 'full'. The default is 'inner'. You may want to check [this tutorial](https://www.w3schools.com/sql/sql_join.asp) if you are not familiar with these terms.

Tables must be grouped to be joined.

If the table `t1` and `t2` have columns with the same name, `t1` columns will be updated with `t2` columns.

Empty strings represent missing values.




+ ### `distinct`
To group the table `t1` by `col1` and to leave only the first row in each group, (removing duplicates) 

```python
conn['t1_1'] = conn['t1'].distinct('col1')
```
You can pass multiple columns to `distinct` as in `by`

+ ### `select` and `deselect` 
You can pass columns to `select` or `deselect` to pick up or delete specific columns in a table

```python
conn['t1_1'] = conn['t1'].update(col3=lambda r: r['col2'] + 1)\
    .deselect('col1', 'col2')
```


+ ### slicing 

To take the first 2 rows from table `t1`,

```python
print(conn['t1'][:2])
```

Negative values are not supported. Of course, you can chain up other methods after slicing. 

Like the other methods, slicing does not execute the operation. `conn['t1'][:2]` holds the instruction to take the first two rows, not the rows themselves. However `print` function enforces taking the first two rows to print out on the screen. So it works as expected.

Grouping methods like `by` or `windowed` cannot come right before slicing (Technically trivial but it will only add confusion)

`conn['t1']['col1']` is not slicing, it returns a list of column values, not a `Rows` object. 

+ ### `takewhile` and `dropwhile`
`takewhile` and `dropwhile` take a predicate (a function that returns a value to be considered `True` or `False`, already seen it in `filter`) as an argument to do what these names suggest. Refer to [itertools.takewhile](https://docs.python.org/3/library/itertools.html#itertools.takewhile) and [itertools.dropwhile](https://docs.python.org/3/library/itertools.html#itertools.dropwhile)

Again, grouping methods cannot come right before these methods.


+ ### `map`

When `update` or `fold` is not powerful enough, you can deal with a row or `Rows` in a more sophisticated way.

```python
# Some of you may feel uncomfortable with the naming.
# This is just a lambda function for 'map'
# Hard to justify spending time on naming a function used nowhere else.
def fn4t1(rs):
    # rs is a Rows object. 
    # Now you can apply all the methods in this section.
    # And again, since these methods create a new Rows object instead of modifying the original,
    # it's safe to build any combinations as you want. 
    tot = sum(rs['col2'])
    # you don't always have to pass a function to `update`, same for `fold`
    return rs[:1].update(col2_sum=tot)

conn['t1_col2sum_groupby_col1'] = conn['t1'].by('col1')\
    .map(fn4t1)\
    .deselect('col2')
```

The argument for `map` is a function that returns a `Rows` object or a single dictionary, or None. It takes a single dictionary as an argument or a `Rows` object in case the previous process is `by`(`group`) or `windowed`.



+ ### `zip` and `zip_longest`
Like `chain`, zip takes a list of dictionaries or an iterator that yields dictionaries or a `Rows` object as an argument. The argument updates the `Rows` object row by row until either one is depleted. 

With `zip`, the above `fn4t1` can be rewritten as

```python
def fn4t1(rs):
    rs2 = [{'col2_sum': sum(rs['col2'])}]
    return rs.zip(rs2)
```

Another example,

```python
conn['t1_1'] = conn['t1'].zip({'idx': i} for i in range(100))
```

`zip_longest` creates empty columns when either one is depleted.

+ ### `merge`

The same interface as `join`. While `join` combines cross-producted rows from two tables,
`merge` simply `zip_longest` them. For example when `join` combines 2 rows against 3 rows in each group,
6 rows are generated while `merge` produces only 3 rows.


+ ### `windowed`
When you need to group a chunk of consecutive rows,

```python
conn['t1_1'] = conn['t1'].windowed(4, 2).fold(
    sum=lambda rs: sum(rs['col2'])
)
```

`fold` takes the first 4 consecutive rows(of course a `Rows` object) and the next 4 starting from the 3rd (skipping 2 rows) and so on. When rows less than or equal to 4 are left, it will be the last. 

+ ### `order` and `group`

Actually, `by` is a combination of `order` and `group`, you can control more precise by separating these processes, 

```python
conn['t1_col2sum_groupby_col1'] = conn['t1']\
    .order('col1', 'col2 desc').group('col1')\
    .map(fn4t1)
```

Now, `map` takes a `Rows` object where `col2` is sorted in descending order.

The keyword `desc` can be either upper-cased, lower-cased or mixed. 

The ascending order is the default.


## Some remarks 

- `by` (or `group`. Again, `by` is a combination of `order` and `group`) and `windowed` are the only grouping methods. 
    1. `join` must be preceded by `by` (must be ordered before grouping, so `group` without `order` is not allowed). 
    2. `fold` must be preceded by `group`(`by`) or `windowed`. 
    3. `map` may or may not be preceded by `group`(`by`) or `windowed`. (the function that's passed to `map` takes a row (dictionary) or a `Rows` object as an argument)
    4. No other cases are allowed for grouping. Therefore `by` cannot come right before `windowed` for instance although it makes sense semantically. 

- To do the cross-join, consider passing a (lexical) closure on the method `map` to avoid repetitive table fetching.

    ```python
    def fn4t1():
        # table2 = conn['t1'] does not do any good.
        # You should list it up. 
        # Otherwise 'map' attempts to fetch 
        # the table 't2' from the database 
        # for every group by 'col1' 
        table2 = conn['t2'].list()
        def innerfn(rs):
            ...do some work using table2
            return something 
        return innerfn

    conn['some_table'] = conn['t1'].by('col1').map(fn4t1())
    ```

    If you want to add an index column for each group,

    ```python
    def fn4t1():
        n = 0 
        def innerfn(rs):
            # nonlocal 
            nonlocal n
            n += 1
            return rs.update(n=n)
        return innerfn 

    conn['t1_1'] = conn['t1'].by('col1').map(fn4t1())
    ```
    Might not be that useful in any way though.


- `Rows` methods do not update objects directly. They create a new object every time a `Rows` method is invoked.

    So the following code works as expected.
    ```python
    rs = conn['t1']
    rs.by('col1').fold(col2_tot=sum(rs['col2']))
    ```
    In expression `sum(rs['col2'])`, `rs` represents a `Rows` object when the statement `rs = conn['t1']` is evaluated. Methods like `by` or `fold` in the statement do not affect `rs` in `sum(rs('col2'))`.

    Take a close look at the next.

    ```python
    def fn4t1(rs):
        # The original rs is not updated
        # Only newrs holds the instruction to update the column 'col2' 
        # (The update instruction will not be executed in the next statement, 
        # newrs simply keeps the instruction here for the time it's really needed, 
        # like for example, database insertion or content print-out)
        newrs = rs.update(col2=lambda r: r['col2'] + 1)
        return newrs.order('col2').zip(rs.order('col2 desc').rename(col2_1='col2'))

    conn['t1_1'] = conn['t1'].by('col1').map(fn4t1)

    ``` 

- Since column names are dictionary keys, they are case-sensitive. However, column names in Sqlite3 (on which `tablemap` is powered) are case-insensitive by default. To avoid confusion, it is strongly recommended that you keep them lower-cased, and spaces stripped. 

    `tablemap` does not automatically convert upper-case column names. Making any excessive assumptions on users' intentions might add more confusions. 

## [API Documentation](https://tablemap.readthedocs.io/en/latest/tablemap.html#module-tablemap.tablemap)