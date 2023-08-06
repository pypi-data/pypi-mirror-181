from selectolax.parser import Node

def _find_parent(node, tag):
    while node:
        if node.tag == tag:
            return node

        node = node.parent

    return None

def _count_prev(x, only_elements=True):
    rv = 0

    x = x.prev
    while not x is None:
        if only_elements and x.tag != '-text' and x.tag != '_comment':
            rv = rv + 1
        x = x.prev

    return rv

def _count_next(x, only_elements=True):
    rv = 0
    x = x.next
    while not x is None:
        if only_elements and x.tag != '-text' and x.tag != '_comment':
            rv = rv + 1
        x = x.next

    return rv

def _height_of(x):
    rv = 0
    while not x is None and x.tag != 'html':
        rv = rv + 1
        x = x.parent

    return rv

def _node_in(x, xs):
    """Is node x in list xs?"""
    for z in xs:
        if _node_equals(x, z):
            return True

    return False

def _node_equals(a, b):
    """selectolax node equality uses .innerHTML equality, which is, not quite right."""

    if isinstance(a, Node) and isinstance(b, Node):
        return node_equals_actual(a, b)

    if isinstance(a, list) or isinstance(b, list):
        if not isinstance(a, list) or not isinstance(b, list):
            return False

        if len(a) != len(b):
            return False

        for i in range(len(a)):
            if not _node_equals(a[i], b[i]):
                return False

            return True

    return a == b

def node_equals_actual(a, b):
    """Guaranteed that a and b are actually Node.

This version takes 2.23s"""

    # A node is the same if:
    # it has the same # of previous siblings
    # it has the same distance to the root, and each parent has the same # of previous siblings

    while a and b:
        # Calling count_pref is slow - function call overhead, plus we don't actually
        # need a count, we just need to know if they have the same # of siblings.
        a_ = a.prev
        b_ = b.prev

        while a_ and b_:
            a_ = a_.prev
            b_ = b_.prev

        if a_ or b_:
            return False

        a = a.parent
        b = b.parent

    return a is None and b is None
