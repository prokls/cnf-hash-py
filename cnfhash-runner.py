#!/usr/bin/env python3

"""
    cnfhash.py
    ==========

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

import sys
from cnfhash.run import main


if __name__ == '__main__':
    sys.exit(main())
