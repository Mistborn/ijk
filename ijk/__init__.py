# -*- encoding: utf-8 -*-

from collections import OrderedDict

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import fields
from django.utils.safestring import mark_safe

import reversion

# Rich text editor for flatpages
class EditorMedia:
    js = (
        'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
        '/static/js/editor.js',
    )
    css = {'all': ('/static/css/editor.css',)}

# Force flatpages to default to the current site, + revisions
from django.forms import ModelMultipleChoiceField
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages import admin as flatadmin, forms as flatforms
from django.contrib.sites.models import Site
from mptt.admin import MPTTModelAdmin, MPTTAdminForm

# add some fields to FlatPage
menu_title = fields.CharField(max_length=50,
    help_text=u'Etikedo por la navigada menuo (se alia ol la titolo)',
    verbose_name=u'Menua titolo', default=u'', blank=True)
menu_title.contribute_to_class(FlatPage, u'menu_title')

show_in_menu = fields.BooleanField(u'Ĉu montri en menuo',
    help_text=u'Ĉu tiu ĉi paĝo aperu en la reteja menuo',
    default=True)
show_in_menu.contribute_to_class(FlatPage, u'show_in_menu')

# create a key for ordering the menu
sort_key = fields.IntegerField(u'Ordiga sxlosilo',
    help_text=u'Ŝlosilo por ordigi menuerojn kun sama patro '
    u'unu rilate al la alia', blank=True, null=True)
sort_key.contribute_to_class(FlatPage, u'sort_key')

# MPTT for flat pages
import mptt
from mptt.fields import TreeForeignKey

# add a parent foreign key
TreeForeignKey(FlatPage, verbose_name='patro',
               help_text=u'Patra nodo, '
                    u'sub kiu tiu ĉi menuero aperos en la menuo',
               blank=True, null=True).contribute_to_class(FlatPage, 'parent')

mptt.register(FlatPage, order_insertion_by=[u'sort_key', u'url'])

class NewFlatpageForm(flatforms.FlatpageForm, MPTTAdminForm):
    sites = ModelMultipleChoiceField(queryset=Site.objects.all(),
        initial=[Site.objects.get_current()])

class NewFlatPageAdmin(flatadmin.FlatPageAdmin,
                       reversion.VersionAdmin,
                       MPTTModelAdmin):
    form = NewFlatpageForm
    fieldsets = (
        (None, {'fields':
            ('url', 'title', 'menu_title', 'show_in_menu',
             'content', 'parent', 'sort_key')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required',
         'template_name', 'sites')}),
    )

admin.site.unregister(FlatPage)
#admin.site.register(FlatPage, NewFlatPageAdmin, Media=EditorMedia)
admin.site.register(FlatPage, NewFlatPageAdmin, Media=EditorMedia)



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
