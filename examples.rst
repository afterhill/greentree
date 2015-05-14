Examples of working with ASTs
=============================

Working versions of these examples are in the `examples directory of the source
repository <https://bitbucket.org/takluyver/greentreesnakes/src/default/examples>`_.

Wrapping integers
-----------------

In Python code, ``1/3`` would normally be evaluated to a floating-point number,
that can never be exactly one third. Mathematical software, like `SymPy
<http://sympy.org/>`_ or `Sage <http://www.sagemath.org/>`_, often wants to use
exact fractions instead. One way to make ``1/3`` produce an exact fraction is
to wrap the integer literals ``1`` and ``3`` in a class::

    class IntegerWrapper(ast.NodeTransformer):
        """Wraps all integers in a call to Integer()"""
        def visit_Num(self, node):
            if isinstance(node.n, int):
                return ast.Call(func=ast.Name(id='Integer', ctx=ast.Load()),
                                args=[node], keywords=[])
            return node

    tree = ast.parse("1/3")
    tree = IntegerWrapper().visit(tree)
    # Add lineno & col_offset to the nodes we created
    ast.fix_missing_locations(tree)

    # The tree is now equivalent to Integer(1)/Integer(3)
    # We would also need to define the Integer class and its __truediv__ method.

See `wrap_integers.py <https://bitbucket.org/takluyver/greentreesnakes/src/default/examples/wrap_integers.py>`_
for a working demonstration.

Simple test framework
---------------------

These two manipulations let you write test scripts as a simple series of
``assert`` statements. First, we need to run the statements one by one,
so execution doesn't stop at the first test failure::

    tree = ast.parse(code)
    lines = [None] + code.splitlines()  # None at [0] so we can index lines from 1
    test_namespace = {}

    for node in tree.body:
        wrapper = ast.Module(body=[node])
        try:
            co = compile(wrapper, "<ast>", 'exec')
            exec(co, test_namespace)
        except AssertionError:
            print("Assertion failed on line", node.lineno, ":")
            print(lines[node.lineno])
            # If the error has a message, show it.
            if e.args:
                print(e)
            print()

Next, we transform ``assert a == b`` into a function call ``assert_equal(a, b)``,
which can give more information about the failure. We could turn many other
assertions into similar function calls.

::

    class AssertCmpTransformer(ast.NodeTransformer):
        def visit_Assert(self, node):
            if isinstance(node.test, ast.Compare) and \
                    len(node.test.ops) == 1 and \
                    isinstance(node.test.ops[0], ast.Eq):
                call = ast.Call(func=ast.Name(id='assert_equal', ctx=ast.Load()),
                                args=[node.test.left, node.test.comparators[0]],
                                keywords=[])
                # Wrap the call in an Expr node, because the return value isn't used.
                newnode = ast.Expr(value=call)
                ast.copy_location(newnode, node)
                ast.fix_missing_locations(newnode)
                return newnode
            
            # Remember to return the original node if we don't want to change it.
            return node

See `test_framework/run.py <https://bitbucket.org/takluyver/greentreesnakes/src/default/examples/test_framework/run.py>`_
for a working demonstration of both parts.
