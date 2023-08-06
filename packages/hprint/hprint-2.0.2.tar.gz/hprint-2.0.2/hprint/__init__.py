from functools import partial
from tabulate import tabulate
import json
from pprint import pformat
import os
import traceback

_print = partial(print, flush=True)

HPRINT_WRAP = os.getenv("HPRINT_WRAP", 50)

HPRINT_DEBUG = os.getenv("HPRINT_DEBUG")


__all__ = ['pretty_print', 'hprint']


def _pprint(obj):
    _print(pformat(obj, indent=4))


def json_print(data):
    if isinstance(data, dict):
        _print(json.dumps(data, indent=4, sort_keys=True))
    elif isinstance(data, list):
        try:
            _print(json.dumps([dict(d) for d in data], indent=4, sort_keys=True))
        except Exception:
            _pprint([dict(d) for d in data])
    else:
        _pprint(data)


def _chain_get(data, chain, default=None):
    attrs = chain.split('.')
    if len(attrs) == 1:
        return data.get(attrs[0], default)
    result = data
    for attr in attrs[:-1]:
        result = result.get(attr, {})
    return result.get(attrs[-1], default)


def _get(obj, key, default='n/a'):
    if not key:
        return obj
    return _chain_get(obj, key, default)


def tabulate_numbered_print(data, mappings, offset=0):
    if not data:
        return
    if not mappings:
        mappings = {k: k for k in data[0]}
    mappings = {'No': '_no', **mappings}
    headers = mappings.keys()
    tabdata = []
    for idx, item in enumerate(data, start=1 + offset):
        attrs = []
        item['_no'] = idx
        for h in headers:
            k = mappings[h]
            if isinstance(k, tuple):
                (k0, func) = k
                attrs.append(func(_get(item, k0)))
            else:
                attrs.append(_get(item, k))
        tabdata.append(attrs)
    _print(tabulate(tabdata, headers=headers))


def _len(x):
    return min(len(str(x)), HPRINT_WRAP)


def x_print(records, headers, offset=0, header=True):
    headers = list(headers)
    left_max_len = max(len(max(headers, key=len)), len(f"-[ RECORD {len(records)} ]-")) + 1
    right_max_len = max(_len(max(record, key=_len)) for record in records) + 1
    for i, record in enumerate(records, 1 + offset):
        if header:
            _print(f'-[ RECORD {i} ]'.ljust(left_max_len, '-') + '+' + '-' * right_max_len)
        for j, v in enumerate(record):
            _print(f'{headers[j]}'.ljust(left_max_len) + '| ' + str(v).ljust(right_max_len))


def tabulate_print(data, mappings, x=False, offset=0, header=True, raw=False, tf='simple'):
    if not data:
        return
    if not mappings:
        keys = set()
        for entry in data:
            keys = keys.union(entry.keys())
        mappings = {k: k for k in keys}
        # entry_with_most_keys = max(data, key=len)
        # mappings = {k: k for k in entry_with_most_keys.keys()}
    headers = mappings.keys()
    tabdata = []
    for item in data:
        attrs = []
        for h in headers:
            k = mappings[h]
            if isinstance(k, tuple):
                (k0, func) = k
                attrs.append(func(_get(item, k0)))
            else:
                attrs.append(_get(item, k))
        tabdata.append(attrs)
    if x:
        x_print(tabdata, headers, offset=offset, header=header)
    else:
        output = tabulate(tabdata, headers=headers if header else (), tablefmt=tf)
        if raw:
            return output
        _print(output)


def hprint(data, *, mappings=None, json_format=False, as_json=False, x=False, offset=0, numbered=False, missing_value='n/a', tf='simple', header=True, raw=False):
    as_json = as_json or json_format
    if not data:
        return
    global _get
    _get0 = _get
    _get = partial(_get, default=missing_value)
    try:
        if as_json:
            json_print(data)
        elif not x and numbered:
            tabulate_numbered_print(data, mappings, offset=offset)
        else:
            return tabulate_print(data, mappings=mappings, x=x, offset=offset, header=header, raw=raw, tf=tf)
    except Exception:
        if HPRINT_DEBUG:
            traceback.print_exc()

        json_print(data)
    finally:
        _get = _get0


pretty_print = hprint
