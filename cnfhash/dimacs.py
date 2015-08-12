#!/usr/bin/env python3

"""
    cnfhash.dimacs
    --------------

    Read a DIMACS file and hash all integers.

    (C) Lukas Prokop, 2015, Public Domain
"""

import _io
import logging

from . import hashing


@hashing.integers
def read_dimacs_file(fp: _io.TextIOWrapper, log: logging.Logger):
    """Parse a DIMACS file and yield all numbers which in turn get hashed.

    :param fp:      A file descriptor to read from
    :param log:     A logger to write messages to
    :return:        A hash value for the DIMACS file
    """
    lineno = 0
    state = 0

    for line in fp:
        parts = line.split()
        lineno += 1

        if line[0] == 'c' and parts[0] == 'c':
            continue

        elif len(parts) == 0:
            continue

        # there are strange DIMACS files out there
        elif len(parts) == 1 and parts[0] == '%':
            return

        elif state == 0:
            msg = 'Expected valid DIMACS header at line {}'
            assert parts[0].lower() == 'p', msg.format(lineno)

            msg = 'DIMACS header line should have value "cnf" as second element at line {}'
            assert parts[1].lower() == 'cnf', msg.format(lineno)

            msg = 'DIMACS header line should have 4 values at line {}'
            assert len(parts) == 4, msg.format(lineno)

            log.info("Header line found at line {}".format(lineno))
            state = 1

            yield int(parts[2])
            yield int(parts[3])
            yield 0

            continue

        else:
            msg = 'Expected header, unexpected clause at line {}'
            assert state > 0, msg.format(lineno)

            for part in parts:
                integer = int(part)
                yield integer

    if state != 1:
        raise ValueError('Empty DIMACS file, expected at least a header')
