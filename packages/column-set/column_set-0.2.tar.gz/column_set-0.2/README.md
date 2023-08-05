About
=====

A tiny library for abstraction of data source columns to reduce coupling.
* decouple your code from upstream data sources;
* brings code completion static and interactive development environments;
* reduce the number of strings you copy and paste around your project.

Installation
============

    pip install column-set


Usage
=====

Interactive development e.g. IPython console, Jupyter notebook
--------------------------------------------------------------

There are 2 ways to create a ColumnSet. If you want to use the same names as the upstream data 
source in your code, pass a list of column names e.g.

`schemas.py`

    from column_set import ColumnSet

    MyColumnSet = ColumnSet([
        'Column1',
        'Column2',
        'Column3'
    ])


If you want to use different names to the upstream data source, pass a dict mapping from upstream
names to the names you want to use in your code e.g.

`schemas.py`

    from column_set import ColumnSet

    MyColumnSet = ColumnSet({
        'Column1': 'column_1',
        'Column2': 'column_2',
        'Column3': 'column_3'
    })


Then, import the ColumnSet instance with a handy alias and use in your notebook e.g.

`my_notebook.ipynb`

    from schemas import MyColumnSet as c

    data['temp_col'] = data[c.column_1].map(my_method)

Static development e.g. PyCharm, VS Code
----------------------------------------
The ColumnSet needs to be created in order to access column names. You can use a Python Protocol to 
tell a static development environment, e.g. IDEs like PyCharm and VS Code, what the columns are, 
without running anything.

`schemas.py`

    from typing import Protocol

    class MyColumnSetProps(Protocol):

        column_1: str
        column_2: str
        column_3: str

`my_script.py`

    from schemas import MyColumnSetProps as c

    data['temp_col'] = data[c.column_1].map(my_method)

To save you a bit of time, after you create a ColumnSet, you can use the `._print_protocol` method
to generate the above code snippet, contextualized for your class.

Recommended Usage
-----------------
It is recommended to use both a ColumnSet and a Protocol to enable code completion in any 
environment, e.g.:

`schemas.py`

    from typing import Protocol, Union
    from column_set import ColumnSet

    class MyColumnSetProps(Protocol):

        column_1: str
        column_2: str
        column_3: str 

    
    MyColumnSet: Union[MyColumnSetProps, ColumnSet] = ColumnSet({
        'Column1': 'column_1',
        'Column2': 'column_2',
        'Column3': 'column_3'
    })

Compatibility
-------------
`typing.Protocol` was introduced in Python version 3.8. To enable compatibility with earlier 
versions of Python, import from `typing_extensions` instead, e.g.:

    import sys

    if sys.version_info >= (3, 8):
        from typing import Protocol
    else:
        from typing_extensions import Protocol
