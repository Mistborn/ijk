# -*- encoding: utf-8 -*-
import re

_eod = {
 'c': u'ĉ', 'g': u'ĝ', 'h': u'ĥ', 'j': u'ĵ', 's': u'ŝ', 'u': u'ŭ', 'x': u'x',
 'C': u'Ĉ', 'G': u'Ĝ', 'H': u'Ĥ', 'J': u'Ĵ', 'S': u'Ŝ', 'U': u'Ŭ', 'X': u'X',
}

def eo(s):
    '''Konverti x-kodigitan stringon al unikodo'''
    # XXX this should be somewhere else
    #return s
    return re.sub(
        r'([cghjsuxCGHJSUX])[xX](?![xX])', lambda m: _eod[m.group(1)], s)
