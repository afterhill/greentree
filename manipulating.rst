Working on the Tree
===================

:class:`ast.NodeVisitor` is the primary tool for 'scanning' the tree. To use it,
subclass it and override methods ``visit_Foo``, corresponding to the node classes
(see :doc:`nodes`).

For example, this visitor will print the names of any functions defined in the
given code, including methods and functions defined within other functions::

    class FuncLister(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            print(node.name)
            self.generic_visit(node)

    FuncLister().visit(tree)

.. note::
   If you want child nodes to be visited, remember to call
   ``self.generic_visit(node)`` in the methods you override.

Alternatively, you can run through a list of all the nodes in the tree using
:func:`ast.walk`. There are no guarantees about the order in which
nodes will appear. The following example again prints the names of any functions
defined within the given code::

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            print(node.name)

You can also get the direct children of a node, using :func:`ast.iter_child_nodes`.
Remember that many nodes have children in several sections: for example, an
:class:`~ast.If` has a node in the ``test`` field, and list of nodes in ``body``
and ``orelse``. :func:`ast.iter_child_nodes` will go through all of these.

Finally, you can navigate directly, using the attributes of the nodes.
For example, if you want to get the last node within a function's body, use
``node.body[-1]``. Of course, all the normal Python tools for iterating and
indexing work. In particular, :func:`isinstance` is very useful for checking
what nodes are.

Inspecting nodes
----------------

The :mod:`ast` module has a couple of functions for inspecting nodes:

* :func:`ast.iter_fields` iterates over the fields defined for a node.
* :func:`ast.get_docstring` gets the docstring of a :class:`~ast.FunctionDef`,
  :class:`~ast.ClassDef` or :class:`~ast.Module` node.
* :func:`ast.dump` returns a string showing the node and any children. See also
  `the pretty printer <https://bitbucket.org/takluyver/greentreesnakes/src/default/astpp.py>`_
  used in this guide.

Modifying the tree
------------------

The key tool is :class:`ast.NodeTransformer`. Like :class:`ast.NodeVisitor`, you
subclass this and override ``visit_Foo`` methods. The method should return the
original node, a replacement node, or ``None`` to remove that node from the tree.

The :mod:`ast` module docs have this example, which rewrites name lookups, so
``foo`` becomes ``data['foo']``::

    class RewriteName(ast.NodeTransformer):

        def visit_Name(self, node):
            return ast.copy_location(ast.Subscript(
                value=ast.Name(id='data', ctx=ast.Load()),
                slice=ast.Index(value=ast.Str(s=node.id)),
                ctx=node.ctx
            ), node)
    
    tree = RewriteName().visit(tree)

When replacing a node, the new node doesn't automatically have the ``lineno``
and ``col_offset`` parameters. The example above doesn't deal with this
completely: it copies the location to the :class:`~ast.Subscript` node, but not
to any of the newly created children of that node. See :ref:`fix-locations`.

Be careful when removing nodes. You can quite easily remove a node from a
required field, such as the ``test`` field of an :class:`~ast.If` node. Python
won't complain about the invalid AST until you try to :func:`compile` it, when
a :class:`TypeError` is raised.
