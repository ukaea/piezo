from enum import Enum


class ArgumentClassification(Enum):
    Fixed = 1
    Required = 2
    Optional = 3
    Conditional = 4
