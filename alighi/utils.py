# -*- encoding: utf-8 -*-
import re
import datetime
from decimal import Decimal
KOMENCA_DATO = datetime.date(2013, 8, 19)
FINIGHA_DATO = datetime.date(2013, 8, 26)
PLEJFRUA_DATO = datetime.date(2013, 8, 16)
PLEJMALFRUA_DATO = datetime.date(2013, 8, 26)

MINIMUMA_ANTAUPAGO = 15

SEKSOJ = (
    ('v', u"♂ vira"),
    ('i', u"♀ ina"),
    ('a', u"☼ alia"),
)

_eod = {
 'c': u'ĉ', 'g': u'ĝ', 'h': u'ĥ', 'j': u'ĵ', 's': u'ŝ', 'u': u'ŭ', 'x': u'x',
 'C': u'Ĉ', 'G': u'Ĝ', 'H': u'Ĥ', 'J': u'Ĵ', 'S': u'Ŝ', 'U': u'Ŭ', 'X': u'X',
}

_eox = {val: (key + 'x') for (key, val) in _eod.items()}

def eo(s):
    u'''Konverti x-kodigitan ĉenon al unikodo'''
    #return s
    return unicode(re.sub(
        u'([cghjsuxCGHJSUX])[xX](?![xX])', lambda m: _eod[m.group(1)], s))

def x(s):
    u'Konverti unikodan ĉenon al x-kodigo'
    return re.sub(u'[ĉĝĥĵŝŭĈĜĤĴŜŬ]', lambda m: _eox[m.group(0)], s)

def json_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

MONATOJ = (u'januaro februaro marto aprilo majo junio '
           u'julio aŭgusto septembro oktobro novembro decembro'.split())

def esperanteca_dato(dato, jaro=True):
    jarstr = u', {}'.format(dato.year) if jaro else u''
    monato = dato.month - 1
    tago = dato.day
    return u'la {}-a de {}{}'.format(tago, MONATOJ[monato], jarstr)
