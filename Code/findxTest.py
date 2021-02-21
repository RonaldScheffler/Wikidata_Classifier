# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 16:30:33 2018

@author: Ronald Scheffler
"""

def findx(string, char, n):
    # Wenn Char in String enthalten
    if string.__contains__(char):
        # Splitte String an Character
        new = string.split(char, n)
        # Finde Position
        # new[-1] gibt letzten Teilstring (Rest) zurück
        posx = len(string) - len(new[-1]) - len(char)
        # Rückgabe
        return posx
    # Wenn Char nicht in String enthalten
    else:
        return 999


hastype = '/* wbtestaction-add:doh */'
notype = '/* wbtestaction:doh */'
protect = 'Protected'

print(findx(notype, ' ', 1))
print(findx(notype, '-', 1))
print(findx(notype, ':', 1))
print(findx(notype, 'wb', 1))
print(notype[findx(hastype, ' ' , 1)+1:findx(notype, '-' , 1)])
print(findx(protect, 'Protected', 1))