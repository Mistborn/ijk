# -*- encoding: utf-8 -*-
from django.contrib import admin
from dosiero.models import *
import os.path

class DosieroAdmin(admin.ModelAdmin):
    def ligilo(self, dosiero):
        return mark_safe(u'<a href="{url}">{url}</a>'.format(url=dosiero.url))
    ligilo.allow_tags = True

    def antaurigardo(self, dosiero):
        ext = os.path.splitext(dosiero.dosiero.path)[1]
        if ext in ('.jpg', '.jpeg', '.gif', '.png'):
            return u'<img src="{}">'.format(dosiero.url)
        else:
            return u'Nekonata dosierformato'
    antaurigardo.allow_tags = True

    readonly_fields = ('ligilo', 'antaurigardo')
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('ligilo', 'antaurigardo')
        return ('dosiero', 'ligilo', 'antaurigardo')

    def get_list_display(self, request):
        return ('priskribo', 'ligilo',)
        
    fields = ('priskribo', 'dosiero', 'ligilo', 'antaurigardo')
    
admin.site.register(Dosiero, DosieroAdmin)
