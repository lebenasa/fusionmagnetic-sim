# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 23:40:13 2015

@author: leben

Some utility functions
"""

def exclude(string, exclude='#'):
    """Remove comment strings from string.
    Return a list of white-space separated strings
    
    Used to remove comments:
    >>> exclude("test # A Test\\n")
    ['test']
    >>> exclude("# some description\\n 123.0 51.0 # values")
    ['123.0', '51.0']
    >>> exclude("not a comment * a comment", '*')
    ['not', 'a', 'comment']
    >>> exclude(" # comment 1\\n value * comment 2", '#*')
    ['value']
    """
    lines = string.split('\n')
    res = []
    for line in lines:
        params = line.split()
        for p in params:
            if contains(p, exclude):
                break
            res.append(p)
    return res
    
def contains(string, exclude='#'):
    exc = tuple(exclude)
    for ch in exc:
        if string.find(ch) != -1:
            return True
    return False
    
def parsable(string, exclude='#'):
    """Check whether a string can safely parsed to number(s)
    >>> parsable(' 1.2 5.0')
    True
    >>> parsable('  ')
    False
    >>> parsable('')
    False
    >>> parsable('\\n')
    False
    """
    return string != '' and not contains(string, exclude) and not string.isspace()
    
formats = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'ULINE': '\033[4m'
    }
    
def passRange(value, minval, maxval=9.9E+300):
    """Check whether value is within permitted range.
    Will print warning if value doesn't comply.
    
    >>> passRange(1.0E-09, 0.0, 1.0)
    True
    >>> passRange(-5.0, 0.0)
    Value must be bigger than 0.0
    False
    >>> passRange(200.0, 0.0, 100.0)
    Value must be smaller than 100.0
    False
    """
    if value < minval:
        print "Value must be bigger than {minval}".format(minval=minval)
        return False
    if value > maxval:
        print "Value must be smaller than {maxval}".format(maxval=maxval)
        return False
    return True
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()