import re
from .equals import _count_prev, _find_parent

def _valid_css_class(name):
    if re.search('^[a-zA-Z0-9_-]+$', name):
        return True

    return False

def _valid_id(name):
    if re.search('^[a-zA-Z0-9_]+$', name):
        return True

    return False

def _candidate_selectors(
        tree,
        needle,
        by_tag=True,
        by_id=True,
        by_class=1,
        by_attr=True,
        by_attr_value=True,
        by_adjacent_sibling=True,
        by_general_sibling=True,
        by_child=True,
        by_descendant=True,
        by_nth_child=True,
        by_previous_tr=True,
        cache={}
):
    """Returns candidate CSS selectors that will identify the given node.

Nodes must be annotated with preorder index."""

    if needle.tag == '-text' or needle.tag == '_comment' or needle.tag == '-undef' or needle.tag == '!doctype':
        return []

    if needle.tag == 'html' or needle.tag == 'body':
        return [needle.tag]

    dpi = needle.attrs['data-preorder-index']
    cache_key = dpi + '!' + str([by_tag, by_id, by_class, by_attr, by_attr_value, by_adjacent_sibling, by_general_sibling, by_child, by_descendant, by_nth_child, by_previous_tr])
    old_cache_value = cache.get(cache_key, None)
    if old_cache_value != None:
        return old_cache_value

    candidates = []

    if by_tag:
        candidates.append(needle.tag)

    if by_id:
        if 'id' in needle.attrs and needle.attrs['id'] and  _valid_id(needle.attrs['id']):
            candidates.append('#' + needle.attrs['id'])

    if by_class > 0:
        # CONSIDER: by pairs of classes? eg .w-full.container ?
        if 'class' in needle.attrs and needle.attrs['class']:
            classes = [x for x in needle.attrs['class'].split(' ') if x]
            for x in classes:
                if _valid_css_class(x):
                    candidates.append('.' + x)

    if by_attr or by_attr_value:
        for x in needle.attrs:
            if x == 'class' or x == 'id' or x == 'data-preorder-index' or x.startswith('on') or x.startswith('js'):
                continue

            if by_attr:
                candidates.append('[' + x + ']')

            if by_attr_value and needle.attrs[x] and not '"' in needle.attrs[x]:
                candidates.append('[' + x + '="' + needle.attrs[x] + '"]')

    # nth-child
    if by_nth_child:
        candidates.append(needle.tag + ':nth-child(' + str(_count_prev(needle) + 1) + ')')

    simple_me_candidates = None

    if by_adjacent_sibling or by_general_sibling or by_child or by_descendant or by_previous_tr:
        simple_me_candidates = _candidate_selectors(
            tree,
            needle,
            cache=cache,
            by_tag=True,
            by_id=True,
            by_class=1,
            by_attr=True,
            by_attr_value=True,
            by_adjacent_sibling=False,
            by_general_sibling=False,
            by_child=False,
            by_descendant=False,
            by_nth_child=True,
            by_previous_tr=False,
        )

    if by_previous_tr:
        # Are we in a table? Permit us to be found relative to the _previous_ row.
        # This lets us work on some sites that abuse tables to present data (eg, HN)
        #
        # This feels a _little_ specialized to HN... :(
        parent_tr = _find_parent(needle, 'tr')
        if parent_tr and parent_tr.prev and parent_tr.prev.tag == 'tr':
            previous_tr_candidates = _candidate_selectors(
                tree,
                parent_tr.prev,
                cache=cache,
                by_tag=True,
                by_id=True,
                by_class=1,
                by_attr=True,
                by_attr_value=True,
                by_adjacent_sibling=False,
                by_general_sibling=False,
                by_child=False,
                by_descendant=False,
                by_nth_child=False,
                by_previous_tr=False,
            )

            for candidate in previous_tr_candidates:
                for me_candidate in simple_me_candidates:
                    candidates.append(candidate + ' + tr ' + me_candidate)


    # Compute the set of previous siblings
    previous_elements = []
    p = needle.prev
    while p:
        if p.tag != '-text' and p.tag != '_comment' and p.tag != '!doctype':
            previous_elements.append(p)

        p = p.prev

    if previous_elements:
        if by_adjacent_sibling:
            adjacent_candidates = _candidate_selectors(
                tree,
                previous_elements[0],
                cache=cache,
                by_adjacent_sibling=False,
                by_general_sibling=False,
                by_child=False,
                by_descendant=False,
                by_previous_tr=False,
            )

            for x in adjacent_candidates:
                for y in simple_me_candidates:
                    candidates.append(x + ' + ' + y)

        if by_general_sibling:
            for sibling in previous_elements:
                adjacent_candidates = _candidate_selectors(
                    tree,
                    sibling,
                    cache=cache,
                    by_adjacent_sibling=False,
                    by_general_sibling=False,
                    by_child=False,
                    by_descendant=False,
                    by_previous_tr=False,
                )

                for x in adjacent_candidates:
                    for y in simple_me_candidates:
                        candidates.append(x + ' ~ ' + y)

    if by_child and needle.parent:
        parent_candidates = _candidate_selectors(
            tree,
            needle.parent,
            cache=cache,
            by_adjacent_sibling=False,
            by_general_sibling=False,
            by_child=False,
            by_descendant=False,
            by_previous_tr=False,
        )

        for x in parent_candidates:
            for y in simple_me_candidates:
                candidates.append(x + ' > ' + y)


    if by_descendant:
        parent = needle.parent

        while parent and parent.tag != 'body' and parent.tag != 'html':
            parent_candidates = _candidate_selectors(
                tree,
                parent,
                cache=cache,
                by_adjacent_sibling=False,
                by_general_sibling=False,
                by_child=False,
                by_descendant=False,
                by_previous_tr=False,
            )

            for x in parent_candidates:
                for y in simple_me_candidates:
                    candidates.append(x + ' ' + y)

            parent = parent.parent

    rv = sorted(set(candidates))
    cache[cache_key] = rv
    #print('{}: {}: '.format(dpi, len(rv)))
    #if len(rv) > 900:
    #    print(rv)
    return rv

