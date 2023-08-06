# Calling modest's CSS engine is expensive, and we often call it
# with the same arguments. So, try to cache things.
def _make_cached_tree_css(tree):
    tree_css_cache = {}
    def cached_tree_css(sel, node=None):
        if sel.startswith('html '):
            node = None
            sel = sel[5:]

        if node is None:
            if sel in tree_css_cache:
                return tree_css_cache[sel]

            rv = tree.css(sel)
            tree_css_cache[sel] = rv
            return rv

        dpi = node.attrs.get('data-preorder-index')

        key = None
        if dpi:
            key = dpi + '!' + sel
        if key and key in tree_css_cache:
            return tree_css_cache[key]

        rv = node.css(sel)
        if key:
            tree_css_cache[key] = rv
        return rv

    return cached_tree_css


