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
class LoghKategorioAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'plena_kosto', 'unutaga_kosto')
admin.site.register(LoghKategorio, LoghKategorioAdmin)
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
    readonly_fields = ('id', 'alighdato',)
admin.site.register(Partoprenanto, PartoprenantoAdmin)
admin.site.register(Pago)
admin.site.register(Pagtipo)
admin.site.register(MinimumaAntaupago)
admin.site.register(KrompagTipo)
admin.site.register(Nomshildo)
admin.site.register(Noto)
admin.site.register(UEARabato)

#class UEAValidecoAdmin(admin.ModelAdmin):
    #readonly_fields = ('kodo', 'lando', 'rezulto')
#admin.site.register(UEAValideco, UEAValidecoAdmin)
