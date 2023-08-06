# -*- encoding: utf-8 -*-


def get_all(func, *args, **kwargs):
    kwargs['return_page_info'] = True
    rs, info = func(*args, **kwargs)
    for r in rs:
        yield r
    while info['start'] + info['count'] < info['total']:
        kwargs['start'] = info['start'] + info['count']
        rs, info = func(*args, **kwargs)
        for r in rs:
            yield r