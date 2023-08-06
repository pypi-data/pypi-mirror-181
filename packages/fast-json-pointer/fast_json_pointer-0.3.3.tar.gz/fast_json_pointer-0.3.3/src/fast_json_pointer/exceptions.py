class JsonPointerException(Exception):
    '''Generic json pointer failure.'''

class ParseException(JsonPointerException):
    '''Failure occurred while parsing a json pointer.'''