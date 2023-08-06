from typing import Pattern
from selectolax.parser import HTMLParser, Node
from .utils import urljoin
from .cache import _make_cached_tree_css

def ensure_str(x):
    if isinstance(x, str):
        return x.replace(u'\xa0', ' ')

    if isinstance(x, Node):
        return x.text().replace(u'\xa0', ' ').strip()

    return str(x)

def maybe_int(x):
    try:
        return int(x)
    except:
        return None

NO_CONVERSIONS = []

def apply_eval(url, tree, node, selector, conversions):
    """Evaluate a set of instructions to node, returning its result."""

    rv = node

    if selector:
        nodes = tree(selector, rv)

        if len(nodes) == 0:
            return None

        rv = nodes[0]

    for conversion in conversions or []:
        if isinstance(conversion, Pattern):
            m = conversion.search(ensure_str(rv))
            if m:
                if 'rv' in m.groupdict():
                    rv = m.group('rv')
            else:
                rv = None
        elif conversion == 'int':
            rv = maybe_int(ensure_str(rv))
        elif conversion.startswith('@'):
            tag = rv.tag
            attr_name = conversion[1:]

            if attr_name in rv.attrs:
                rv = rv.attrs[attr_name]

                if (tag == 'a' and attr_name == 'href') or (tag == 'img' and attr_name == 'src'):
                    rv = urljoin(url, rv)
            else:
                rv = None
        else:
            raise Exception('unknown conversion: ' + conversion)

    if isinstance(rv, Node):
        return ensure_str(rv)

    return rv



def extract_rows(url, tree, instructions, cache=None):
    if isinstance(tree, HTMLParser):
        tree = _make_cached_tree_css(tree)

    if not 'selector' in instructions:
        raise Exception('expected top-level key `selector`, but was missing')

    selector = instructions['selector']
    if not isinstance(selector, str):
        raise Exception('expected top-level key `selector` to be str, but was: ' + str(selector))

    if not 'columns' in instructions:
        raise Exception('expected top-level key `columns`, but was missing')

    columns = instructions['columns']
    if not isinstance(columns, list):
        raise Exception('expected top-level key `columns` to be list, but was: ' + str(columns))

    if not columns:
        raise Exception('expected at least one value in `columns`, but was empty')

    rv = []

    for i in range(len(columns)):
        column = columns[i]
        if not isinstance(column, dict):
            raise Exception('expected `columns[' + str(i) + ']` to be a dict, but was ' + str(column))

        if not isinstance(column.get('selector', ''), str):
            raise Exception('expected `columns[' + str(i) + '].selector` to be str, but was ' + str(columns[i].selector))

        if not isinstance(column.get('optional', False), bool):
            raise Exception('expected columns[' + str(i) + '].optional to be absent or bool, but was ' + str(column['optional']))

        if not isinstance(column.get('conversions', []), list):
            raise Exception('expected `columns[' + str(i) + '].conversions` to be absent or list, but was ' + str(column['conversions']))

    for node in tree(selector):
        candidate = []

        ok = True

        for column in columns:
            #print('Evaluating for key=' + k)
            key = None

            selector = None if not 'selector' in column else column['selector']
            conversions = NO_CONVERSIONS if not 'conversions' in column else column['conversions']

            if not cache is None:
                key = (node.attrs['data-preorder-index'], selector, str(conversions))

            if not cache is None and key in cache:
                value = cache[key]
            else:
                value = apply_eval(url, tree, node, selector, conversions)

                if not cache is None:
                    cache[key] = value

            if value is None and (not 'optional' in column or not column['optional']):
                #print('  did not find value')
                ok = False
                break

            candidate.append(value)

        if ok:
            rv.append(candidate)

    return rv


