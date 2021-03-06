cnf-hash-py
===========

:author:        Lukas Prokop
:date:          August 2015, May 2016
:version:       2.1.2
:license:       CC-0

A python3 implementation to hash DIMACS CNF files.
See `the technical report <http://lukas-prokop.at/proj/megosat/downloads/cnf-hash.pdf>`_ for more details.
This implementation was pushed to `Python Package Index PyPI <https://pypi.python.org/pypi/cnfhash>`_.

How to use
----------

To install use pip3::

    pip3 install cnfhash

Then you can use the following API in python3::

    import cnfhash

    # reading blockwise from a DIMACS file

    def read_blockwise(filepath):
        with open(filepath) as fd:
            while True:
                buf = fd.read(4096)
                if len(buf) == 0:
                    break
                yield buf

    reader = read_blockwise('test.cnf')
    print(cnfhash.hash_dimacs(reader))

    # or use integers directly

    print(cnfhash.hash_cnf([3, 2, 1, -3, 0, -1, 2, 0]))

Testing the software
--------------------

Download `the testsuite <http://github.com/prokls/cnf-hash-tests1/>`_.
Provide the folder location as environment variable::

    export TESTSUITE="/home/prokls/Downloads/cnf-hash/tests1/"

Then run all files in the ``tests`` directory::

    python3 tests/test_testsuite.py

The testsuite has been run successfully, if the exit code has always been 0.

DIMACS file assumptions
-----------------------

A DIMACS file is valid iff

1. Any line starting with "c" or consisting only of whitespace is considered as *comment line* and content is not interpreted until the next newline character occurs.
2. The remaining file is a sequence of whitespace separated values.

   1. The first value is required to be "p"
   2. The second value is required to be "cnf"
   3. The third value is required to be a non-negative integer and called *nbvars*.
   4. The fourth value is required to be a non-negative integer and called *nbclauses*.
   5. The remaining non-zero integers are called *lits*.
   6. The remaining zero integers are called *clause terminators*.

3. A DIMACS file must be terminated by a clause terminator.
4. Every lit must satisfy ``-nbvars ≤ lit ≤ nbvars``.
5. The number of clause terminators must equate nbclauses.

============== =========================================
**term**       **ASCII mapping**
-------------- -----------------------------------------
"c"            U+0063
"p"            U+0070
"cnf"          U+0063 U+006E U+0066 U+0020
sign           U+002D
nonzero digit  U+0031 – U+0039
digits         U+0030 – U+0039
whitespace     U+0020, U+000D, U+000A, U+0009
zero           U+0030
============== =========================================

Formal specification
--------------------

A valid DIMACS file is read in and a SHA1 instance is fed with bytes:

1. The first four values are dropped.
2. Lits are treated as integers without leading zeros. Integers are submitted as base 10 ASCII digits with an optional leading sign to the SHA1 instance.
3. Clause terminators are submitted as zero character followed by a newline character to the SHA1 instance.

Performance and memory
----------------------

The DIMACS parser uses OS' page size as default block size.
A few constant values and the python runtime is also stored in memory.
So for a python program, this implementation is very memory-friendly.

The technical report shows that 45 DIMACS files summing up to 1 GB memory
can be read in 2989 seconds. In terms of performance, the equivalent `Go
implementation <http://github.com/prokls/cnf-hash-go/>`_ is recommended.

Example
-------

::

    % cat test.cnf
    p cnf 5 6
    1 2 3 0
    2 3 -4 0
    1 -2 0
    -1 2 0
    1 3 5 0
    1 -4 -5 0
    % cnf-hash-py test.cnf
    cnf-hash-py 2.1.2 2016-05-29T12:27:13.991260 /root
    cnf2$776d81a0c805104e265667917b22ffefe9f39433  test.cnf
    %

Cheers!
