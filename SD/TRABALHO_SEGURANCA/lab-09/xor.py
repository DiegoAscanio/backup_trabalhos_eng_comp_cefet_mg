#!/usr/bin/python

import dict
import random

# encryption function: XOR
def encrypt(msg, key):
    result = ''
    for i in range (0,len(msg)):
        result += chr(ord(msg[i]) ^ ord(key[i%len(key)]))
    return result

# main code
print '\n=== XOR pay-per-view encryption service ==='
print 'Your secrets are moderately safe with us!'
print 'Today\'s rates: $0 per encryption, $1 per decryption'

key = dict.get_sentence()
msg = dict.get_sentence()
print(msg,  key)

print(msg[0:3])
print(key[0:3])

print([ord(msg[i]) for i in range (0,3)])

print '\nExample:\t' + msg
print 'Our reference:\t' + encrypt(msg,key).encode('string_escape')

while (True):
    msg = raw_input("\nYour secret:\t").decode('string_escape')
    print 'Our reference:\t' + encrypt(msg,key).encode('string_escape')
