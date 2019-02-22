def get_set_difference(a, b):
    return list(set(a) - set(b))


def set_value_in_nested_dict(nested_dict, path, value):
    current_dict = nested_dict
    for i in range(len(path) - 1):
        current_dict = current_dict[path[i]]
    current_dict[path[len(path) - 1]] = value
    return nested_dict
