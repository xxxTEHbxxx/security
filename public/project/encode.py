#!/usr/bin/env python
"""rmencode.py

By Sebastian Raaphorst, 2012.

Simple command-line application for Reed-Muller encoding of one or more 0-1 strings."""

import sys
import numpy as np

if __name__ == '__main__':
    # Validate the command-line parameters.
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s word [word [...]]\n' % (sys.argv[0],))
        sys.exit(1)

    file = open('open_key_E.txt', 'r')
    E = [list(map(int, row.split())) for row in file.readlines()]
    file.close()
    E = np.array(E)
    #print(E)
    #print(E.shape[0])
    k = E.shape[0]
    # Now iterate over the words to encode, validate them, and encode them.
    for word in sys.argv[1:]:
        try:
            listword = list(map(int,word))
            if (not set(listword).issubset([0,1])) or (len(listword) != k):
                sys.stderr.write('FAIL: word %s is not a 0-1 string of length %d\n' % (word, k))
            else:
                np_word = np.array(listword)
                encoded_word = (np_word@E)%2
                s =''
                for i in encoded_word:
                    s+=str(i)
                print(s)


        except:
            sys.stderr.write('FAIL: word %s is not a 0-1 string of length %d\n' % (word, k))
