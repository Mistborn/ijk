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
    def add(self, item):
        if item.url == u'/':
            levels = []
        else:
            levels = item.url.strip('/').split('/')
        self.additem(item, levels)
    def additem(self, item, parent=None):
        print 'adding {}, parent {}'.format(item, parent)
        if not parent:
            self.mainpage = item
        else:
            if parent[0] not in self.menu:
                self.menu[parent[0]] = Menu()
            self.menu[parent[0]].additem(item, parent[1:])
    def to_html(self, toplevel=True):
        if self.mainpage is None:
            label = u''
        else:
            label = u'<a href="{}">{}</a>'.format(self.mainpage.url,
                                                  self.mainpage.title)
        items = [self.menu[key].to_html(toplevel=False)
                    for key in self.menu]
        if toplevel:
            items = [label] + items
            label = u''
        if not items:
            return label
        items = u'<ul{}>{}</ul>'.format(
            u' class="menuo"' if toplevel else u'',
            u''.join(u'<li>{}</li>'.format(item)
                        for item in items))
        return label + items

menu = Menu()
for fp in FlatPage.objects.order_by('pk'):
    menu.add(fp)
menu_html = menu.to_html()
def menu_context_processor(request):
    return {'MENUO': mark_safe(menu_html)}

