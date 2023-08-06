from .selectors import _candidate_selectors, _candidate_repeating_selectors

from collections import namedtuple
import itertools
from .bannable_product import bannable_product
import time
from .utils import urljoin
from .equals import _node_in, _height_of
from .extract import extract_rows
from .cache import _make_cached_tree_css

TreeStats = namedtuple('TreeStats', ['url', 'tree', 'row_examples', 'cache', 'extract_rows_cache', 'cached_tree_css', 'attribute_examples', 'singleton_columns', 'optional_columns', 'max_distinct_column_values'])

SelectorAttribute = namedtuple('SelectorAttribute', ['selector', 'attribute'])
ColumnChoices = namedtuple('ColumnCandidates', ['attribute', 'nodes', 'selectors'])

def _no_banned_nodes(tree_css_func, selector, reject):
    if not reject:
        return True

    nodes = tree_css_func(selector)
    for node in reject:
        if _node_in(node, nodes):
            return False

    return True

def _only_the_same_conversions(x):
    attr = x[0][1]

    for y in x:
        if y[1] != attr:
            return False

    return True

def infer_column(url, tree_css_func, tree, keep, reject=[], cache={}):
    """In the given tree, propose some candidate selectors that would find elements
       that have the values in "keep". (Some massaging may be needed, eg, stripping,
       reading an attribute.)

       Don't propose a selector if it would select a node in reject."""


    # Correct: [225, 225, 16, 16]
    # We're getting: [453, 285, 183, 123]

    # Item codes sets=:
    # sets=[[(<Node span>, None, 'Item Code: LPGIG00133')], [(<Node span>, None, 'Item Code: LPGIG00114')], [(<Node span>, None, 'Item Code: LPMSI00429')], [(<Node span>, None, 'Item Code: LPCNO00048')]]

    start_time = time.time()

    needles_to_keep = {}
    for i, needle in enumerate(keep):
        arr = needles_to_keep.get(needle, [])
        arr.append(i)
        needles_to_keep[needle] = arr

    choices_arr = []
    for i in range(len(keep)):
        choices_arr.append([])

    traverse_time = time.time()
    for node in tree.root.traverse():
        for i, (k, v) in enumerate(node.attrs.items()):
            if k != 'class' and k != 'id' and k != 'data-preorder-index':
                if (node.tag == 'a' and k == 'href') or (node.tag == 'img' and k == 'src'):
                    v = urljoin(url, v)

                if v in needles_to_keep:
                    for q in needles_to_keep[v]:
                        choices_arr[q].append((node, k, v))
        # To avoid wasting a ton of resource, only check nodes that have
        # kids, and all kids are text nodes or empty nodes.
        if node.child:
            ok = True
            kid = node.child
            while kid:
                if kid.child:
                    ok = False
                    break
                kid = kid.next

            if ok:
                t = node.text().strip()
                if t in needles_to_keep and (not reject or not _node_in(node, reject)):
                    for q in needles_to_keep[t]:
                        choices_arr[q].append((node, None, t))

    sets = []
    for i, choices in enumerate(choices_arr):
        if not choices:
            print('infer_column failed on needle {} after {}'.format(keep[i], time.time() - start_time))
            return []
        sets.append(choices)

    print('sets len: {} took: {}'.format([len(q) for q in sets], time.time() - start_time))

    # Create all the permutations of the sets; permutations that have different attribute selection
    # rules are banned.
    permutations = [x for x in itertools.product(*sets) if _only_the_same_conversions(x)]

    #print('before: permutations is {}'.format(permutations))

    # permutations is a seq of seq of tuple (node, attribute, label)
    # change it into a seq of (attribute, seq of tuple (node, label))
    permutations = [(x[0][1], [(y[0], y[2]) for y in x]) for x in permutations]
    #print('after : permutations is {}'.format(permutations))

    # Try to find list of candidate selectors that find the nodes

    # Don't use any q-classes from the nodes themselves
    t = time.time()
    banned_q_classes = {}
    for (attribute, tuples) in permutations:
        for (node, label) in tuples:
            if 'class' in node.attrs:
                for klazz in node.attrs['class'].split(' '):
                    if klazz.startswith('q-'):
                        banned_q_classes['.' + klazz] = True

    #print('banned_q_classes = {}'.format(banned_q_classes))

    candidates = []
    total_time = 0
    for i, permutation in enumerate(permutations):
        (attribute, nodes) = permutation
        t = time.time()

        # TODO: possible optimization - this feels like a dynamic programming problem?
        #       would it be useful to cache the intermediate results of intersection?
        #
        #       oh, and/or, should we guarantee that we sort by smallest sets first?

        sets = [set(_candidate_selectors(tree, node, cache=cache)) for (node, label) in nodes]
