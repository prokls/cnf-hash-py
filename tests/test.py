#!/usr/bin/env python3

"""
    cnfhash.test
    ------------

    Testsuite for the python3 implementation of CNF hashing.

    Provide the folder to the testsuite either as environment
    variable TESTSUITE, as second command line parameter or
    'testsuite' is taken.

    'testsuite' is a folder with CNF files with their hash value
    in their name like `cnfhash-test <https://github.com/prokls/cnfhash-tests>`_.

    (C) Lukas Prokop, 2015, Public Domain
"""

import sys
import os.path
import unittest

import cnfhash.dimacs


class CnfHashingTestsuite(unittest.TestCase):
    def test_testsuite(self):
        testsuite = sys.argv[1] if len(sys.argv) > 1 else 'testsuite'
        testsuite = dict(os.environ).get('TESTSUITE', testsuite)

        for filename in os.listdir(testsuite):
            if os.path.isdir(os.path.join(testsuite, filename)):
                continue

            filepath = os.path.join(testsuite, filename)
            hashvalue = filename.split('_')[0]

            with open(filepath) as fp:
                comp_hashvalue = cnfhash.dimacs.read_dimacs_file(fp)

            self.assertEqual(hashvalue, comp_hashvalue, filename[len(hashvalue) + 1:])


if __name__ == '__main__':
    unittest.main()
