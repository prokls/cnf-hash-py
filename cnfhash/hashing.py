#!/usr/bin/env python3

"""
    cnfhash.hashing
    ---------------

    Integer hashing library for cnfhash.

    (C) Lukas Prokop, 2015, Public Domain
"""

import _io
import logging
import hashlib
import functools

zero_bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00'


def bytes_repr(v: bytearray) -> str:
    """Represent a byte array in a Go-like style.

    :param bytearray v:     A byte array to represent
    :return str:            String representation
    """
    return '[' + ' '.join([str(c) for c in v]) + ']'


def bytes_count(integer: int) -> int:
    """How many bytes shall be used to represent integer?

    :param int integer:     An integer to represent
    :return int:            Number of bytes
    """
    # -2^63 .. 2^63-1  => 8 bytes
    # -2^64 .. 2^64-1  => 16 bytes
    # -2^127 .. 2^127-1  => 16 bytes
    b = 1 + (integer.bit_length() // 8)
    return b + (-b % 8)


def integers(f):
    """Decorator for a function yielding integers.
    I will replace the generated values with a return value
    which is a hash value for all those integers.
    """
    @functools.wraps(f)
    def inner(fp: _io.TextIOWrapper, log=None, *args, **kwargs):
        if not log:
            log = logging.getLogger("silent")
            log.setLevel(logging.ERROR)

        sha1 = hashlib.sha1()
        for integer in f(fp, log):
            log.info("Hashing {}".format(integer))
            if integer == 0:
                log.debug(bytes_repr(zero_bytes))
                sha1.update(zero_bytes)
            else:
                count = bytes_count(integer)
                byted = integer.to_bytes(count, byteorder='big', signed=True)
                log.debug(bytes_repr(byted))
                log.debug(bytes_repr(zero_bytes))
                sha1.update(byted)
                sha1.update(zero_bytes)

        return sha1.hexdigest()
    return inner
