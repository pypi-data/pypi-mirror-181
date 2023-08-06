'''Implements low-level json pointer parsing. See `RFC 6901 Section 4
<https://www.rfc-editor.org/rfc/rfc6901#section-4>`_ for the specification that this
parser adheres to.
'''

import re
from typing import *

from .exceptions import ParseException

RE_INVALID_ESCAPE = re.compile("(~[^01]|~$)")


def validate(pointer: str) -> None:
    '''Validate that a string is a well formed json pointer.
    
    :raises: :exc:`.ParseException`: If json pointer is invalid.

    >>> validate('') # empty string is fine, means "whole json object"
    >>> validate('foo') # parts must lead with '/'
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...
    >>> validate('/foo~') # ~ is the escape char, can't be solo
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...
    >>> validate('/~2/foo') # only ~0, ~1 are valid escapes
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...
    '''
    
    if len(pointer) > 0 and not pointer.startswith("/"):
        raise ParseException("JSON pointers must be empty or start with '/'")

    if match := RE_INVALID_ESCAPE.search(pointer):
        raise ParseException("Found invalid escape {}".format(match.group()))


def parse(pointer: str) -> list[str]:
    r'''Parse a json pointer into a list of unescaped path parts.

    :raises: :exc:`.ParseException`: If json pointer is invalid.

    >>> parse('') # empty string is "the whole json object"
    []
    >>> parse('/') # keys can be zero-length strings
    ['']
    >>> parse('/ //  ') # which can look funky
    [' ', '', '  ']
    >>> parse('/foo/m~0n/a~1b') # ~1 escapes /, ~0 escapes ~
    ['foo', 'm~n', 'a/b']
    >>> parse('/c%d/e^f') # funky symbols are fine too!
    ['c%d', 'e^f']
    >>> parse(r'/i\\j/g|h/k\l') # r-string avoids escaping backslashes
    ['i\\\\j', 'g|h', 'k\\l']
    '''
    validate(pointer)

    parts = pointer.split("/")
    # discard "empty" str, as "/foo/bar".split() becomes ["", "foo", "bar"]
    parts.pop(0) 
    return [unescape(p) for p in parts]


def unparse(parts: Iterable[str]) -> str:
    r'''Combine an iterable of unescaped path parts into a json pointer.
    
    >>> unparse([])
    ''
    >>> unparse([''])
    '/'
    >>> unparse([' ', '', '  '])
    '/ //  '
    >>> unparse(['foo', 'm~n', 'a/b'])
    '/foo/m~0n/a~1b'
    >>> unparse(['c%d', 'e^f'])
    '/c%d/e^f'
    >>> unparse([r'i\\j', 'g|h', r'k\l'])
    '/i\\\\j/g|h/k\\l'
    '''
    return "".join('/' + escape(part) for part in parts)


def escape(part: str) -> str:
    '''Escape a path part.
    
    >>> escape("foo")
    'foo'
    >>> escape("m~/0")
    'm~0~10'
    '''
    # Escape `~` first! https://www.rfc-editor.org/rfc/rfc6901#section-4
    return part.replace("~", "~0").replace("/", "~1")


def unescape(part: str) -> str:
    '''Unescape a path part.
    
    >>> unescape("foo")
    'foo'
    >>> unescape("m~0~10")
    'm~/0'
    '''
    # Unscape `~` last! https://www.rfc-editor.org/rfc/rfc6901#section-4
    return part.replace("~1", "/").replace("~0", "~")
