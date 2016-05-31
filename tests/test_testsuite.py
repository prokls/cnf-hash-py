#!/usr/bin/env python3

"""
    cnfhash.test
    ------------

    Testsuite for the python3 implementation of CNF hashing.

    Provide the folder to the testsuite either as environment
    variable TESTSUITE, as second command line parameter or
    'testsuite' is taken.

    'testsuite' is a folder with CNF files with their hash value
    in their name like `cnf-hash-test <https://github.com/prokls/cnf-hash-tests>`_.

    (C) Lukas Prokop, 2016, Public Domain
"""

import sys
import os.path
import unittest

import cnfhash


class CnfHashingTestsuite(unittest.TestCase):
    def test_testsuite(self):
        testsuite = sys.argv[1] if len(sys.argv) > 1 else 'testsuite'
        testsuite = dict(os.environ).get('TESTSUITE', testsuite)

        for filename in os.listdir(testsuite):
            if not filename.endswith('.cnf'):
                continue
            if os.path.isdir(os.path.join(testsuite, filename)):
                continue

            filepath = os.path.join(testsuite, filename)
            hashvalue = filename.split('_')[0]

            with open(filepath, 'rb') as fd:
                try:
                    comp_hashvalue = cnfhash.hash_dimacs(fd)
                    assert comp_hashvalue[0:5] == 'cnf2$'
                except Exception as e:
                    print('Failure while processing testcase {}'.format(filepath), file=sys.stderr)
                    raise e

            self.assertEqual(hashvalue, comp_hashvalue[5:], filename[len(hashvalue) + 1:])


if __name__ == '__main__':
    unittest.main()
