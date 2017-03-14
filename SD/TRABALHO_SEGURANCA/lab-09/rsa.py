#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Util import number

def genRSAkey(p,q):
    n = p*q                        # modulus; goes in public key
    e = 65537L                     # public key exponent, standard value
    phi = (p-1)*(q-1)
    d = number.inverse(e,phi)    # private key exponent
    #return RSA.construct((n,e,d,p,q,None))
    return RSA.construct((n,e,d,p,q))

n1 = long(open('rsa_n1.txt').read())
n2 = long(open('rsa_n2.txt').read())
msg = [line.strip().decode('hex') for line in open('rsa_conversation.txt')]

# Your solution here!

# parte 1 RSA

p = number.GCD(n1, n2)
q1 = n1 / p
q2 = n2 / p

# parte 2 RSA

person_1 = genRSAkey(p,q1)
person_2 = genRSAkey(p,q2)

print(person_1.decrypt(msg[0]))
print(person_2.decrypt(msg[1]))
print(person_1.decrypt(msg[2]))
print(person_2.decrypt(msg[3]))
print(person_1.decrypt(msg[4]))
