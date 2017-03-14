#!/usr/bin/python

import dict
from Crypto.Cipher import ARC4

# main code
print '\n=== RC4 pay-per-view encryption service ==='
print 'Your secrets are relatively safe with us!'
print 'Today\'s rates: $0 per encryption, $5 per decryption'
key = dict.get_sentence()
cipher = ARC4.new(key)

msg = dict.get_sentence()
print '\nSample:\t\t' + cipher.encrypt(msg).encode('string_escape')

while (True):
    cipher = ARC4.new(key)
    msg = raw_input("\nYour secret:\t").decode('string_escape')
    print(key)
    print 'Our reference:\t' + cipher.encrypt(msg).encode('string_escape')
