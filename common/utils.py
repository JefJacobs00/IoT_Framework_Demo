def merge(a, b):
    if b == None: return a
    if type(a) is str:
        if a != b:
            return { 'a': a, 'b': b }
    else:
        for key in a:  #host ip
            if key in b: # host ip is first key in result
                if type(a[key]) is list:
                    for value in b[key]:
                        if value not in a[key]:
                            a[key].append(value)
                else:
                    a[key] = merge(a[key],b[key])

        for key in b:
            if key not in a:
                a[key] = b[key]

    return a

def convert_keys_to_int(d: dict):
    new_dict = {}
    for k, v in d.items():
        try:
            new_key = int(k)
        except ValueError:
            new_key = k
        if type(v) == dict:
            v = convert_keys_to_int(v)
        new_dict[new_key] = v
    return new_dict

def find_in_dict(d:dict, key):
    if isinstance(d, str): return None
    if key in d: return d[key]
    for k in d:
        if type(k) is dict:
            find_in_dict(k, key)
        if type(d) is dict:
            res = find_in_dict(d[k], key)
            if not res == None: return res
    return None

def rm_fields(d, unwanted_keys:list):
    # remove empty fields plus any unwanted keys
    if isinstance(d, dict):
        return {
            k:v for k, v in ((k, rm_fields(v,unwanted_keys)) for k, v in d.items()) if v and k not in unwanted_keys
        }
    if isinstance(d, list):
        return [v for v in map(rm_fields, d, unwanted_keys) if v]
    return d

def recursive_lookup(k, d:dict):
    if isinstance(d, str): return None
    if k in d: return d[k]
    if isinstance(d, dict):
        for v in d.values():
            if isinstance(v, dict):
                a = recursive_lookup(k, v)
                if a is not None: return a
    return None