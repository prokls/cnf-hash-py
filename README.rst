cnfhash-python3
===============

:author:        Lukas Prokop
:date:          August 2015
:version:       1.0.0
:license:       Public Domain

A python3 implementation to hash CNF/DIMACS files.

DIMACS file assumptions
-----------------------

A DIMACS file is valid iff

1. it is encoded as ASCII file.
2. *Comment lines* start with "c". Every character until the next newline is discarded. Comment lines can be inserted at any line position.
3. *Header lines* start with "p cnf " followed by two whitespace-separated sequences of digits.
4. All remaining lines, called *clause lines*, only contain whitespace-separated integers. Except within integers, whitespace can be inserted anywhere in clause lines.
5. An integer is an optional sign followed by one nonzero digit and an arbitrary number of digits.
6. Every clause line must be terminated with a whitespace followed by a zero and optionally following whitespace.
7. Every clause line contains at least one integer besides the zero terminator.

============== =========================================
**term**       **unicode mapping**
-------------- -----------------------------------------
"c"            U+0063
"p"            U+0070
"p cnf "       U+0070 U+0020 U+0063 U+006E U+0066 U+0020
sign           U+002D
nonzero digit  U+0031 – U+0039
digits         U+0030 – U+0039
whitespace     U+0020, U+000D, U+000A, U+0009
zero           U+0030
============== =========================================

Formal specification
--------------------

A valid DIMACS file is read in and a SHA1 instance is fed with bytes:

1. The first digit sequence of the header line is written.
2. A zero value is written.
3. The second digit sequence of the header line is written.
4. Two zero values are written.
5. For every clause line

   1. For every digit sequence with optional sign, excluding the terminating zero

      1. Write this signed integer
      2. Write a zero value

   2. Write a zero value

All the mentioned values are encoded as byte sequence where the integer parameter is represented as signed big-endian 64bit value.
If the value is negative, the two's complement has to be applied to retrieve the negative byte array representation of an absolute value.
If the value exceeds 2^63-1 or underflows -2^63, the integer can be extended to the smallest possible signed big-endian representation such that the number of bytes is a multiple of 8.

This implementation ensures that all valid DIMACS files are read correctly.
It might parse more files and compute the corresponding hash value.

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
    1 -4 -6 0
    % cnfhash.py test.cnf
    4d886cd3c4c90b97385e8b6459fbc96a037e8b22  test.cnf
    %

Cheers!
