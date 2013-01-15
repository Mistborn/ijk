# -*- encoding: utf-8 -*-
import re
import datetime
from decimal import Decimal
from collections import OrderedDict

from django.contrib.flatpages.models import FlatPage
from django.utils.safestring import mark_safe

KOMENCA_DATO = datetime.date(2013, 8, 19)
FINIGHA_DATO = datetime.date(2013, 8, 26)

SEKSOJ = (
    ('v', u"♂ vira"),
    ('i', u"♀ ina"),
    ('a', u"☼ alia"),
)

_eod = {
 'c': u'ĉ', 'g': u'ĝ', 'h': u'ĥ', 'j': u'ĵ', 's': u'ŝ', 'u': u'ŭ', 'x': u'x',
 'C': u'Ĉ', 'G': u'Ĝ', 'H': u'Ĥ', 'J': u'Ĵ', 'S': u'Ŝ', 'U': u'Ŭ', 'X': u'X',
}

def eo(s):
    '''Konverti x-kodigitan ĉenon al unikodo'''
    #return s
    return unicode(re.sub(
        u'([cghjsuxCGHJSUX])[xX](?![xX])', lambda m: _eod[m.group(1)], s))

def json_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

MONATOJ = (u'januaro februaro marto aprilo majo junio '
           u'julio aŭgusto septembro oktobro novembro decembro'.split())
    
def esperanteca_dato(dato):
    jaro = dato.year
    monato = dato.month - 1
    tago = dato.day
    return 'la {}-a de {}, {}'.format(tago, MONATOJ[monato], jaro)


class Menu(object):
    def __init__(self):
        self.menu = OrderedDict() # mapping from parent url to Menu object
        self.mainpage = None
    @staticmethod
    def get_levels(url):
        if url == u'/':
            return []
        else:
            return url.strip('/').split('/')
    @staticmethod
    def get_label(url, title):
        return u'<a href="{}">{}</a>'.format(url, title)
    def addfp(self, item):
        self.add(item.url, item.title)
    def add(self, url, title):
        label = self.get_label(url, title)
        levels = self.get_levels(url)
        self.additem(label, levels)
    def additem(self, label, levels=None):
        if not levels:
            self.mainpage = label
        else:
            if levels[0] not in self.menu:
                self.menu[levels[0]] = Menu()
            self.menu[levels[0]].additem(label, levels[1:])
    def to_html(self, toplevel=True):
        label = self.mainpage if self.mainpage is not None else u''
        items = [self.menu[key].to_html(toplevel=False)
                    for key in self.menu]
        if toplevel:
            items = [label] + items
            label = u''
        if not items:
            return label
        items = u'<ul>{}</ul>'.format(u''.join(u'<li>{}</li>'.format(item)
                                               for item in items))
        return label + items

menu = Menu()
for fp in FlatPage.objects.order_by('pk'):
    menu.addfp(fp)
menu.add(u'/alighi/', u'Aliĝi!')
menu_html = menu.to_html()
def menu_context_processor(request):
    return {'MENUO': mark_safe(menu_html)}

