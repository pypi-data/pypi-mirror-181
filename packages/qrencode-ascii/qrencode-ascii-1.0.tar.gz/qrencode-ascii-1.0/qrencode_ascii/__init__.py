import sys
import os
import tempfile

from . import _qrencode

if sys.version_info >= (3,):
    unicode = str
    basestring = (str, bytes)

QR_ECLEVEL_L = 0
QR_ECLEVEL_M = 1
QR_ECLEVEL_Q = 2
QR_ECLEVEL_H = 3
levels = [QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q, QR_ECLEVEL_H]


QR_MODE_8 = 2
QR_MODE_KANJI = 3
hints = [QR_MODE_8, QR_MODE_KANJI]


def encode(data, version=0, level=QR_ECLEVEL_L, hint=QR_MODE_8,
           case_sensitive=True):
    """Creates a QR-Code from string data.

    Args:
      data: string: The data to encode in a QR-code. If a unicode string is
          supplied, it will be encoded in UTF-8. Raw bytes are also supported.
      version: int: The minimum version to use. If set to 0, the library picks
          the smallest version that the data fits in.
      level: int: Error correction level. Defaults to 'L'.
      hint: int: The type of data to encode. Either QR_MODE_8 or QR_MODE_KANJI.
      case_sensitive: bool: Should string data be encoded case-preserving?
    Returns:
       ASCII QR-code
    """


    if isinstance(data, unicode):
        data = data.encode('utf8')
    elif not isinstance(data, basestring):
        raise ValueError('data argument must be a string or bytes.')
    if not data:
        raise ValueError('data argument cannot be empty.')
    version = int(version)
    if level not in levels:
        raise ValueError('Invalid error-correction level.')
    if hint not in hints:
        raise ValueError('Invalid encoding mode.')

    fd, name = tempfile.mkstemp()
    try:
        _qrencode.encode(data, fd, version, level, hint, case_sensitive)
    except (ValueError, TypeError):
        _qrencode.encode_bytes(data, fd, version, level)

    with open(name) as f:
        output = f.read()

    os.remove(name)

    if not output:
        raise ValueError('Error generating QR-Code.')

    return output