#        print([len(x) for x in sets])
#        print([
#            len(set.intersection(sets[0], sets[1])),
#            len(set.intersection(sets[1], sets[2])),
#            len(set.intersection(sets[1], sets[2], sets[0]))
#        ])
        selectors = list(set.intersection(*sets))
        selectors = [x for x in selectors if not '.q-' in x or not x.split(' ')[-1] in banned_q_classes]

        # Only accept if the selector doesn't pick any of the rejected nodes.
        selectors = selectors if not reject else [selector for selector in selectors if _no_banned_nodes(tree_css_func, selector, reject)]
        total_time += time.time() - t

        if selectors:
            candidates.append(ColumnChoices(
                attribute=attribute,
                nodes=[node[0] for node in nodes],
                selectors=sorted(selectors, key=lambda x: x)
            ))
    print('intersection took {} len(candidates)={}'.format(total_time, len(candidates)))

    #print('candidates is {}'.format(candidates))
    return candidates

def _all_at_same_height(nodes):
    if not nodes:
        return False

    height = _height_of(nodes[0])

    for node in nodes:
        if _height_of(node) != height:
            return False

    return True

def _all_extracted_in_examples(extracted, row_examples):
    for row in row_examples:
        if not row in extracted:
            return False

    return True

def _sanity_check_row_examples(row_examples):
    if not row_examples:
        raise Exception('need to provide at least one row example')

    for row_example in row_examples:
        if len(row_example) != len(row_examples[0]):
            raise Exception('all row examples should be the same length (' + str(len(row_examples[0])) + '): ' + str(row_example))

        all_empty = True
        for attr in row_example:
            if attr:
                all_empty = False

        if all_empty:
            raise Exception('at least one attribute in the row must be defined: ' + str(row_example))

def _summarize_tree(url, tree, row_examples):
    cache = {}
    extract_rows_cache = {}
    cached_tree_css = _make_cached_tree_css(tree)


    # If an attribute is a "singleton", it means it's unique across all the examples
    # and should be computed relative to the HTML root, not relative to a repeating
    # selector. (This can cause false positives! The user will have to ensure they
    # add examples that are _not_ unique.)
    singleton_columns = []
    optional_columns = []
    max_distinct_column_values = 0

    # Pivot the row examples so instead of logical rows, we have all the birth years,
    # all the first names, etc
    attribute_examples = []
    for i in range(len(row_examples[0])):
        is_singleton = True
        all_empty = True
        some_empty = False
        attribute_examples.append([row_example[i] for row_example in row_examples])

        attribute_values = {}

        for x in attribute_examples[-1]:
            attribute_values[x] = True
            if x != attribute_examples[-1][0]:
                is_singleton = False

            if x:
                all_empty = False
            else:
                some_empty = True

        distinct_column_values = len([x for x in attribute_values.keys() if not x is None])

        if distinct_column_values > max_distinct_column_values:
            max_distinct_column_values = distinct_column_values
        singleton_columns.append(is_singleton)
        optional_columns.append(some_empty)

        if all_empty:
            raise Exception('you must provide at least one non-null example for attribute ' + str(i))

    print(attribute_examples)

    return TreeStats(
        url=url,
        tree=tree,
        row_examples=row_examples,
        cache=cache,
        extract_rows_cache=extract_rows_cache,
        cached_tree_css=cached_tree_css,
        attribute_examples=attribute_examples,
        singleton_columns=singleton_columns,
        optional_columns=optional_columns,
        max_distinct_column_values=max_distinct_column_values
    )

