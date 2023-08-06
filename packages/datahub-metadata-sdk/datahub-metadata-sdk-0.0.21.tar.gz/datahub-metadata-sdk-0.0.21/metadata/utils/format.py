# -*- coding: utf-8 -*-

import json
import yaml
from collections import defaultdict


def format_table(headers, properties, show_headers=True):
    import pandas as pd
    pd.set_option('display.max_colwidth', 0)
    pd.set_option("display.max_rows", len(properties))

    if not properties:
        return

    df = pd.DataFrame(properties, columns=headers)
    return df.to_string(na_rep='None', index=False, header=show_headers)

def json2yaml(data):
    data = json.loads(data)
    text = yaml.safe_dump(data, default_flow_style=False, allow_unicode=True)
    return text

def yaml2json(data):
    data = yaml.safe_load(data)
    text = json.dumps(data, ensure_ascii=False)
    return text

def dict2yaml(dt):
    return json2yaml(json.dumps(dt))

def dict2json(dt):
    return json.dumps(dt, ensure_ascii=False, indent=4)

def gen_tree_files(paths):
    def to_desired(node, name=''):
        result = {'name': name}
        if node:
           children = [
              to_desired(value, key)
              for key, value in node.items()
           ]
           result['children'] = children
        return result

    def build_dynamic_trees(list_of_folders):
       tree = lambda: defaultdict(tree)
       root = tree()
       for folders in list_of_folders:
          dynamic_keys = ''
          for folder_name in folders.split("/"):
             if not folder_name:
                continue
             dynamic_keys += "['{}']".format(folder_name)
          exec('root' + dynamic_keys + ' = None')
       return root

    return to_desired(build_dynamic_trees(paths))['children']

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"