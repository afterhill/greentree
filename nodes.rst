Meet the Nodes
==============

.. currentmodule: ast

An AST represents each element in your code as an object. These are instances of
the various subclasses of :class:`AST` described below. For instance, the code
``a + 1`` is a :class:`BinOp`, with a :class:`Name` on the left, a :class:`Num`
on the right, and an :class:`Add` operator.

Literals
--------

.. class:: Num(n)

   A number - integer, float, or complex. The ``n`` attribute stores the value,
   already converted to the relevant type.

.. class:: Str(s)

   A string. The ``s`` attribute hold the value. In Python 2, the same type
   holds unicode strings too.

.. class:: Bytes(s)

   A :class:`bytes` object. The ``s`` attribute holds the value. Python 3 only.

.. class:: List(elts, ctx)
           Tuple(elts, ctx)

   A list or tuple. ``elts`` holds a list of nodes representing the elements.
   ``ctx`` is :class:`Store` if the container is an assignment target (i.e.
   ``(x,y)=pt``), and :class:`Load` otherwise.

.. class:: Set(elts)

   A set. ``elts`` holds a list of nodes representing the elements.

.. class:: Dict(keys, values)

   A dictionary. ``keys`` and ``values`` hold lists of nodes with matching order
   (i.e. they could be paired with :func:`zip`).

.. class:: Ellipsis()

   Represents the ``...`` syntax for the ``Ellipsis`` singleton.

.. class:: NameConstant(value)

   :data:`True`, :data:`False` or :data:`None`. ``value`` holds one of those constants.

   .. versionadded:: 3.4
      Previously, these constants were instances of :class:`Name`.

Variables
---------

.. class:: Name(id, ctx)

   A variable name. ``id`` holds the name as a string, and ``ctx`` is one of
   the following types.
   
.. class:: Load()
           Store()
           Del()

   Variable references can be used to load the value of a variable, to assign
   a new value to it, or to delete it. Variable references are given a context
   to distinguish these cases.

::

    >>> parseprint("a")      # Loading a
    Module(body=[
        Expr(value=Name(id='a', ctx=Load())),
      ])
    
    >>> parseprint("a = 1")  # Storing a
    Module(body=[
        Assign(targets=[
            Name(id='a', ctx=Store()),
          ], value=Num(n=1)),
      ])

    >>> parseprint("del a")  # Deleting a
    Module(body=[
        Delete(targets=[
            Name(id='a', ctx=Del()),
          ]),
      ])


.. note::
   The pretty-printer used in these examples is available `in the source repository
   <https://bitbucket.org/takluyver/greentreesnakes/src/default/astpp.py>`_ for
   Green Tree Snakes.

.. class:: Starred(value, ctx)

   A ``*var`` variable reference. ``value`` holds the variable, typically a
   :class:`Name` node.
   
   Note that this *isn't* needed to call or define a function with ``*args`` -
   the :class:`Call` and :class:`FunctionDef` nodes have special fields for that.

::

    >>> parseprint("a, *b = it")
    Module(body=[
        Assign(targets=[
            Tuple(elts=[
                Name(id='a', ctx=Store()),
                Starred(value=Name(id='b', ctx=Store()), ctx=Store()),
              ], ctx=Store()),
          ], value=Name(id='it', ctx=Load())),
      ])


Expressions
-----------

.. class:: Expr(value)

   When an expression, such as a function call, appears as a statement by itself
   (an :ref:`expression statement <python:exprstmts>`),
   with its return value not used or stored, it is wrapped in this container.
   ``value`` holds one of the other nodes in this section, or a literal, a
   :class:`Name`, a :class:`Lambda`, or a :class:`Yield` or :class:`YieldFrom`
   node.

::

    >>> parseprint('-a')
    Module(body=[
        Expr(value=UnaryOp(op=USub(), operand=Name(id='a', ctx=Load()))),
      ])

.. class:: UnaryOp(op, operand)

   A unary operation. ``op`` is the operator, and ``operand`` any expression
   node.