def _candidate_repeating_selectors(tree, singleton_columns, attribute_nodes, cache={}):
    """Generate a set of CSS selectors that describe repeating elements that could be used
to enumerate the attributes."""

    # The naive approach: for every node in tree, generate its selectors. Return the union of all
    # of them.
    #
    # However, this is slow. We can do better in two cases.

    # Case 1: pre-order index after attributes'

    # <div>                    <!-- 0 -->
    #   <span>Value 1</span>   <!-- 1 -->
    #   <span>Value 2</span>   <!-- 2 -->
    # </div>
    # <footer>&copy;</footer>  <!-- 3 -->

    # Anything after index 1 cannot be correct.
    # Everything after the pre-order index of the attribute with the highest value can be ignored.

    # Case 2: pre-order index before attributes'
    # <nav>                        <!-- 0 -->
    #   <button>Click me</button>  <!-- 1 -->
    # </nav>
    # <div>                        <!-- 2 -->
    #   <span>Value 1</span>       <!-- 3 -->
    #   <span>Value 2</span>       <!-- 4 -->
    # </div>

    # `<button>` can never be correct: none of the targets are contained within its parent's descendants.
    # More specifically:
    # If selectors use the sibling combinators (`+` or `~`), the attributes must be contained within
    #   its parent's descendants
    # For all other selectors, the targets must be contained within its descendants

    # Case 1: a naive implementation is to take the highest preorder-index we've found.
    #         This is safe, but may not be optimal. Still, better than nothing!
    
    # Case 2, I think, lends itself to a simpler implementation: walk all the discovered nodes. Enumerate
    # their ancestor IDs into a set. When deciding if we should include an element, check if it's parent ID
    # is in the set.

    # Another optimization: both of these cases can be considered on a per-attribute basis.
    #
    # Take the attribute that produces the most restrictive set of nodes.
    # Note that "singleton" attributes are a confounder -- because they get referenced via
    # absolute "html ..." CSS, they should not be considered when restricting things.

    print('! candidate_repeating_selectors, len(attribute_nodes)={}, inner lens={}'.format(len(attribute_nodes), [len(x) for x in attribute_nodes]))

    # NB: tree must be annotated with preorder indexes
    # Every entry in permutations represents a proposed set of nodes that might answer the problem.
    # There could be many entries.
    # Each entry is len(singleton_columns) long.

    highest_preorder_indexes = []
    candidate_rootses = []

    non_singleton_column_exists = False
    for x in singleton_columns:
        if not x:
            non_singleton_column_exists = True


    for i, nodes in enumerate(attribute_nodes):
        if singleton_columns[i] and non_singleton_column_exists:
            continue

        highest_preorder_index_i = -1
        candidate_roots_i = {}

        for node in nodes:
            index = int(node.attrs['data-preorder-index'])

            if highest_preorder_index_i == -1 or index > highest_preorder_index_i:
                highest_preorder_index_i = index

            if index in candidate_roots_i:
                continue

            parent_tr = _find_parent(node, 'tr')
            if parent_tr and parent_tr.prev and parent_tr.prev.tag == 'tr':
                candidate_roots_i[int(parent_tr.prev.attrs['data-preorder-index'])] = True

            while node and node.tag != 'html':
                index = int(node.attrs['data-preorder-index'])
                candidate_roots_i[index] = True
                node = node.parent
        highest_preorder_indexes.append(highest_preorder_index_i)
        candidate_rootses.append(candidate_roots_i)

    highest_preorder_index = min([x for x in highest_preorder_indexes if x != -1] or [-1])
    candidate_roots = [x for x in candidate_rootses if len(x) > 0]
    candidate_roots.sort(key=lambda x: len(x))
    candidate_roots = (candidate_roots or [{}])[0]


    use_candidate_roots = len(candidate_roots) > 0
    rv = []

    for node in tree.root.traverse():
        if node.tag == 'html':
            continue

        # DANGEROUS: I assert that we can ignore leaf elements -- we'll likely also
        #            have generated a reference to a parent of theirs, eg
        if not node.child:
            continue

        node_index = int(node.attrs['data-preorder-index'])

        if highest_preorder_index != -1 and node_index > highest_preorder_index:
            continue

        if use_candidate_roots and not int(node.parent.attrs['data-preorder-index']) in candidate_roots:
            continue
        #else:
        #    node.attrs['class'] = 'ok'

        # TODO: should we limit how long the selector can be? Very long selectors are probably
        #       keying off of things like URLs, that are likely to change.
        #candidate_repeating_selectors.extend([x for x in candidate_selectors(tree, node) if len(x) < 20])
        rv.extend(_candidate_selectors(tree, node, cache=cache))

    rv = sorted(set(rv), key=lambda x: (len(x), x))

    #print(candidate_roots)
    #print(tree.html)
    #return []
    return rv
