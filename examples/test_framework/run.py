#!/usr/bin/python3
"""This will run asserts.py, but keep going if an assertion fails.

It also transforms assertions of the form a==b into a function call, which can
display more info if the 
"""
import ast

filename = "asserts.py"
with open(filename, encoding='utf-8') as f:
    code = f.read()
    
class AssertCmpTransformer(ast.NodeTransformer):
    """Transform 'assert a==b' into 'assert_equal(a, b)'
    """
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
        
        # Return the original node if we don't want to change it.
        return node

def assert_equal(a, b):
    if a != b:
        raise AssertionError("%r != %r" % (a, b))

tree = ast.parse(code)
lines = [None] + code.splitlines()  # None at [0] so we can index lines from 1
test_namespace = {'assert_equal': assert_equal}

tree = AssertCmpTransformer().visit(tree)

for node in tree.body:
    wrapper = ast.Module(body=[node])
    try:
        co = compile(wrapper, filename, 'exec')
        exec(co, test_namespace)
    except AssertionError as e:
        print("Assertion failed on line", node.lineno, ":")
        print(lines[node.lineno])
        # If the error has a message, show it.
        if e.args:
            print(e)
        print()
