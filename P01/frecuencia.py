# -*- coding: utf-8 -*- 

from codecs import open

"""
These are some transformation arrays to understand properly the strings passed by.
If it's any vowel with accent or anything more exotic, it does have its proper
simple vowel (or consonant) relative.
"""
accents =    u'ÀÁÂÃÄÅàáâãäåÒÓÔÕÕÖØòóôõöøÈÉÊËèéêëðÇçÐÌÍÎÏìíîïÙÚÛÜùúûüÑñŠšŸÿýŽž'
accentsOut = u'AAAAAAaaaaaaOOOOOOOooooooEEEEeeeedCcDIIIIiiiiUUUUuuuuNnSsYyyZz'

"""
This is a string that stores all the characters to be filtered out when trying to
find the character frequency
"""
filter_chars = u'\n\rºª\\!|"@·#$~%€&¬/()=?\'¿¡[]*+{}<>,;:.-_1234567890 '

def make_plain(c):
    """
    A pretty simple function that transforms from exotic character or consonant to
    simple and borint vowel or consonant.
    """
    if accents.count(c) > 0:
        i = accents.index(c)
        return accentsOut[i]
    return c

def available_char_at(path):
    """
    A generator method to get each char of the file to be read.
    """
    with open(path, 'r', 'utf-8') as stream:
        lines = stream.readlines()
        for line in lines:
            for c in line:
                yield c

def frequency(path):
    """
    Main method that calculates the character frequency of a text.
    """
    d = {}
    for c in available_char_at(path):
        if not c in filter_chars:
            c = make_plain(c).lower()
            if not c in d:
                d[c] = 1
            else:
                d[c] += 1
    print d

if __name__ == '__main__':
    frequency('./data/asimov.txt')
