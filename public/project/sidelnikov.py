import numpy as np
import rm
import sys
import re

def num_decimal_places(s):
    ls = s.split('.', 1)
    if len(ls) == 2 and re.match(r'\d*$', ls[1]):
        return len(ls[1].rstrip('0'))
    return 0

if __name__ == '__main__':
    # Validate the command-line parameters.
    if len(sys.argv) < 3:
        sys.stderr.write('Usage: %s r m\n' % (sys.argv[0],))
        sys.exit(1)

    r,m = list(map(int,sys.argv[1:3]))
    if (m <= r):
        sys.stderr.write('We require r < m.\n')
        sys.exit(2)

    # Create the code.
    rm = rm.ReedMuller(r,m)
    k = rm.message_length()

    #Generate matrix P
    n = rm.n
    P = np.eye(n)
    np.random.shuffle(P)


    #Generate matrix A
    def gen_A1(k):
        A = np.random.randint(0, 2, size = (k, k))
        det = np.linalg.det(A)
        while(det == 0):
            A = np.random.randint(0, 2, size = (k, k))
            det = np.linalg.det(A)
        return A
    def gen_A2(k):
        A_reversed = (np.zeros((k,k)))
        A_is_ok = False
        A = gen_A1(k)
        while(A_is_ok == False):
            A = gen_A1(k)
            A_reversed = (np.linalg.inv(A))
            A_is_ok = True
            for i in range(k):
                for j in range(k):
                    st = str(A_reversed[i][j])
                    if(num_decimal_places(st)>0):
                        A_is_ok = False
            #a_r = float(st)
            #A_reversed[i][j] = a_r
        return A
    A = gen_A2(k)
    A_reversed = (np.linalg.inv(A))
    #print(A_reversed)


    #Remember that we have matrix G
    G = np.array(rm.M)
    #print(A)
    #print(G.shape)
    #print(P.shape)
    E = (A@G.T@P)%2
    mistakes = rm.strength()


    #Save open key (matrix E)
    #print(mistakes)
    #print(E)
    np.savetxt('open_key_E.txt', E, fmt = '%i')
    file = open('open_key_mistakes.txt','w')
    file.write(str(mistakes))
    file.close()

    #Save secret key (matrixes A, G, P)
    np.savetxt('secret_key_A.txt', A, fmt = '%i')
    np.savetxt('secret_key_G.txt', G, fmt = '%i')
    np.savetxt('secret_key_P.txt', P, fmt = '%i')

    #file = open('open_key_G.txt', 'r')
    #matrix = [list(map(float, row.split())) for row in file.readlines()]
    #matrix = np.array(matrix)
    #print(matrix[0])
    #print(E[0])
