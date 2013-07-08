# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from dosiero.models import *
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import os.path

class DosieroAdmin(admin.ModelAdmin):
    def ligilo(self, dosiero):
        return mark_safe(u'<a href="{url}" target="_blank">{url}</a>'.format(
            url=dosiero.url))
    ligilo.allow_tags = True
    ligilo.short_description = _('Link')

    def antaurigardo(self, dosiero):
        ext = os.path.splitext(dosiero.dosiero.path)[1]
        if ext in ('.jpg', '.jpeg', '.gif', '.png'):
            return u'<img src="{}">'.format(dosiero.url)
        else:
            return _('Unknown file format')
    antaurigardo.allow_tags = True
    antaurigardo.short_description = _('Preview')

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('ligilo', 'antaurigardo')
        return ('dosiero', 'ligilo', 'antaurigardo')

    def get_list_display(self, request):
        return ('priskribo', 'ligilo',)

    def mass_delete(self, request, queryset):
        for item in queryset:
            item.delete()
    mass_delete.short_description = _('Delete selected')

    readonly_fields = ('ligilo', 'antaurigardo')
    fields = ('priskribo', 'dosiero', 'ligilo', 'antaurigardo')

    def get_actions(self, request):
        actions = super(DosieroAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    actions = ['mass_delete']

admin.site.register(Dosiero, DosieroAdmin)
