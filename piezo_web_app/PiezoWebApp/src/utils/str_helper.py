def is_str_empty(string):
    if string is None:
        return True
    return string.strip() == ""


def str2non_negative_int(string):
    integer = int(string)
    if integer < 0:
        raise ValueError("'{}' is not a non-negative integer".format(string))
    return integer