def _infer_column_choices(stats):
    rv = []

    for i in range(len(stats.attribute_examples)):

        reject = []
        #for j in range(len(attribute_examples)):
        #   if i == j:
        #       continue

        #   for needle in attribute_examples[j]:
        #       if not needle in attribute_examples[i]:
        #           reject.append(needle)


        # TODO: do we need to 2 passes of infer_column? Once to find the nodes that
        #       are candidates, and a second time to exclude those nodes from the other
        #       attributes.
        qq = time.time()

        selectors = infer_column(stats.url, stats.cached_tree_css, stats.tree, [x for x in stats.attribute_examples[i] if x], reject, cache=stats.cache)
        print('! infer_column[{}] took {} from examples {} (reject={})'.format(i, time.time() - qq, stats.attribute_examples[i], reject))

        if not selectors:
            raise Exception('unable to infer candidates for attribute ' + str(i) + ': ' + str(stats.attribute_examples[i]))

        # Ensure that singleton attributes always have 'html' style selectors
        if stats.singleton_columns[i]:
            for j, opts in enumerate(selectors):
                #print('!!! opts is {}'.format(opts))
                selectors[j] = opts._replace(selectors = [x if x.startswith('html ') else ('html ' + x) for x in opts.selectors])

        rv.append(selectors)

        #print(selectors)
    return rv

