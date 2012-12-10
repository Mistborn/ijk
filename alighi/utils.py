# -*- encoding: utf-8 -*-
import re
import datetime

KOMENCA_DATO = datetime.date(2013, 8, 19)
FINIGHA_DATO = datetime.date(2013, 8, 26)

SEKSOJ = (
    ('v', 'vira'),
    ('i', 'ina'),
    ('a', 'alia'),
)

_eod = {
 'c': u'ĉ', 'g': u'ĝ', 'h': u'ĥ', 'j': u'ĵ', 's': u'ŝ', 'u': u'ŭ', 'x': u'x',
 'C': u'Ĉ', 'G': u'Ĝ', 'H': u'Ĥ', 'J': u'Ĵ', 'S': u'Ŝ', 'U': u'Ŭ', 'X': u'X',
}

def eo(s):
    '''Konverti x-kodigitan stringon al unikodo'''
    #return s
    return unicode(re.sub(
        u'([cghjsuxCGHJSUX])[xX](?![xX])', lambda m: _eod[m.group(1)], s))
