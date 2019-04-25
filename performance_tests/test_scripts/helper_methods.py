import datetime


def average_timedelta(list_of_timedeltas):
    return sum(list_of_timedeltas, datetime.timedelta(0)) / len(list_of_timedeltas)
