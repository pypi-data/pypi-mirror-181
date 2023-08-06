
def without_keys(d, *keys):
    return dict(filter(lambda key_value: key_value[0] not in keys, d.items()))

