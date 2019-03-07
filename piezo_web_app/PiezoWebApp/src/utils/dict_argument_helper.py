def get_set_difference(first, second):
    return list(set(first) - set(second))


def set_value_in_nested_dict(nested_dict, path, value):
    current_dict = nested_dict
    for i in range(len(path) - 1):
        if path[i] not in current_dict:
            current_dict[path[i]] = {}
        current_dict = current_dict[path[i]]
    current_dict[path[len(path) - 1]] = value
    return nested_dict
