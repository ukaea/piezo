from enum import Enum


class StatusCodes(Enum):
    Not_found = 404
    Unauthorised = 401
    Unautheticated = 403
    Bad_request = 400
    Okay = 200