def _generate_candidate_extract_params(stats, column_choices, index_to_column, candidate_repeating_selectors):
    ban_entries = 0
    attempts = 0
    crs_attempts = 0
    appends = 0

    t = time.time()

    column_row_examples = []
    for i in range(len(stats.row_examples[0])):
        column_rows = []
        for row in stats.row_examples:
            column_rows.append([row[i]])

        column_row_examples.append(column_rows)

    optional_columns = []
    for i in range(len(stats.row_examples[0])):
        is_optional = False
        for j in stats.row_examples:
            if j[i] == None:
                is_optional = True

        optional_columns.append(is_optional)



    selector_attributes = []

    for column_choice in column_choices:
        choices = []
        for (attribute, nodes, selectors) in column_choice:
            #choices.extend([SelectorAttribute(attribute=attribute, selector=selector) for selector in selectors if len(selector) < 25])
            choices.extend([SelectorAttribute(attribute=attribute, selector=selector) for selector in selectors])

        choices = sorted(set(choices), key=lambda x: (len(x.selector), x.selector))
        selector_attributes.append(choices)

    # TODO: future optimization
    # Test the attributes in order of the one with the _fewest_ candidate selectors first.
    # e.g. for relish, test price (3 selectors), then sale price (80), then title (671 !)
    #
    # This brings a _big_ speedup
    shortest_to_longest = []

    for i in range(len(column_choices)):
        shortest_to_longest.append(i)

    shortest_to_longest.sort(key=lambda x: len(selector_attributes[x]))
    print('### after {} shortest_to_longest={} {}'.format(time.time() - t, shortest_to_longest, [len(x) for x in selector_attributes]))
    #print(selector_attributes[0])

    # TODO remove me
    #candidate_repeating_selectors = ['a .h1', 'a .medium--left', '.small--one-half']
    #candidate_repeating_selectors = ['a .medium--left', 'a .h1', '.small--one-half']
    #candidate_repeating_selectors = ['a .h1']
    #candidate_repeating_selectors = ['a .medium--left']

    #print(selector_attributes[0])
    #print(selector_attributes[1])
    #print(selector_attributes[2])


    already_tested = {}
    for candidate_repeating_selector in candidate_repeating_selectors:
        product_iters = 0
        #if candidate_repeating_selector != '.small--one-half':
        #    continue
        #print(candidate_repeating_selector)
        crs_attempts += 1
        repeating_elements = stats.cached_tree_css(candidate_repeating_selector)
        #print(candidate_repeating_selector + ': ' + str(len(repeating_elements)))

        if len(repeating_elements) < stats.max_distinct_column_values:
            #print('! too few repeating elements')
            continue

        if not _all_at_same_height(repeating_elements):
            #print('! not all at same height')
            continue

        key = ','.join([x.attrs['data-preorder-index'] for x in repeating_elements])

        if key in already_tested:
            continue

        already_tested[key] = True


        # Compute which columns have at least 1 node contained in this sub-tree
        # This lets us efficiently skip selectors that don't use sibling combinators
        # (TODO: and maybe a lot of sibing combinators? eg if the first selector selects
        # a child, vs the current element)

        contained_columns = {}
        for el in repeating_elements:
            for node in el.traverse():
                dpi = node.attrs['data-preorder-index']
                if not dpi in index_to_column:
                    continue

                for index in index_to_column[dpi]:
                    contained_columns[index] = True

        #print('_all_at_same_height took {}'.format(time.time() - t))

        #print(' ok: ' + candidate_repeating_selector)

        bans = [{} for i in column_choices]

        attempt_time = time.time()
        column_times = [0] * len(selector_attributes)
        for chosen_selectors in bannable_product(bans, *selector_attributes):
            product_iters += 1
            columns = []

            for i, (selector, attribute) in enumerate(chosen_selectors):
                column = {
                    'selector': selector,
                }

                if optional_columns[i]:
                    column['optional'] = True

                if attribute:
                    column['conversions'] = ['@' + attribute]
                columns.append(column)

            all_columns_ok = True
            for i, column in enumerate(columns):
                extract_params = {
                    'selector': candidate_repeating_selector,
                    'columns': [column]
                }
                t = time.time()

                if not optional_columns[i] and not column['selector'].startswith('html ') and not '+' in column['selector'] and not '~' in column['selector']:
                    if not i in contained_columns:
                        all_columns_ok = False
                        ban_entries += 1
                        bans[i][chosen_selectors[i]] = True
                        column_times[i] += time.time() - t
                        continue



                extracted = extract_rows(
                    stats.url,
                    stats.cached_tree_css,
                    extract_params,
                    stats.extract_rows_cache,
                )
                column_times[i] += time.time() - t

                if not _all_extracted_in_examples(extracted, column_row_examples[i]):
                    #print("ban column {}: {}".format(i, chosen_selectors[i]))
                    all_columns_ok = False
                    ban_entries += 1
                    bans[i][chosen_selectors[i]] = True


            if all_columns_ok:
                print('{}: {}'.format(candidate_repeating_selector, [x.selector for x in chosen_selectors]))
                extract_params = {
                    'selector': candidate_repeating_selector,
                    'columns': columns
                }

                #print(extract_params)
                attempts += 1
                extracted = extract_rows(
                    stats.url,
                    stats.cached_tree_css,
                    extract_params,
                    stats.extract_rows_cache,
                )

                if _all_extracted_in_examples(extracted, stats.row_examples):
                    print('!!! found after {} attempts, {} crs_attempts, {} bans'.format(attempts, crs_attempts, ban_entries))
                    yield extract_params
                else:
                    # If each individual column extracted OK, but the row as a whole didn't,
                    # we've probably got a garbage repeating selector.
                    break

        print('actually trying {} ({} els, {} product_iters) took {} column_times={}'.format(candidate_repeating_selector, len(repeating_elements), product_iters, time.time() - attempt_time, column_times))


def _filter_duplicate_column_selectors(column_choices):
    """This tries to optimize our search space by ruling out a selector if it's proposed for
    multiple columns.

    We must consider if the selector is targeting an attribute.
    e.g. <img src="foo" alt="A title"> can contribute to two columns via
    img[src] and img[alt]."""
    candidate_selector_sets = []

    dupes = {}
    for i, column_choice in enumerate(column_choices):
        #print('column_choice={}'.format(column_choice))
        column_selectors = []
        for (attribute, nodes, selectors) in column_choice:
            for selector in selectors:
                key = (attribute, selector)
                obj = dupes.get(key, {})
                obj[i] = True
                dupes[key] = obj

    # Filter column_choices to exclude attribute/selector pairs that appear in multiple columns.
    rv = []
    for i, column_choice in enumerate(column_choices):
        new_column_choice = []
        for (attribute, nodes, selectors) in column_choice:
            filtered_selectors = [selector for selector in selectors if len(dupes[(attribute, selector)]) == 1]

            if filtered_selectors:
                new_column_choice.append((attribute, nodes, filtered_selectors))

        if not new_column_choice:
            raise Exception('could not infer non-duplicated selectors for column {}'.format(i))
        rv.append(new_column_choice)

    #print('BEFORE   is {}'.format(column_choices))
    #print('AFTER rv is {}'.format(rv))
    return rv