.. class:: UAdd
           USub
           Not
           Invert

   Unary operator tokens. :class:`Not` is the ``not`` keyword, :class:`Invert`
   is the ``~`` operator.

.. class:: BinOp(left, op, right)

   A binary operation (like addition or division). ``op`` is the operator, and
   ``left`` and ``right`` are any expression nodes.

.. class:: Add
           Sub
           Mult
           Div
           FloorDiv
           Mod
           Pow
           LShift
           RShift
           BitOr
           BitXor
           BitAnd

   Binary operator tokens.

.. class:: BoolOp(op, values)

   A boolean operation, 'or' or 'and'. ``op`` is :class:`Or` or
   :class:`And`. ``values`` are the values involved. Consecutive operations
   with the same operator, such as ``a or b or c``, are collapsed into one node
   with several values.
   
   This doesn't include ``not``, which is a :class:`UnaryOp`.

.. class:: And
           Or

   Boolean operator tokens.

.. class:: Compare(left, ops, comparators)

   A comparison of two or more values. ``left`` is the first value in the
   comparison, ``ops`` the list of operators, and ``comparators`` the list of
   values after the first. If that sounds awkward, that's because it is::
   
      >>> parseprint("1 < a < 10")
      Module(body=[
        Expr(value=Compare(left=Num(n=1), ops=[
            Lt(),
            Lt(),
          ], comparators=[
            Name(id='a', ctx=Load()),
            Num(n=10),
          ])),
        ])

.. class:: Eq
           NotEq
           Lt
           LtE
           Gt
           GtE
           Is
           IsNot
           In
           NotIn

   Comparison operator tokens.

.. class:: Call(func, args, keywords, starargs, kwargs)

   A function call. ``func`` is the function, which will often be a
   :class:`Name` or :class:`Attribute` object. Of the arguments:

   * ``args`` holds a list of the arguments passed by position.
   * ``keywords`` holds a list of :class:`keyword` objects representing
     arguments passed by keyword.
   * ``starargs`` and ``kwargs`` each hold a single node, for arguments passed
     as ``*args`` and ``**kwargs``.
   
   When compiling a Call node, ``args`` and ``keywords`` are required, but they
   can be empty lists. ``starargs`` and ``kwargs`` are optional.
   
   ::

       >>> parseprint("func(a, b=c, *d, **e)")
       Module(body=[
           Expr(value=Call(func=Name(id='func', ctx=Load()),
                           args=[Name(id='a', ctx=Load())],
                           keywords=[keyword(arg='b', value=Name(id='c', ctx=Load()))],
                           starargs=Name(id='d', ctx=Load()),
                           kwargs=Name(id='e', ctx=Load()))),
         ])

.. class:: keyword(arg, value)
   
   A keyword argument to a function call or class definition. ``arg`` is a raw
   string of the parameter name, ``value`` is a node to pass in.

.. class:: IfExp(test, body, orelse)

   An expression such as ``a if b else c``. Each field holds a single node, so
   in that example, all three are :class:`Name` nodes.

.. class:: Attribute(value, attr, ctx)

   Attribute access, e.g. ``d.keys``. ``value`` is a node, typically a
   :class:`Name`. ``attr`` is a bare string giving the name of the attribute,
   and ``ctx`` is :class:`Load`, :class:`Store` or :class:`Del` according to
   how the attribute is acted on.

   ::

       >>> parseprint('snake.colour')
       Module(body=[
           Expr(value=Attribute(value=Name(id='snake', ctx=Load()), attr='colour', ctx=Load())),
         ])


Subscripting
~~~~~~~~~~~~

.. class:: Subscript(value, slice, ctx)

   A subscript, such as ``l[1]``. ``value`` is the object, often a
   :class:`Name`. ``slice`` is one of :class:`Index`, :class:`Slice`
   or :class:`ExtSlice`. ``ctx`` is :class:`Load`, :class:`Store` or :class:`Del`
   according to what it does with the subscript.

