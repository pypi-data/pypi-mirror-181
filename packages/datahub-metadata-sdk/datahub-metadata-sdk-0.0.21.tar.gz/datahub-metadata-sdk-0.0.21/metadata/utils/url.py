# -*- encoding: utf-8 -*-

import urllib.parse


def build_url(base, path, **args):
    url_parts = list(urllib.parse.urlparse(base))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args)
    return urllib.parse.urlunparse(url_parts)