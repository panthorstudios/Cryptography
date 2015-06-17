#!/usr/bin/env python 
from collections import Counter

def find_key_length(chars):
    """ 
    Return the Vigenere key length for a list of character values. 

    Keyword arguments:

    chars -- A list of the ASCII values of the characters
             in the string
    """
    sqvals=[]
    kval=-1
    klen=-1
    for kl in range(1,14):
        sublist=chars[::kl]
        sublen=len(sublist)
        dist=dict((k,float(v)/sublen) for k,v in Counter(sublist).most_common())
        distsum=sum(d**2 for d in dist.itervalues())
        if distsum>kval:
            kval=distsum
            klen=kl

    return klen


def find_keys(message):
    """
    Return a list of the Vigenere keys for an encoded string

    Keyword arguments:

    message -- A string representing a message that has been encoded 
               using the Vigenere cipher
    """

    ENGLISH_FREQ = {
        'A':0.08167, 'B':0.01492, 'C':0.02782, 'D':0.04253, 'E':0.12702,
        'F':0.02228, 'G':0.02015, 'H':0.06094, 'I':0.06966, 'J':0.00153,
        'K':0.00772, 'L':0.04025, 'M':0.02406, 'N':0.06749, 'O':0.07507,
        'P':0.01929, 'Q':0.00095, 'R':0.05987, 'S':0.06327, 'T':0.09056,
        'U':0.02758, 'V':0.00978, 'W':0.02360, 'X':0.00150, 'Y':0.01974,
        'Z':0.00074
    }
    chars=[]
    for i in range(0,len(message)//2):
        os=i*2
        chars.append(int(message[os:os+2],16))

    keylen=find_key_length(chars)

    keys=[]
    for kn in range(keylen):
        sublist=chars[kn::keylen]
        kval=-1
        kdig=-1


        for keyval in range(256):
            nlist=[x ^ keyval for x in sublist]

# Only check if all chars are in range 32..127
            if max(nlist)<128 and min(nlist)>31:

# take lowercase letters, i.e. ASCII 97-122
                lcletts=[x for x in nlist if x>=97 and x<=122]
                freqs=dict((k,float(v)/26.0) for k,v in Counter(lcletts).most_common())
                s=0.0
                for f in freqs:
                    ef=ENGLISH_FREQ[chr(f-32)]
                    s+=freqs[f]*ef

                if s>kval:
                    kval=s
                    kdig=keyval
        keys.append(kdig)
    return keys






def encode(message,keys):
    """ 
    Encode a message using a Vigenere cipher

    Keyword arguments:

    message -- The message to encode
    keys -- The keys to use for encoding

    """

    encoded=''
    message=message.replace('\n','')
    for i in range(len(message)):
        char=ord(message[i]) ^ keys[i%len(keys)]
        encoded += '%02X' % char
    return encoded


def decode(message,keys):
    """ 
    Decode a message using a Vigenere cipher

    Keyword arguments:
    
    message -- The message to encode
    keys -- The keys to use for encoding
    
    """
    decoded=''
    for i in range(0,len(message)//2):
        os=i*2
        v=int(message[os:os+2],16)
        char=chr(v ^ keys[i%len(keys)])
        decoded+=char

    return decoded

if __name__== '__main__':

    KEYS=[123,54,111,23,250,195,2,33,201]


    message="You don't know about me without you have read a book by the name of The Adventures of Tom Sawyer; but that ain't no matter.  That book was made by Mr. Mark Twain, and he told the truth, mainly.  There was things which he stretched, but mainly he told the truth.  That is nothing.  I never seen anybody but lied one time or another, without it was Aunt Polly, or the widow, or maybe Mary.  Aunt Polly-Tom's Aunt Polly, she is-and Mary, and the Widow Douglas is all told about in that book, which is mostly a true book, with some stretchers, as I said before."

# Encrypt the message
    encrypted=encode(message,KEYS)
    print encrypted

# Decrypt the message
    decrypted=decode(encrypted,KEYS)
    assert decrypted==message
    print decrypted

# Find the keys
    keys=find_keys(encrypted)
    assert keys == KEYS
    print keys
 
