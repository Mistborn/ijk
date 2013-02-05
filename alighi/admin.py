from django.contrib import admin
import reversion
from alighi.models import *

# inline additions to User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
#from alighi.models import Respondeco, Pago, Noto

class UserRespondecoInline(admin.TabularInline):
    model = Respondeco
    extra = 0
    #can_delete = False
    #verbose_name_plural = 'profile'
class UserPagoInline(admin.TabularInline):
    model = Pago
    fk_name = 'respondeculo'
    extra = 0
class UserNotoInline(admin.TabularInline):
    model = Noto
    extra = 0

class NewUserAdmin(UserAdmin, reversion.VersionAdmin):
    inlines = (UserRespondecoInline, UserNotoInline, UserPagoInline)

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)

# inlines
class ProgramKotizoInline(admin.TabularInline):
    model = ProgramKotizo
    extra = 0
class ChambroInline(admin.TabularInline):
    model = Chambro
    extra = 0
class LandoInline(admin.TabularInline):
    model = Lando
    extra = 0
class UEARabatoInline(admin.TabularInline):
    model = UEARabato
    extra = 0
class SurlokaMembrighoInline(admin.TabularInline):
    model = SurlokaMembrigho
    extra = 0
class PagoInline(admin.TabularInline):
    model = Pago
    extra = 0
class NotoInline(admin.TabularInline):
    model = Noto
    extra = 0
class KurzoInline(admin.TabularInline):
    model = Kurzo
    extra = 0
class SenditaRetposhtajhoInline(admin.TabularInline):
    model = SenditaRetposhtajho
    extra = 0
class OficialajhoInline(admin.TabularInline):
    model = SenditaOficialajho
    extra = 0

class RespondecoAdmin(reversion.VersionAdmin):
    #fields = (('rolo', 'uzanto'),)
    list_display = ('rolo', 'uzanto')
    list_editable = ('uzanto',)
    #save_as = True
    list_filter = ('rolo', 'uzanto')

class ValutoAdmin(reversion.VersionAdmin):
    #fields = (('kodo', 'nomo'),)
    list_display = ('kodo', 'nomo')
    list_editable = ('nomo',)
    search_fields = ('nomo',)
    inlines = (KurzoInline,)
    
class KurzoAdmin(reversion.VersionAdmin):
    list_display = ('valuto', 'dato', 'kurzo')
    list_editable = ('dato', 'kurzo')
    list_filter = ('valuto', 'dato')
    
class AghKategorioAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'limagho', 'aldona_kotizo')
    list_editable = ('priskribo', 'limagho', 'aldona_kotizo')
    search_fields = ('nomo', 'priskribo')
    inlines = (ProgramKotizoInline,)

class AlighKategorioAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'limdato')
    list_editable = ('priskribo', 'limdato')
    search_fields = ('nomo', 'priskribo')
    inlines = (ProgramKotizoInline,)

class LandoKategorioAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo')
    list_editable = ('priskribo',)
    search_fields = ('nomo', 'priskribo')
    inlines = (LandoInline, ProgramKotizoInline, UEARabatoInline)

class LandoAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'kodo', 'kategorio')
    list_editable = ('kategorio',)
    list_filter = ('kategorio',)
    search_fields = ('nomo',)

class LoghKategorioAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'plena_kosto', 'unutaga_kosto')
    list_editable = list_display[1:]
    search_fields = ('nomo', 'priskribo')
    inlines = (ChambroInline,)

class ManghoMendoTipoAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'kosto')
    list_editable = list_display[1:]
    search_fields = ('nomo', 'priskribo')

#class ManghoMendoAdmin(reversion.VersionAdmin):
    #list_display = ('partoprenanto', 'tipo')
    ##list_editable = list_display[1:]
    #list_filter = list_display

class ManghoTipoAdmin(reversion.VersionAdmin):
    #def model_unicode(self, obj):
        #return unicode(obj)
    #model_unicode.short_description = 'Ero'
    #list_display = ('model_unicode', 'nomo')
    #list_display_links = ('model_unicode',)
    #list_editable = list_display[1:]
    pass

