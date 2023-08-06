from urllib.parse import urljoin as urljoin_raw

def urljoin(base, extra):
    if extra:
        if extra.startswith('https://') or extra.startswith('http://'):
            return extra

        return urljoin_raw(base, extra)


