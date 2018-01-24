#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sunfish import tools
from engines import legal
import numpy as np


piecetypes = 'PNBRQKpnbrqk'

def vrepr(pos):
    """
    encode pos.board into an array of 12 bit boards for piecetypes:

    >>> assert len(piecetypes) == 12
    >>> assert piecetypes[:6] == piecetypes[6:].upper()

    * An example of the game opening

      >>> p0 = tools.parseFEN(tools.FEN_INITIAL)
      >>> "".join(p0.board.split()) == (
      ... 'rnbqkbnr'
      ... 'pppppppp'
      ... '........'
      ... '........'
      ... '........'
      ... '........'
      ... 'PPPPPPPP'
      ... 'RNBQKBNR' )
      True

      >>> v0 = vrepr(p0)
      >>> assert len(v0) == 12
      >>> assert all(map((64).__eq__,(map(len,v0))))
      >>> assert all(map(np.dtype(bool).__eq__,map(np.result_type,v0)))

      >>> assert all(np.packbits(v0) == np.array([
      ...   0,   0,   0,   0,   0,   0, 255,   0, # P
      ...   0,   0,   0,   0,   0,   0,   0,  66, # N
      ...   0,   0,   0,   0,   0,   0,   0,  36, # B
      ...   0,   0,   0,   0,   0,   0,   0, 129, # R
      ...   0,   0,   0,   0,   0,   0,   0,  16, # Q
      ...   0,   0,   0,   0,   0,   0,   0,   8, # K
      ...   0, 255,   0,   0,   0,   0,   0,   0, # p
      ...  66,   0,   0,   0,   0,   0,   0,   0, # n
      ...  36,   0,   0,   0,   0,   0,   0,   0, # b
      ... 129,   0,   0,   0,   0,   0,   0,   0, # r
      ...  16,   0,   0,   0,   0,   0,   0,   0, # q
      ...   8,   0,   0,   0,   0,   0,   0,   0, # k
      ... ]))

    * An example white checkmate!

      >>> p1 = tools.parseFEN('7k/6Q1/5K2/8/8/8/8/8 b - - 0 1')
      >>> "".join(p1.rotate().board.split()) == ( # un-rotating for black
      ... '.......k'
      ... '......Q.'
      ... '.....K..'
      ... '........'
      ... '........'
      ... '........'
      ... '........'
      ... '........' )
      True

      >>> v1 = vrepr(p1)
      >>> assert all(np.packbits(v1) == np.array([
      ... 0, 0, 0, 0, 0, 0, 0, 0, # P
      ... 0, 0, 0, 0, 0, 0, 0, 0, # N
      ... 0, 0, 0, 0, 0, 0, 0, 0, # B
      ... 0, 0, 0, 0, 0, 0, 0, 0, # R
      ... 0, 2, 0, 0, 0, 0, 0, 0, # Q
      ... 0, 0, 4, 0, 0, 0, 0, 0, # K
      ... 0, 0, 0, 0, 0, 0, 0, 0, # p
      ... 0, 0, 0, 0, 0, 0, 0, 0, # n
      ... 0, 0, 0, 0, 0, 0, 0, 0, # b
      ... 0, 0, 0, 0, 0, 0, 0, 0, # r
      ... 0, 0, 0, 0, 0, 0, 0, 0, # q
      ... 1, 0, 0, 0, 0, 0, 0, 0, # k
      ... ]))

    """

    if pos.board.startswith("\n"): # is black
        pos = pos.rotate() # un-rotate to the  conventional orientation
    squares = np.array(tuple("".join(pos.board.split()))) # strip
    return [(squares == piece) for piece in piecetypes]

if __name__ == '__main__':

    import doctest
    print(doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    scripts = doctest.script_from_examples(vrepr.__doc__) # exec(scripts)
