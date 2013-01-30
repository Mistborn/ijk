# -*- encoding: utf-8 -*-
from django.contrib import admin
from dosiero.models import *

class DosieroAdmin(admin.ModelAdmin):
    def ligilo(self, dosiero):
        return mark_safe(u'<a href="{url}">{url}</a>'.format(url=dosiero.url))
    ligilo.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return ('dosiero', 'ligilo',)

    def get_list_display(self, request):
        return ('priskribo', 'ligilo',)
        
    list_fields = ('priskribo', 'dosiero', 'ligilo',)
    
admin.site.register(Dosiero, DosieroAdmin)
