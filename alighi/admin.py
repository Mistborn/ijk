from django.contrib import admin

from alighi.models import *

admin.site.register(Respondeco)
admin.site.register(Valuto)
admin.site.register(Kurzo)
admin.site.register(AghKategorio)
admin.site.register(AlighKategorio)
admin.site.register(LandoKategorio)
class LandoAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'kodo', 'kategorio')
admin.site.register(Lando, LandoAdmin)
admin.site.register(LoghKategorio)
admin.site.register(ManghoMendoTipo)
admin.site.register(ManghoMendo)
admin.site.register(ManghoTipo)
admin.site.register(ProgramKotizo)
admin.site.register(Pagmaniero)
admin.site.register(Retposhtajho)
admin.site.register(MembrighaKategorio)
admin.site.register(SurlokaMembrigho)
admin.site.register(Chambro)
class PartoprenantoAdmin(admin.ModelAdmin):
    '''Unuopa partoprenanto en la kongreso'''
    readonly_fields = ('alighdato',)
admin.site.register(Partoprenanto, PartoprenantoAdmin)
admin.site.register(Pago)
admin.site.register(Pagtipo)
admin.site.register(MinimumaAntaupago)
admin.site.register(Nomshildo)
admin.site.register(Noto)
admin.site.register(UEARabato)
