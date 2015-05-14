Green Tree Snakes - the missing Python AST docs
===============================================

**Abstract Syntax Trees**, ASTs, are a powerful feature of Python. You can write
programs that inspect and modify Python code, after the syntax has been parsed,
but before it gets compiled to byte code. That opens up a world of possibilities
for introspection, testing, and mischief.

The `official documentation for the ast module <http://docs.python.org/3/library/ast>`_
is good, but somewhat brief. *Green Tree Snakes* is more like a field guide
(or should that be forest guide?) for working with ASTs. To contribute to the
guide, see the `source repository <https://bitbucket.org/takluyver/greentreesnakes>`_.

Contents:

.. toctree::
   :maxdepth: 2
   
   tofrom.rst
   nodes.rst
   manipulating.rst
   examples.rst

.. seealso::
   
   `Instrumenting the AST <http://www.dalkescientific.com/writings/diary/archive/2010/02/22/instrumenting_the_ast.html>`_
     Using AST tools to assess code coverage.
     
   `astviewer <https://github.com/titusjan/astviewer>`_
     A simple GUI for exploring ASTs


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

