from django.contrib import admin

from alighi.models import *

class RespondecoAdmin(admin.ModelAdmin):
    #fields = (('rolo', 'uzanto'),)
    list_display = ('rolo', 'uzanto')
    list_editable = ('uzanto',)
    #save_as = True
    list_filter = ('rolo', 'uzanto')
admin.site.register(Respondeco, RespondecoAdmin)

class ValutoAdmin(admin.ModelAdmin):
    #fields = (('kodo', 'nomo'),)
    list_display = ('kodo', 'nomo')
    list_editable = ('nomo',)
admin.site.register(Valuto, ValutoAdmin)

class KurzoAdmin(admin.ModelAdmin):
    list_display = ('valuto', 'dato', 'kurzo')
    list_editable = ('dato', 'kurzo')
    list_filter = ('valuto',)
admin.site.register(Kurzo, KurzoAdmin)

class AghKategorioAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'priskribo', 'limagho', 'aldona_kotizo')
    list_editable = ('priskribo', 'limagho', 'aldona_kotizo')
admin.site.register(AghKategorio, AghKategorioAdmin)

class AlighKategorioAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'priskribo', 'limdato')
    list_editable = ('priskribo', 'limdato')
admin.site.register(AlighKategorio, AlighKategorioAdmin)

class LandoKategorioAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'priskribo')
    list_editable = ('priskribo',)
admin.site.register(LandoKategorio, LandoKategorioAdmin)

class LandoAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'kodo', 'kategorio')
    list_editable = ('kategorio',)
    list_filter = ('kategorio',)
admin.site.register(Lando, LandoAdmin)

class LoghKategorioAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'priskribo', 'plena_kosto', 'unutaga_kosto')
    list_editable = list_display[1:]
admin.site.register(LoghKategorio, LoghKategorioAdmin)

class ManghoMendoTipoAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'priskribo', 'kosto')
    list_editable = list_display[1:]
admin.site.register(ManghoMendoTipo, ManghoMendoTipoAdmin)

class ManghoMendoAdmin(admin.ModelAdmin):
    list_display = ('partoprenanto', 'tipo')
    #list_editable = list_display[1:]
    list_filter = list_display
admin.site.register(ManghoMendo, ManghoMendoAdmin)

class ManghoTipoAdmin(admin.ModelAdmin):
    #def model_unicode(self, obj):
        #return unicode(obj)
    #model_unicode.short_description = 'Ero'
    #list_display = ('model_unicode', 'nomo')
    #list_display_links = ('model_unicode',)
    #list_editable = list_display[1:]
    pass
admin.site.register(ManghoTipo, ManghoTipoAdmin)

class ProgramKotizoAdmin(admin.ModelAdmin):
    fields = (('aghkategorio', 'landokategorio', 'alighkategorio'), 'kotizo')
    list_display = ('aghkategorio', 'landokategorio',
                    'alighkategorio', 'kotizo')
    list_display_links = fields[0]
    list_editable = ('kotizo',)
    list_filter = ('aghkategorio', 'landokategorio', 'alighkategorio')
admin.site.register(ProgramKotizo, ProgramKotizoAdmin)

class PagmanieroAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'priskribo', 'komenta_etikedo',
                    'chu_publika', 'chu_nurisraela')
    list_editable = list_display[1:]
    list_filter = ('chu_publika', 'chu_nurisraela')
admin.site.register(Pagmaniero, PagmanieroAdmin)

class RetposhtajhoAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'sendadreso', 'temo', 'teksto')
    list_editable = list_display[1:]
    list_filter = ('sendadreso',)
admin.site.register(Retposhtajho, RetposhtajhoAdmin)

class MembrighaKategorioAdmin(admin.ModelAdmin):
    pass
admin.site.register(MembrighaKategorio, MembrighaKategorioAdmin)

class SurlokaMembrighoAdmin(admin.ModelAdmin):
    list_display = ('partoprenanto', 'kategorio', 'kotizo', 'valuto')
    #list_editable = list_display[1:]
    list_filter = ('partoprenanto', 'kategorio', 'kotizo', 'valuto')
admin.site.register(SurlokaMembrigho, SurlokaMembrighoAdmin)

class ChambroAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'litonombro', 'loghkategorio', 'rimarko')
    list_editable = list_display[1:]
    list_filter = ('litonombro', 'loghkategorio',)
admin.site.register(Chambro, ChambroAdmin)