class ProgramKotizoAdmin(reversion.VersionAdmin):
    fields = (('aghkategorio', 'landokategorio', 'alighkategorio'), 'kotizo')
    list_display = ('aghkategorio', 'landokategorio',
                    'alighkategorio', 'kotizo')
    list_display_links = fields[0]
    list_editable = ('kotizo',)
    list_filter = ('aghkategorio', 'landokategorio', 'alighkategorio')

class PagmanieroAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'komenta_etikedo',
                    'chu_publika', 'chu_nurisraela')
    list_editable = list_display[1:]
    list_filter = ('chu_publika', 'chu_nurisraela')
    search_fields = ('nomo', 'priskribo', 'komenta_etikedo')

class RetposhtajhoAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'sendadreso', 'temo', 'teksto')
    list_editable = list_display[1:]
    list_filter = ('sendadreso',)
    search_fields = ('nomo', 'temo', 'teksto')

class MembrighaKategorioAdmin(reversion.VersionAdmin):
    search_fields = ('nomo',)
    inlines = (SurlokaMembrighoInline,)

class SurlokaMembrighoAdmin(reversion.VersionAdmin):
    list_display = ('partoprenanto', 'kategorio', 'kotizo', 'valuto')
    #list_editable = list_display[1:]
    list_filter = ('partoprenanto', 'kategorio', 'kotizo', 'valuto')

class ChambroAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'litonombro', 'loghkategorio', 'rimarko')
    list_editable = list_display[1:]
    list_filter = ('litonombro', 'loghkategorio',)
    search_fields = ('nomo',)

class PartoprenantoAdmin(reversion.VersionAdmin):
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
            'chambro',),
        ('manghotipo', 'manghomendoj'),
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
        'manghomendoj', 'manghotipo', 'antaupagos_ghis', 'pagmaniero',
        'chu_ueamembro',
        'chu_kontrolita',
        'unua_konfirmilo_sendita', 'dua_konfirmilo_sendita',
        'alighdato', 'malalighdato',
        'chu_alvenis', 'chu_havasmanghkuponon', 'chu_havasnomshildon',)
    search_fields = ('persona_nomo', 'familia_nomo', 'shildnomo',
        'retposhtadreso', 'adreso', 'urbo', 'loghlando__nomo', 'shildlando',
        'skype', 'facebook', 'mesaghiloj', 'alveno', 'foriro',
        'programa_kontribuo', 'organiza_kontribuo',
        'deziras_loghi_kun_nomo',
        'deziras_loghi_kun__persona_nomo',
        'deziras_loghi_kun__familia_nomo',
        'pagmaniera_komento', 'uea_kodo',)
    inlines = (PagoInline, NotoInline, OficialajhoInline)
        #SenditaRetposhtajhoInline)

class PagtipoAdmin(reversion.VersionAdmin):
    search_fields = ('nomo',)

class PagoAdmin(reversion.VersionAdmin):
    list_display = ('partoprenanto', 'respondeculo', 'pagmaniero',
                    'pagtipo', 'valuto', 'sumo', 'dato', 'rimarko',)
    readonly_fields = ('kreinto', 'lasta_redaktanto')
    list_editable = ('respondeculo', 'pagmaniero', 'pagtipo', 'valuto',
                     'rimarko',)
    list_filter = ('partoprenanto', 'respondeculo', 'kreinto',
                   'lasta_redaktanto', 'pagmaniero',
                   'pagtipo', 'valuto', 'dato')
    search_fields = ('rimarko',)
    def save_model(self, request, obj, form, change):
        if not change and not obj.kreinto:
            obj.kreinto = request.user
        obj.lasta_redaktanto = request.user
        super(PagoAdmin, self).save_model(request, obj, form, change)

class MinimumaAntaupagoAdmin(reversion.VersionAdmin):
    list_display = ('landokategorio', 'oficiala_antaupago')
    list_editable = list_display[1:]
    list_filter = ('landokategorio',)

class KrompagTipoAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'sumo')
    list_editable = list_display[1:]
    search_fields = ('nomo',)

class NomshildoAdmin(reversion.VersionAdmin):
    list_display = ('nomo', 'titolo_lokalingve', 'titolo_esperante',
                    'chu_havasnomshildon')
    list_editable = list_display[1:]
    list_filter = ('chu_havasnomshildon',)
    search_fields = list_display[:-1]

class NotoAdmin(reversion.VersionAdmin):
    list_display = ('partoprenanto', 'uzanto', 'dato', 'enhavo',
                    'chu_prilaborita', 'revidu')
    list_editable = ('uzanto', 'chu_prilaborita', 'revidu')
    list_filter = ('partoprenanto', 'uzanto', 'dato', 'chu_prilaborita',
                   'revidu')
    search_fields = ('enhavo',)

class UEARabatoAdmin(reversion.VersionAdmin):
    list_display = ('landokategorio', 'sumo',)
    list_editable = list_display[1:]
    list_filter = ('landokategorio',)

class SenditaRetposhtajhoAdmin(reversion.VersionAdmin):
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
    search_fields = ('temo', 'teksto')
    def has_add_permission(self, request): return False
    #def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
    actions = None

class SenditaOficialajhoAdmin(reversion.VersionAdmin):
    #readonly_fields = ('alshutinto',)
    list_display = ('priskribo', 'dosiero', 'partoprenanto', 'alshutinto')
    list_filter = ('partoprenanto', 'alshutinto')
    search_fields = ('priskribo', 'dosiero__name')
    actions = None
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('alshutinto',)
        return ('dosiero', 'alshutinto')

    def has_delete_permission(self, request, obj=None): return False
        
    def save_model(self, request, obj, form, change):
        if not change and not obj.alshutinto:
            obj.alshutinto = request.user
        super(SenditaOficialajhoAdmin, self).save_model(
                request, obj, form, change)
    
#class UEAValidecoAdmin(admin.ModelAdmin):
    #readonly_fields = ('kodo', 'lando', 'rezulto')
#admin.site.register(UEAValideco, UEAValidecoAdmin)

admin.site.register(Respondeco, RespondecoAdmin)
admin.site.register(Valuto, ValutoAdmin)
admin.site.register(Kurzo, KurzoAdmin)
admin.site.register(AghKategorio, AghKategorioAdmin)
admin.site.register(AlighKategorio, AlighKategorioAdmin)
admin.site.register(LandoKategorio, LandoKategorioAdmin)
admin.site.register(Lando, LandoAdmin)
admin.site.register(LoghKategorio, LoghKategorioAdmin)
admin.site.register(ManghoMendoTipo, ManghoMendoTipoAdmin)
#admin.site.register(ManghoMendo, ManghoMendoAdmin)
admin.site.register(ManghoTipo, ManghoTipoAdmin)
admin.site.register(ProgramKotizo, ProgramKotizoAdmin)
admin.site.register(Pagmaniero, PagmanieroAdmin)
admin.site.register(Retposhtajho, RetposhtajhoAdmin)
admin.site.register(MembrighaKategorio, MembrighaKategorioAdmin)
admin.site.register(SurlokaMembrigho, SurlokaMembrighoAdmin)
admin.site.register(Chambro, ChambroAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Pagtipo, PagtipoAdmin)
admin.site.register(MinimumaAntaupago, MinimumaAntaupagoAdmin)
admin.site.register(KrompagTipo, KrompagTipoAdmin)
admin.site.register(Nomshildo, NomshildoAdmin)
admin.site.register(Noto, NotoAdmin)
admin.site.register(UEARabato, UEARabatoAdmin)
admin.site.register(SenditaRetposhtajho, SenditaRetposhtajhoAdmin)
admin.site.register(Partoprenanto, PartoprenantoAdmin)
admin.site.register(SenditaOficialajho, SenditaOficialajhoAdmin)
