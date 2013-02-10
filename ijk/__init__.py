# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import fields
from django.db import DatabaseError
from django.utils.safestring import mark_safe
from django.conf import settings

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
sort_key = fields.IntegerField(u'Ordiga ŝlosilo',
    help_text=u'Ŝlosilo por ordigi menuerojn kun sama patro '
    u'unu rilate al la alia', blank=False, null=False, default=0)
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

# For some reason, FlatPage.tree is an ordinary manager, not a TreeManager
treemanager = mptt.managers.TreeManager()
treemanager._base_manager = None
treemanager.contribute_to_class(FlatPage, 'treemanager')

try:
    initial_site = [Site.objects.get_current()]
except DatabaseError:
    from django.db import connection
    connection._rollback()
    initial_site = []

class NewFlatpageForm(flatforms.FlatpageForm, MPTTAdminForm):
    sites = ModelMultipleChoiceField(queryset=Site.objects.all(),
        initial=initial_site)

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
admin.site.register(FlatPage, NewFlatPageAdmin, Media=EditorMedia)

from django.core.urlresolvers import reverse

_roots = FlatPage.treemanager.root_nodes()

def _mkmenu(node):
    '''Return a <li> that links to the item at node and
    includes a submenu of all its descendants'''
    sublist = [_mkmenu(child) for child in node.get_children()]
    return u'''<li><a href="{}">{}</a>{}</li>'''.format(
        node.get_absolute_url(),
        node.menu_title.strip() or node.title,
        u'<ul>{}</ul>'.format(u''.join(sublist)) if sublist else u'')

_menu = [_mkmenu(node) for node in _roots]
if not settings.HIDE_ALIGHILO:
    _menu.append(u'<li><a href="{}">Aliĝi!</a></li>'.format(reverse('alighi')))
menu_html = u'<ul>{}</ul>'.format(u''.join(_menu))

def menu_context_processor(request):
    return {'MENUO': mark_safe(menu_html)}

# Google Analytics
def ga_context_processor(request):
    d = {'GA': ''}
    if not settings.DEBUG:
        d['GA'] = mark_safe('''<script type="text/javascript">

            var _gaq = _gaq || [];
            _gaq.push(['_setAccount', 'UA-38382173-1']);
            _gaq.push(['_setDomainName', 'mesha.org']);
            _gaq.push(['_trackPageview']);

            (function() {
                var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
            })();

            \n</script>''')
    return d
    