.. class:: Index(value)

   Simple subscripting with a single value::
   
       >>> parseprint("l[1]")
       Module(body=[
         Expr(value=Subscript(value=Name(id='l', ctx=Load()),
                              slice=Index(value=Num(n=1)), ctx=Load())),
         ])

.. class:: Slice(lower, upper, step)

   Regular slicing::
   
       >>> parseprint("l[1:2]")
       Module(body=[
         Expr(value=Subscript(value=Name(id='l', ctx=Load()),
                         slice=Slice(lower=Num(n=1), upper=Num(n=2), step=None),
                         ctx=Load())),
         ])

.. class:: ExtSlice(dims)

   Advanced slicing. ``dims`` holds a list of :class:`Slice` and
   :class:`Index` nodes::
   
       >>> parseprint("l[1:2, 3]")
       Module(body=[
           Expr(value=Subscript(value=Name(id='l', ctx=Load()), slice=ExtSlice(dims=[
               Slice(lower=Num(n=1), upper=Num(n=2), step=None),
               Index(value=Num(n=3)),
             ]), ctx=Load())),
         ])

Comprehensions
~~~~~~~~~~~~~~

.. class:: ListComp(elt, generators)
           SetComp(elt, generators)
           GeneratorExp(elt, generators)
           DictComp(key, value, generators)

   List and set comprehensions, generator expressions, and dictionary
   comprehensions. ``elt`` (or ``key`` and ``value``) is a single node
   representing the part that will be evaluated for each item.
   
   ``generators`` is a list of :class:`comprehension` nodes. Comprehensions with
   more than one ``for`` part are legal, if tricky to get right - see the
   example below.

.. class:: comprehension(target, iter, ifs)

   One ``for`` clause in a comprehension. ``target`` is the reference to use for
   each element - typically a :class:`Name` or :class:`Tuple` node. ``iter``
   is the object to iterate over. ``ifs`` is a list of test expressions: each
   ``for`` clause can have multiple ``ifs``

::

    >>> parseprint("[ord(c) for line in file for c in line]", mode='eval') # Multiple comprehensions in one.
    Expression(body=ListComp(elt=Call(func=Name(id='ord', ctx=Load()), args=[
        Name(id='c', ctx=Load()),
      ], keywords=[], starargs=None, kwargs=None), generators=[
        comprehension(target=Name(id='line', ctx=Store()), iter=Name(id='file', ctx=Load()), ifs=[]),
        comprehension(target=Name(id='c', ctx=Store()), iter=Name(id='line', ctx=Load()), ifs=[]),
      ]))

    >>> parseprint("(n**2 for n in it if n>5 if n<10)", mode='eval')       # Multiple if clauses
    Expression(body=GeneratorExp(elt=BinOp(left=Name(id='n', ctx=Load()), op=Pow(), right=Num(n=2)), generators=[
        comprehension(target=Name(id='n', ctx=Store()), iter=Name(id='it', ctx=Load()), ifs=[
            Compare(left=Name(id='n', ctx=Load()), ops=[
                Gt(),
              ], comparators=[
                Num(n=5),
              ]),
            Compare(left=Name(id='n', ctx=Load()), ops=[
                Lt(),
              ], comparators=[
                Num(n=10),
              ]),
          ]),
      ]))

Statements
----------

.. class:: Assign(targets, value)

   An assignment. ``targets`` is a list of nodes, and ``value`` is a single node.
   
   Multiple nodes in ``targets`` represents assigning the same value to each.
   Unpacking is represented by putting a :class:`Tuple` or :class:`List`
   within ``targets``.
   
   >>> parseprint("a = b = 1")     # Multiple assignment
   Module(body=[
       Assign(targets=[
          Name(id='a', ctx=Store()),
          Name(id='b', ctx=Store()),
        ], value=Num(n=1)),
     ])
   
   >>> parseprint("a,b = c")       # Unpacking
   Module(body=[
       Assign(targets=[
           Tuple(elts=[
               Name(id='a', ctx=Store()),
               Name(id='b', ctx=Store()),
             ], ctx=Store()),
         ], value=Name(id='c', ctx=Load())),
     ])

