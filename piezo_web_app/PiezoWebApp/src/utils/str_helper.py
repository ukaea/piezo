def is_str_empty(string):
    if string is None:
        return True
    return string.strip() == ""


def str2bool(string):
    lower_str = string.lower()
    if lower_str == "true":
        return True
    if lower_str == "false":
        return False
    raise ValueError("'{}' not recognised as a Boolean. Use 'True' or 'False' (case insensitive)." .format(string))



def str2non_negative_int(string):
    integer = int(string)
    if integer < 0:
        raise ValueError("'{}' is not a non-negative integer".format(string))
    return integer