def infer_rows(urls, trees, n_row_examples):
    # As a DX convenience, we let you pass a single tree/example - wrap those into a list
    # of size 1.
    if not isinstance(trees, list):
        trees = [trees]
        n_row_examples = [n_row_examples]
        urls = [urls]

    # TODO: validate trees/row_examples are same len

    # NB: you must have called annotate_preorder on the tree; we use the preorder indexes
    #     to cache css selector evaluations, and eventually, to prune the search space

    for ex in n_row_examples:
        _sanity_check_row_examples(ex)
        print(ex)

    n_stats = [_summarize_tree(urls[i], trees[i], n_row_examples[i]) for i in range(len(trees))]

    t = time.time()
    n_column_choices = [_infer_column_choices(n_stats[i]) for i in range(len(n_stats))]

    # For each tree, for each column compute the intersection of its selectors with
    # the those of the other tree's selectors for that column, if they're optional.
    #
    # The idea is that if a given tree generates a novel selector, it's not generalizable,
    # and therefore, not correct.
    #
    #  TODO: I'm not confident this code is correct, I think it can fail for optional
    #  attributes, eg.

    for column_index in range(len(n_column_choices[0])):
        unions = []
        for tree_index in range(len(trees)):
            all_selectors = set([selector for column_candidates in n_column_choices[tree_index][column_index] for selector in column_candidates.selectors])
            unions.append(all_selectors)

        for i, column_candidate in enumerate(n_column_choices[0][column_index]):
            selectors = set(column_candidate.selectors)
            for tree_index in range(1, len(trees)):
                selectors = selectors & unions[tree_index]

            if selectors:
                n_column_choices[0][column_index][i] = n_column_choices[0][column_index][i]._replace(selectors = list(selectors))

    print('! infer_column(s) took {}'.format(time.time()-t))

    t = time.time()

    tree = trees[0]
    stats = n_stats[0]
    column_choices = n_column_choices[0]

    column_choices = _filter_duplicate_column_selectors(column_choices)

    print('! intersecting took {}'.format(time.time() - t))

    column_nodes = []
    index_to_column = {}
    for i, column_choice in enumerate(column_choices):
        nodes_i = {}
        for (attribute, nodes, selectors) in column_choice:
            for node in nodes:
                nodes_i[node.attrs['data-preorder-index']] = node

        column_nodes.append(nodes_i.values())

        for index in nodes_i.keys():
            old_value = [] if not index in index_to_column else index_to_column[index]
            old_value.append(i)
            index_to_column[index] = old_value

    #print('candidate_selector_sets[0] = {}'.format(candidate_selector_sets[0]))


    t = time.time()

    candidate_repeating_selectors = ['html']

    if stats.max_distinct_column_values > 1:
        candidate_repeating_selectors = _candidate_repeating_selectors(tree, stats.singleton_columns, column_nodes, cache=stats.cache)

    print("! producing {} candidate_repeating_selectors took {}".format(len(candidate_repeating_selectors), time.time() - t))

    t = time.time()
    #print(candidate_repeating_selectors)

    for extract_params in _generate_candidate_extract_params(stats, column_choices, index_to_column, candidate_repeating_selectors):
        ok = True
        print('! after {} found candidate extract_params {}'.format(time.time() - t, extract_params))
        for i in range(1, len(trees)):
            print('!! testing tree {}'.format(i))
            extracted = extract_rows(urls[i], trees[i], extract_params, n_stats[i].extract_rows_cache)
            print(extracted)

            if not _all_extracted_in_examples(extracted, n_row_examples[i]):
                print('...does not match expected, search continues')
                ok = False
                break

        if ok:
            return extract_params

    return None