.. class:: AugAssign(target, op, value)

   Augmented assignment, such as ``a += 1``. In that example, ``target`` is a
   :class:`Name` node for ``a`` (with the :class:`Store` context), op is
   :class:`Add`, and ``value`` is a :class:`Num` node for 1. ``target`` can be
   :class:`Name`, :class:`Subscript` or :class:`Attribute`, but not a
   :class:`Tuple` or :class:`List` (unlike the targets of :class:`Assign`).

.. class:: Print(dest, values, nl)

   Print statement, Python 2 only. ``dest`` is an optional destination (for
   ``print >>dest``. ``values`` is a list of nodes. ``nl`` (newline) is True or
   False depending on whether there's a comma at the end of the statement.

.. class:: Raise(exc, cause)

   Raising an exception, Python 3 syntax. ``exc`` is the exception object to be
   raised, normally a :class:`Call` or :class:`Name`, or ``None`` for
   a standalone ``raise``. ``cause`` is the optional part for ``y`` in
   ``raise x from y``.
   
   In Python 2, the parameters are  instead ``type, inst, tback``, which
   correspond to the old ``raise x, y, z`` syntax.

.. class:: Assert(test, msg)

   An assertion. ``test`` holds the condition, such as a :class:`Compare` node.
   ``msg`` holds the failure message, normally a :class:`Str` node.

.. class:: Delete(targets)

   Represents a ``del`` statement. ``targets`` is a list of nodes, such as
   :class:`Name`, :class:`Attribute` or :class:`Subscript` nodes.

.. class:: Pass()

   A ``pass`` statement.

Other statements which are only applicable inside functions or loops are
described in other sections.

Imports
~~~~~~~

.. class:: Import(names)

   An import statement. ``names`` is a list of :class:`alias` nodes.

.. class:: ImportFrom(module, names, level)

   Represents ``from x import y``. ``module`` is a raw string of the 'from' name,
   without any leading dots, or ``None`` for statements such as ``from . import foo``.
   ``level`` is an integer holding the level of the relative import (0 means
   absolute import).

.. class:: alias(name, asname)

   Both parameters are raw strings of the names. ``asname`` can be ``None`` if
   the regular name is to be used.

::

    >>> parseprint("from ..foo.bar import a as b, c")
    Module(body=[
        ImportFrom(module='foo.bar', names=[
            alias(name='a', asname='b'),
            alias(name='c', asname=None),
          ], level=2),
      ])

Control flow
------------

.. note::
   Optional clauses such as ``else`` are stored as an empty list if they're
   not present.

.. class:: If(test, body, orelse)

   An ``if`` statement. ``test`` holds a single node, such as a :class:`Compare`
   node. ``body`` and ``orelse`` each hold a list of nodes.
   
   ``elif`` clauses don't have a special representation in the AST, but rather
   appear as extra :class:`If` nodes within the ``orelse`` section of the
   previous one.

.. class:: For(target, iter, body, orelse)

   A ``for`` loop. ``target`` holds the variable(s) the loop assigns to, as a
   single :class:`Name`, :class:`Tuple` or :class:`List` node. ``iter`` holds
   the item to be looped over, again as a single node. ``body`` and ``orelse``
   contain lists of nodes to execute. Those in ``orelse`` are executed if the
   loop finishes normally, rather than via a ``break`` statement.

.. class:: While(test, body, orelse)

   A ``while`` loop. ``test`` holds the condition, such as a :class:`Compare`
   node.

.. class:: Break
           Continue

   The ``break`` and ``continue`` statements.

::

    In [2]: %%dump_ast
       ...: for a in b:
       ...:   if a > 5:
       ...:     break
       ...:   else:
       ...:     continue
       ...: 
    Module(body=[
        For(target=Name(id='a', ctx=Store()), iter=Name(id='b', ctx=Load()), body=[
            If(test=Compare(left=Name(id='a', ctx=Load()), ops=[
                Gt(),
              ], comparators=[
                Num(n=5),
              ]), body=[
                Break(),
              ], orelse=[
                Continue(),
              ]),
          ], orelse=[]),
      ])

.. class:: Try(body, handlers, orelse, finalbody)

   ``try`` blocks. All attributes are list of nodes to execute, except for
   ``handlers``, which is a list of :class:`ExceptHandler` nodes.

   .. versionadded:: 3.3

.. class:: TryFinally(body, finalbody)
           TryExcept(body, handlers, orelse)

   ``try`` blocks up to Python 3.2, inclusive. A ``try`` block with both
   ``except`` and ``finally`` clauses is parsed as a :class:`TryFinally`, with
   the body containing a :class:`TryExcept`.

.. class:: ExceptHandler(type, name, body)

   A single ``except`` clause. ``type`` is the exception type it will match,
   typically a :class:`Name` node (or ``None`` for a catch-all ``except:`` clause).
   ``name`` is a raw string for the name to hold the exception, or ``None`` if
   the clause doesn't have ``as foo``. ``body`` is a list of nodes.

::

    In [3]: %%dump_ast
       ...: try:
       ...:   a + 1
       ...: except TypeError:
       ...:   pass
       ...: 
    Module(body=[
        TryExcept(body=[
            Expr(value=BinOp(left=Name(id='a', ctx=Load()), op=Add(), right=Num(n=1))),
          ], handlers=[
            ExceptHandler(type=Name(id='TypeError', ctx=Load()), name=None, body=[
                Pass(),
              ]),
          ], orelse=[]),
      ])


.. class:: With(items, body)

   A ``with`` block. ``items`` is a list of :class:`withitem` nodes representing
   the context managers, and ``body`` is the indented block inside the context.

   .. versionchanged:: 3.3

      Previously, a :class:`With` node had ``context_expr`` and ``optional_vars``
      instead of ``items``. Multiple contexts were represented by nesting
      a second :class:`With` node as the only item in the ``body`` of the first.

.. class:: withitem(context_expr, optional_vars)

   A single context manager in a ``with`` block. ``context_expr`` is the context
   manager, often a :class:`Call` node. ``optional_vars`` is a :class:`Name`,
   :class:`Tuple` or :class:`List` for the ``as foo`` part, or ``None`` if that
   isn't used.

::

    In [3]: %%dump_ast
      ...: with a as b, c as d:
      ...:     do_things(b, d)
      ...:
    Module(body=[
        With(items=[
            withitem(context_expr=Name(id='a', ctx=Load()), optional_vars=Name(id='b', ctx=Store())),
            withitem(context_expr=Name(id='c', ctx=Load()), optional_vars=Name(id='d', ctx=Store())),
          ], body=[
            Expr(value=Call(func=Name(id='do_things', ctx=Load()), args=[
                Name(id='b', ctx=Load()),
                Name(id='d', ctx=Load()),
              ], keywords=[], starargs=None, kwargs=None)),
          ]),
      ])


Function and class definitions
------------------------------

.. class:: FunctionDef(name, args, body, decorator_list, returns)

   A function definition. 
   
   * ``name`` is a raw string of the function name.
   * ``args`` is a :class:`arguments` node.
   * ``body`` is the list of nodes inside the function.
   * ``decorator_list`` is the list of decorators to be applied, stored outermost
     first (i.e. the first in the list will be applied last).
   * ``returns`` is the return annotation (Python 3 only).

.. class:: Lambda(args, body)

   ``lambda`` is a minimal function definition that can be used inside an
   expression. Unlike :class:`FunctionDef`, ``body`` holds a single node.

.. class:: arguments(args, vararg, kwonlyargs, kwarg, defaults, kw_defaults)
   
   The arguments for a function. In **Python 3**:
   
   * ``args`` and ``kwonlyargs`` are lists of :class:`arg` nodes.
   * ``vararg`` and ``kwarg`` are single :class:`arg` nodes, referring to the
     ``*args, **kwargs`` parameters.
   * ``defaults`` is a list of default values for arguments that can be passed
     positionally. If there are fewer defaults, they correspond to the last n
     arguments.
   * ``kw_defaults`` is a list of default values for keyword-only arguments. If
     one is ``None``, the corresponding argument is required.

   .. versionchanged:: 3.4
   
      Up to Python 3.3, ``vararg`` and ``kwarg`` were raw strings of the
      argument names, and there were separate ``varargannotation`` and
      ``kwargannotation`` fields to hold their annotations.

   In **Python 2**, the attributes for keyword-only arguments are not needed.

.. class:: arg(arg, annotation)

   A single argument in a list; Python 3 only. ``arg`` is a raw string of the
   argument name, ``annotation`` is its annotation, such as a :class:`Str` or
   :class:`Name` node.
   
   In Python 2, arguments are instead represented as :class:`Name` nodes, with
   ``ctx=Param()``.

::

    In [52]: %%dump_ast
       ....: @dec1
       ....: @dec2
       ....: def f(a: 'annotation', b=1, c=2, *d, e, f=3, **g) -> 'return annotation':
       ....:   pass
       ....: 
    Module(body=[
        FunctionDef(name='f', args=arguments(args=[
            arg(arg='a', annotation=Str(s='annotation')),
            arg(arg='b', annotation=None),
            arg(arg='c', annotation=None),
          ], vararg=arg(arg='d', annotation=None), kwonlyargs=[
            arg(arg='e', annotation=None),
            arg(arg='f', annotation=None),
          ], kw_defaults=[
            None,
            Num(n=3),
          ], kwarg=arg(arg='g', annotation=None), defaults=[
            Num(n=1),
            Num(n=2),
          ]), body=[
            Pass(),
          ], decorator_list=[
            Name(id='dec1', ctx=Load()),
            Name(id='dec2', ctx=Load()),
          ], returns=Str(s='return annotation')),
      ])

.. class:: Return(value)

   A ``return`` statement.

.. class:: Yield(value)
           YieldFrom(value)

   A ``yield`` or ``yield from`` expression. Because these are expressions, they
   must be wrapped in a :class:`Expr` node if the value sent back is not used.
   
   .. versionadded::  3.3
      The :class:`YieldFrom` node type.

.. class:: Global(names)
           Nonlocal(names)

   ``global`` and ``nonlocal`` statements. ``names`` is a list of raw strings.

.. class:: ClassDef(name, bases, keywords, starargs, kwargs, body, decorator_list)

   A class definition.
   
   * ``name`` is a raw string for the class name
   * ``bases`` is a list of nodes for explicitly specified base classes.
   * ``keywords`` is a list of :class:`keyword` nodes, principally for 'metaclass'.
     Other keywords will be passed to the metaclass, as per `PEP-3115
     <http://www.python.org/dev/peps/pep-3115/>`_.
   * ``starargs`` and ``kwargs`` are each a single node, as in a function call.
     starargs will be expanded to join the list of base classes, and kwargs will
     be passed to the metaclass.
   * ``body`` is a list of nodes representing the code within the class
     definition.
   * ``decorator_list`` is a list of nodes, as in :class:`FunctionDef`.

::

    In [59]: %%dump_ast
       ....: @dec1
       ....: @dec2
       ....: class foo(base1, base2, metaclass=meta):
       ....:   pass
       ....: 
    Module(body=[
        ClassDef(name='foo', bases=[
            Name(id='base1', ctx=Load()),
            Name(id='base2', ctx=Load()),
          ], keyword=
            keyword(arg='metaclass', value=Name(id='meta', ctx=Load())),
          ], starargs=None, kwargs=None, body=[
            Pass(),
          ], decorator_list=[
            Name(id='dec1', ctx=Load()),
            Name(id='dec2', ctx=Load()),
          ]),
      ])
