def merge_dicts(base, updates=None):
    if updates is None:
        updates = {}
    result = base.copy()
    result.update(updates)
    return result
