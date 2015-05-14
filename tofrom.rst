Getting to and from ASTs
========================

To build an ast from code stored as a string, use :func:`ast.parse`. To turn the
ast into executable code, pass it to :func:`compile` (which can also compile a
string directly).

::

    >>> tree = ast.parse("print('hello world')")
    >>> tree
    <_ast.Module object at 0x9e3df6c>
    >>> exec(compile(tree, filename="<ast>", mode="exec"))
    hello world

Modes
-----

Python code can be compiled in three modes. The root of the AST depends on the
`mode` parameter you pass to :func:`ast.parse`, and it must correspond to the
`mode` parameter when you call :func:`compile`.

* **exec** - Normal Python code is run with ``mode='exec'``. The root of the AST
  is a :class:`ast.Module`, whose ``body`` attribute is a list of nodes.
* **eval** - Single expressions are compiled with ``mode='eval'``, and passing
  them to :func:`eval` will return their result. The root of the AST is an
  :class:`ast.Expression`, and its ``body`` attribute is a single node, such as
  :class:`ast.Call` or :class:`ast.BinOp`. This is different from
  :class:`ast.Expr`, which holds an expression within an AST.
* **single** - Single statements or expressions can be compiled with
  ``mode='single'``. If it's an expression, :func:`sys.displayhook` will be called
  with the result, like when code is run in the interactive shell. The root of
  the AST is an :class:`ast.Interactive`, and its ``body`` attribute is a list
  of nodes.

.. _fix-locations:

Fixing locations
----------------

To compile an AST, every node must have ``lineno`` and ``col_offset`` attributes.
Nodes produced by parsing regular code already have these, but nodes you create
programmatically don't. There are a few helper functions for this:

* :func:`ast.fix_missing_locations` recursively fills in any missing locations
  by copying from the parent node. The rough and ready answer.
* :func:`ast.copy_location` copies ``lineno`` and ``col_offset`` from one node to
  another. Useful when you're replacing a node.
* :func:`ast.increment_lineno` increases ``lineno`` for a node and its
  children, pushing them further down a file.

Going backwards
---------------

Python itself doesn't provide a way to turn a compiled code object into an AST,
or an AST into a string of code. Third party tools, like `Meta
<http://pypi.python.org/pypi/meta>`_, allow you to do this - but they might not
be as well supported.
