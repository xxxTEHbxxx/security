import sys
import numpy as np
import rm
import math

if __name__ == '__main__':
    # Validate the command-line parameters.
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s word [word [...]]\n' % (sys.argv[0],))
        sys.exit(1)

    file = open('secret_key_A.txt', 'r')
    A = [list(map(int, row.split())) for row in file.readlines()]
    A = np.array(A)
    A_reversed = (np.linalg.inv(A))
    file.close()

    file = open('secret_key_G.txt', 'r')
    G = [list(map(int, row.split())) for row in file.readlines()]
    G = np.array(G)
    file.close

    file = open('secret_key_P.txt', 'r')
    P = [list(map(int, row.split())) for row in file.readlines()]
    P = np.array(P)
    P_reversed = np.linalg.inv(P)
    file.close

    file = open('open_key_mistakes.txt','r')
    mistakes = file.read(1)
    file.close()

    #print(E)
    #print(G.shape[0])
    n = G.shape[0]
    k = G.shape[1]
    m = math.log2(n)
    m = int(m)
    r = m - 1 - math.log2(int(mistakes)+1)
    r = int(r)
    # Now iterate over the words to encode, validate them, and encode them.

    rm = rm.ReedMuller(r,m)

    for word in sys.argv[1:]:
            listword = list(map(int,word))
            if (not set(listword).issubset([0,1])) or (len(listword) != n):
                sys.stderr.write('FAIL: word %s is not a 0-1 string of length %d\n' % (word, n))
            else:
                np_word = np.array(listword)
                b = np_word@P_reversed
                s =''
                for i in b:
                    s+=str(int(i))
                b_new = list(map(int,s))
                #print(A_reversed)
                #print(b_new)
                a = np.array(rm.decode(b_new))
                #print(len(a))
                decodedword = (a.dot(A_reversed))%2
                #print(decodedword)
                strg =''
                for i in decodedword:
                    strg+=str(int(i))
                print(strg)
                #print(''.join(map(str,decodedword)))
                #print(b)
