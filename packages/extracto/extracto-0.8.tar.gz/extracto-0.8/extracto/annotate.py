import re
from selectolax.parser import HTMLParser

def prepare(tree, for_infer=True):
    if for_infer:
        sanitize(tree)

    wrap_orphans(tree)
    add_q_classes(tree)

    if for_infer:
        annotate_preorder(tree)

    return tree

def sanitize(tree):
    '''Remove the contents of style and script tags, but leave the tags themselves.'''

    for node in tree.root.traverse(include_text=True):
        if node.tag == '-text':
            if u'\xa0' in node.text_content:
                node.replace_with(node.text_content.replace(u'\xa0', ' '))

def add_q_classes(tree):
    for node in tree.root.traverse(include_text=True):
        if node.tag != '-text':
            continue


        # Try to short-circuit quickly if the text is all whitespace, or too long to be interesting
        non_whitespace = 0
        for x in node.text_content:
            if x != ' ' and x != '\n' and x != '\r' and x != '\t' and x != '-' and x != '+' and x != '*':
                non_whitespace += 1
                break

        if non_whitespace == 0 or non_whitespace > 20:
            continue

        sanitized = ''
        last_was_hyphen = True
        for char in node.text_content.lower():
            if (char >= 'a' and char <= 'z') or (char >= '0' and char <= '9'):
                last_was_hyphen = False
                sanitized += char
            elif not last_was_hyphen:
                sanitized += '-'
                last_was_hyphen = True

        if last_was_hyphen:
            sanitized = sanitized[0:-1]

        if sanitized and len(sanitized) < 20:
            q_class = 'q-' + sanitized
            parent = node.parent
            if 'class' in parent.attrs:
                parent.attrs['class'] = parent.attrs['class'] + ' ' + q_class
            else:
                parent.attrs['class'] = q_class

def wrap_orphans(tree):
    span_doc = HTMLParser('<span>span</span>')

    # An "orphaned" text node is a text node that has element siblings, for example:
    # <p><b>Name</b> Colin</p>
    #
    # It's impossible to specify such a node via a CSS selector. Instead, wrap it in a span:
    # <p><b>Name</b><span> Colin</span></p>

    # Do one pass to find all the orphans - can't mutate while iterating
    orphans = []
    for node in tree.root.traverse(include_text=True):
        if node.tag != '-text':
            continue

        if node.prev is None and node.next is None:
            continue

        if node.text().strip():
            orphans.append(node)

    # Do a second pass where we mutate
    for node in orphans:
        cloned = span_doc.clone()
        span = cloned.root.child.next.child
        span.child.replace_with(node.text_content)
        node.replace_with(span)


def annotate_preorder(tree):
    """Annotate elements in the tree with their preorder traversal index. This
       could let us determine when a selector is unlikely to be useful, e.g.
       because it selects nodes too low in the tree."""
    index = 0

    to_visit = [tree.root]

    while to_visit:
        visiting = to_visit.pop()
        visiting.attrs['data-preorder-index'] = index
        index += 1

        kid = visiting.last_child
        while kid:
            to_visit.append(kid)
            kid = kid.prev
