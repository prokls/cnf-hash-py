#!/usr/bin/env python3

"""
    cnfhash.py
    ==========

    Script for executable module.

    Compute a hash value for the given DIMACS file.
    Requires Python >=3.2 for ``int.to_bytes``

    * Considers the two header values
    * Ignores comments
    * Order of clauses matters
    * Order of literals matter [0]_
    * A more formal specification is provided with the `Go implementation`_.

    .. [0]: Difficult decision, but we decided in favor of it
    .. _Go implementation: https://github.com/prokls/cnfhash-go

    (C) Lukas Prokop, 2015, Public Domain
"""

import logging
import os.path
import argparse

from . import dimacs


def run(args: argparse.Namespace, log: logging.Logger) -> int:
    for dimacsfile in args.dimacsfiles:
        filename = os.path.basename(dimacsfile)
        log.info("Start hash computation for {}".format(dimacsfile))
        with open(dimacsfile) as fp:
            hashvalue = dimacs.read_dimacs_file(fp, log)

        print('{:<40}  {}'.format(hashvalue, dimacsfile if args.fullpath else filename))
    return 0


def main():
    parser = argparse.ArgumentParser(description='CNF analysis')
    parser.add_argument('dimacsfiles', metavar='dimacsfiles', nargs='+',
                        help='filepath of DIMACS file')
    parser.add_argument('-f', '--fullpath', action='store_true',
                        help='the hash value will be followed by the filepath, not filename')
    parser.add_argument('-l', '--loglevel', choices={'error', 'debug', 'info'}, default='error',
                        help='filepath of DIMACS file')

    args = parser.parse_args()
    log = logging.getLogger('cnfhash')
    logging.basicConfig(
        format='%(name)s.%(levelname) 5s - %(message)s',
        level=logging.NOTSET
    )
    log.setLevel(getattr(logging, args.loglevel.upper()))

    return run(args, log)