class PartoprenantoAdmin(admin.ModelAdmin):
    '''Unuopa partoprenanto en la kongreso'''
    fields = (
        ('persona_nomo', 'familia_nomo', 'shildnomo',),
        ('sekso', 'naskighdato', 'retposhtadreso'),
        ('adreso', 'urbo', 'poshtkodo', 'loghlando', 'shildlando',), ('chu_bezonas_invitleteron', 'chu_invitletero_sendita',),
        ('telefono', 'skype', 'facebook', 'mesaghiloj',),
        ('chu_retalisto', 'chu_postkongresalisto',),
        ('ekde', 'ghis'),
        ('alveno', 'foriro'),
        ('interesighas_pri_antaukongreso', 'interesighas_pri_postkongreso',
            'chu_tuttaga_ekskurso', 'chu_unua_dua_ijk', 'chu_komencanto', 'chu_interesighas_pri_kurso',),
        'programa_kontribuo', 'organiza_kontribuo',
        ('loghkategorio', 'deziras_loghi_kun_nomo', 'deziras_loghi_kun',),
        ('chu_preferas_unuseksan_chambron', 'chu_malnoktemulo',
            'chambro', 'manghotipo',),
        ('antaupagos_ghis', 'pagmaniero', 'pagmaniera_komento',),
        ('chu_ueamembro', 'uea_kodo',),
        'chu_kontrolita',
        ('unua_konfirmilo_sendita', 'dua_konfirmilo_sendita'),
        ('alighdato', 'malalighdato'),
        ('chu_alvenis', 'chu_havasmanghkuponon', 'chu_havasnomshildon',)
    )
    readonly_fields = ('id', 'alighdato',)
    list_display = ('persona_nomo', 'familia_nomo', 'loghlando', 'chambro')
    list_editable = ('loghlando', 'chambro')
    list_display_links = ('persona_nomo', 'familia_nomo')
    list_filter = ('sekso', 'naskighdato', 'loghlando',
        'chu_bezonas_invitleteron', 'chu_invitletero_sendita',
        'chu_retalisto', 'chu_postkongresalisto', 'ekde', 'ghis',
        'interesighas_pri_antaukongreso', 'interesighas_pri_postkongreso',
        'chu_tuttaga_ekskurso', 'chu_unua_dua_ijk', 'chu_komencanto',
        'chu_interesighas_pri_kurso', 'loghkategorio',
        'chu_preferas_unuseksan_chambron', 'chu_malnoktemulo', 'chambro',
        'manghotipo', 'antaupagos_ghis', 'pagmaniero',
        'chu_ueamembro',
        'chu_kontrolita',
        'unua_konfirmilo_sendita', 'dua_konfirmilo_sendita',
        'alighdato', 'malalighdato',
        'chu_alvenis', 'chu_havasmanghkuponon', 'chu_havasnomshildon',)
admin.site.register(Partoprenanto, PartoprenantoAdmin)

class PagoAdmin(admin.ModelAdmin):
    list_display = ('partoprenanto', 'respondeculo', 'pagmaniero',
                    'pagtipo', 'valuto', 'sumo', 'dato', 'rimarko',)
    readonly_fields = ('kreinto',)
    list_editable = ('respondeculo', 'pagmaniero', 'pagtipo', 'valuto',
                     'rimarko',)
    list_filter = ('partoprenanto', 'respondeculo', 'kreinto', 'pagmaniero',
                   'pagtipo', 'valuto')
    def save_model(self, request, obj, form, change):
        if not change and not obj.kreinto:
            obj.kreinto = request.user
        super(PagoAdmin, self).save_model(request, obj, form, change)
admin.site.register(Pago, PagoAdmin)

class PagtipoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Pagtipo, PagtipoAdmin)

class MinimumaAntaupagoAdmin(admin.ModelAdmin):
    list_display = ('landokategorio', 'oficiala_antaupago')
    list_editable = list_display[1:]
    list_filter = ('landokategorio',)
admin.site.register(MinimumaAntaupago, MinimumaAntaupagoAdmin)

class KrompagTipoAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'sumo')
    list_editable = list_display[1:]
admin.site.register(KrompagTipo, KrompagTipoAdmin)

class NomshildoAdmin(admin.ModelAdmin):
    list_display = ('nomo', 'titolo_lokalingve', 'titolo_esperante',
                    'chu_havasnomshildon')
    list_editable = list_display[1:]
    list_filter = ('chu_havasnomshildon',)
admin.site.register(Nomshildo, NomshildoAdmin)

class NotoAdmin(admin.ModelAdmin):
    list_display = ('partoprenanto', 'uzanto', 'dato', 'enhavo',
                    'chu_prilaborita', 'revidu')
    list_editable = ('uzanto', 'chu_prilaborita', 'revidu')
    list_filter = ('partoprenanto', 'uzanto', 'chu_prilaborita',)
admin.site.register(Noto, NotoAdmin)

class UEARabatoAdmin(admin.ModelAdmin):
    list_display = ('landokategorio', 'sumo',)
    list_editable = list_display[1:]
admin.site.register(UEARabato, UEARabatoAdmin)

class SenditaRetposhtajhoAdmin(admin.ModelAdmin):
    readonly_fields = (
        'temo',
        'teksto',
        'sendadreso',
        'ricevanto',
        'partoprenanto',
        'retposhtajho',
        'chu_sukcese',
        'dato',
    )
    list_display = readonly_fields
    list_filter = ('sendadreso', 'ricevanto', 'partoprenanto',
                   'retposhtajho', 'dato', 'temo',)
    def has_add_permission(self, request): return False
    #def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
    actions = None
admin.site.register(SenditaRetposhtajho, SenditaRetposhtajhoAdmin)

#class UEAValidecoAdmin(admin.ModelAdmin):
    #readonly_fields = ('kodo', 'lando', 'rezulto')
#admin.site.register(UEAValideco, UEAValidecoAdmin)
