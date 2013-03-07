# -*- encoding: utf-8 -*-
import urllib

from django.conf.urls import patterns, url
from django.contrib import admin
from annoying.functions import get_object_or_None
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import reversion
from alighi.models import *
from alighi.permissions import *

class ChambroAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'litonombro', 'loghkategorio', 'rimarko')
    list_editable = list_display[1:]
    list_filter = ('litonombro', 'loghkategorio',)
    search_fields = ('nomo',)
    def get_actions(self, request):
        actions = super(ChambroAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_chambro'):
            del actions['delete_selected']
        return actions
class ChambroInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = Chambro
    extra = 0

class RespondecoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    # fields = (('rolo', 'uzanto'),)
    list_display = ('rolo', 'uzanto')
    list_editable = ('uzanto',)
    # save_as = True
    list_filter = ('rolo', 'uzanto')
    def get_actions(self, request):
        actions = super(RespondecoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_respondeco'):
            del actions['delete_selected']
        return actions


class KurzoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('valuto', 'dato', 'kurzo')
    list_editable = ('dato', 'kurzo')
    list_filter = ('valuto', 'dato')
    def get_actions(self, request):
        actions = super(KurzoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_kurzo'):
            del actions['delete_selected']
        return actions
class KurzoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = Kurzo
    extra = 0

class ValutoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    # fields = (('kodo', 'nomo'),)
    list_display = ('kodo', 'nomo')
    list_editable = ('nomo',)
    search_fields = ('nomo',)
    inlines = (KurzoInline,)
    def get_actions(self, request):
        actions = super(ValutoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_valuto'):
            del actions['delete_selected']
        return actions

class ProgramKotizoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    fields = (('aghkategorio', 'landokategorio', 'alighkategorio'), 'kotizo')
    list_display = ('aghkategorio', 'landokategorio',
                    'alighkategorio', 'kotizo')
    list_display_links = fields[0]
    list_editable = ('kotizo',)
    list_filter = ('aghkategorio', 'landokategorio', 'alighkategorio')
    def get_actions(self, request):
        actions = super(ProgramKotizoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_programkotizo'):
            del actions['delete_selected']
        return actions
class ProgramKotizoInline(SpecialPermissionsAdmin, admin.TabularInline,):
    model = ProgramKotizo
    extra = 0

class AghKategorioAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'limagho', 'aldona_kotizo')
    list_editable = ('priskribo', 'limagho', 'aldona_kotizo')
    search_fields = ('nomo', 'priskribo')
    inlines = (ProgramKotizoInline,)
    def get_actions(self, request):
        actions = super(AghKategorioAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_aghkategorio'):
            del actions['delete_selected']
        return actions

class AlighKategorioAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'limdato')
    list_editable = ('priskribo', 'limdato')
    search_fields = ('nomo', 'priskribo')
    inlines = (ProgramKotizoInline,)
    def get_actions(self, request):
        actions = super(AlighKategorioAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_alighkategorio'):
            del actions['delete_selected']
        return actions

class LandoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'kodo', 'kategorio')
    list_editable = ('kategorio',)
    list_filter = ('kategorio',)
    search_fields = ('nomo',)
    def get_actions(self, request):
        actions = super(LandoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_lando'):
            del actions['delete_selected']
        return actions
class LandoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = Lando
    extra = 0

class UEARabatoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('landokategorio', 'sumo',)
    list_editable = list_display[1:]
    list_filter = ('landokategorio',)
    def get_actions(self, request):
        actions = super(UEARabatoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_uearabato'):
            del actions['delete_selected']
        return actions
class UEARabatoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = UEARabato
    extra = 0

class LandoKategorioAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo')
    list_editable = ('priskribo',)
    search_fields = ('nomo', 'priskribo')
    inlines = (ProgramKotizoInline, UEARabatoInline, LandoInline,)
    def get_actions(self, request):
        actions = super(LandoKategorioAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_landokategorio'):
            del actions['delete_selected']
        return actions

class LoghKategorioAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'plena_kosto', 'unutaga_kosto')
    list_editable = list_display[1:]
    search_fields = ('nomo', 'priskribo')
    inlines = (ChambroInline,)
    def get_actions(self, request):
        actions = super(LoghKategorioAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_loghkategorio'):
            del actions['delete_selected']
        return actions

class ManghoMendoTipoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'kosto')
    list_editable = list_display[1:]
    search_fields = ('nomo', 'priskribo')
    def get_actions(self, request):
        actions = super(ManghoMendoTipoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_manghomendotipo'):
            del actions['delete_selected']
        return actions

# class ManghoMendoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    # list_display = ('partoprenanto', 'tipo')
    # #list_editable = list_display[1:]
    # list_filter = list_display

class ManghoTipoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    # def model_unicode(self, obj):
        # return unicode(obj)
    # model_unicode.short_description = 'Ero'
    # list_display = ('model_unicode', 'nomo')
    # list_display_links = ('model_unicode',)
    # list_editable = list_display[1:]
    def get_actions(self, request):
        actions = super(ManghoTipoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_manghotipo'):
            del actions['delete_selected']
        return actions

class PagmanieroAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'priskribo', 'komenta_etikedo',
                    'chu_publika', 'chu_nurisraela')
    list_editable = list_display[1:]
    list_filter = ('chu_publika', 'chu_nurisraela')
    search_fields = ('nomo', 'priskribo', 'komenta_etikedo')
    def get_actions(self, request):
        actions = super(PagmanieroAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_pagmaniero'):
            del actions['delete_selected']
        return actions

class RetposhtajhoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'sendadreso', 'temo', 'teksto')
    list_editable = list_display[1:]
    list_filter = ('sendadreso',)
    search_fields = ('nomo', 'temo', 'teksto',)
    def get_actions(self, request):
        actions = super(RetposhtajhoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_retposhtajho'):
            del actions['delete_selected']
        return actions

class SurlokaMembrighoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('partoprenanto', 'kategorio', 'kotizo', 'valuto')
    # list_editable = list_display[1:]
    list_filter = ('kategorio', 'kotizo', 'valuto', 'partoprenanto',)
    def get_actions(self, request):
        actions = super(SurlokaMembrighoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_surlokamembrigho'):
            del actions['delete_selected']
        return actions
class SurlokaMembrighoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = SurlokaMembrigho
    extra = 0

class MembrighaKategorioAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    search_fields = ('nomo',)
    inlines = (SurlokaMembrighoInline,)
    def get_actions(self, request):
        actions = super(MembrighaKategorioAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_membrighakategorio'):
            del actions['delete_selected']
        return actions

class PagoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('partoprenanto', 'respondeculo', 'pagmaniero',
                    'pagtipo', 'valuto', 'sumo', 'dato', 'rimarko',)
    readonly_fields = ('kreinto', 'lasta_redaktanto')
    list_editable = ('respondeculo', 'pagmaniero', 'pagtipo', 'valuto',
                     'rimarko',)
    list_filter = ('partoprenanto', 'respondeculo', 'kreinto', 'lasta_redaktanto', 'pagmaniero',
                   'pagtipo', 'valuto', 'dato',)
    search_fields = ('rimarko',)
    def save_model(self, request, obj, form, change):
        if not change and not obj.kreinto:
            obj.kreinto = request.user
        obj.lasta_redaktanto = request.user
        super(PagoAdmin, self).save_model(request, obj, form, change)
    def get_actions(self, request):
        actions = super(PagoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_pago'):
            del actions['delete_selected']
        return actions
class PagoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = Pago
    extra = 0
    readonly_fields = PagoAdmin.readonly_fields + ('dato',
            'pagmaniero', 'pagtipo', 'valuto', 'sumo')
    fields = [f for f in PagoAdmin.list_display]  # if f != 'respondeculo']
    can_delete = False
    def has_add_permission(self, request): return False

class NotoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('partoprenanto', 'uzanto', 'dato', 'enhavo',
                    'chu_prilaborita', 'revidu')
    list_editable = ('uzanto', 'chu_prilaborita', 'revidu')
    list_filter = ('uzanto', 'dato', 'chu_prilaborita', 'revidu',
                   'partoprenanto',)
    search_fields = ('enhavo',)
    def get_actions(self, request):
        actions = super(NotoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_noto'):
            del actions['delete_selected']
        return actions
class NotoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = Noto
    extra = 0

class OficialajhoAdminBase(object):
    def elshuto(self, oficialajho):
        return u'<a href="{url}">{url}</a>'.format(
            url=oficialajho.dosiero.url)
    elshuto.allow_tags = True
    elshuto.short_description = u'elŝuto'
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('alshutinto', 'alshutodato', 'elshuto')
        return ('dosiero', 'alshutinto', 'alshutodato', 'elshuto')
    def has_delete_permission(self, request, obj=None): return False
    def save_model(self, request, obj, form, change):
        if not change and not obj.alshutinto:
            obj.alshutinto = request.user
        super(OficialajhoAdminBase, self).save_model(
                request, obj, form, change)
    def get_actions(self, request):
        actions = super(OficialajhoAdminBase, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_senditaoficialajho'):
            del actions['delete_selected']
        return actions

class SenditaOficialajhoAdmin(OficialajhoAdminBase,
                              SpecialPermissionsAdmin,
                              reversion.VersionAdmin):
    # readonly_fields = ('alshutinto',)
    list_display = ('priskribo', 'elshuto', 'partoprenanto',
        'alshutinto', 'alshutodato')
    list_filter = ('partoprenanto', 'alshutinto', 'alshutodato')
    search_fields = ('priskribo', 'dosiero__name')
    actions = None
    readonly_fields = ('alshutinto', 'alshutodato', 'elshuto',)
    fields = ('priskribo', 'dosiero', 'alshutinto', 'alshutodato', 'elshuto',
              'partoprenanto')
class OficialajhoInline(OficialajhoAdminBase,
                        SpecialPermissionsAdmin,
                        admin.TabularInline):
    extra = 0
    can_delete = False
    readonly_fields = SenditaOficialajhoAdmin.readonly_fields
    fields = [f for f in SenditaOficialajhoAdmin.fields if f != 'dosiero']
    model = SenditaOficialajho
    def has_add_permission(self, request, obj=None): return False

class SenditaRetposhtajhoAdmin(
            SpecialPermissionsAdmin, reversion.VersionAdmin):
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
    list_filter = ('sendadreso', 'ricevanto', 'retposhtajho', 'dato', 'temo',
                   'partoprenanto')
    search_fields = ('temo', 'teksto')
    def has_add_permission(self, request): return False
    # def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
    actions = None
    can_delete = False
class SenditaRetposhtajhoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = SenditaRetposhtajho
    extra = 0
    def has_delete_permission(self, request, obj=None): return False
    def has_add_permission(self, request): return False
    readonly_fields = SenditaRetposhtajhoAdmin.readonly_fields
    actions = None
    can_delete = False

class PartoprenantoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    '''Unuopa partoprenanto en la kongreso'''
    fields = (
        ('persona_nomo', 'familia_nomo',),
        ('shildnomo',),
        ('sekso', 'naskighdato',),
        'retposhtadreso', 'adreso',
        ('urbo', 'poshtkodo',),
        'loghlando', 'shildlando',
        ('chu_bezonas_invitleteron', 'chu_invitletero_sendita',),
        ('telefono', 'skype',),
        ('facebook', 'mesaghiloj',),
        ('chu_retalisto', 'chu_postkongresalisto',),
        ('ekde', 'ghis'),
        ('alveno', 'foriro'),
        ('interesighas_pri_antaukongreso', 'interesighas_pri_postkongreso',),
        ('chu_tuttaga_ekskurso', 'chu_unua_dua_ijk',),
        ('chu_komencanto', 'chu_interesighas_pri_kurso',),
        'programa_kontribuo', 'organiza_kontribuo',
        ('loghkategorio',),
        ('deziras_loghi_kun_nomo', 'deziras_loghi_kun',),
        ('chu_preferas_unuseksan_chambron', 'chu_malnoktemulo',),
        ('chambro',),
        ('manghotipo', 'manghomendoj'),
        ('antaupagos_ghis',),
        ('pagmaniero', 'pagmaniera_komento',),
        ('chu_antaupagis_disp', 'antaupaga_sumo_disp',),
        ('chu_ueamembro', 'uea_kodo',),
        'alighila_kotizo',
        'chu_kontrolita',
        ('unua_konfirmilo_sendita', 'dua_konfirmilo_sendita'),
        ('alighdato', 'malalighdato'),
        ('chu_alvenis', 'chu_havasmanghkuponon', 'chu_havasnomshildon',)
    )
    readonly_fields = ('id', 'alighdato', 'alighila_kotizo',
                       'chu_antaupagis_disp', 'antaupaga_sumo_disp')
    list_display = ('persona_nomo', 'familia_nomo', 'sekso',
                    'loghlando', 'chu_kontrolita', 'chambro')
    list_editable = ('loghlando', 'chambro')
    list_display_links = ('persona_nomo', 'familia_nomo')
    list_filter = ('chu_kontrolita',
        'sekso', 'naskighdato', 'loghlando',
        'chu_bezonas_invitleteron', 'chu_invitletero_sendita',
        'chu_retalisto', 'chu_postkongresalisto', 'ekde', 'ghis',
        'interesighas_pri_antaukongreso', 'interesighas_pri_postkongreso',
        'chu_tuttaga_ekskurso', 'chu_unua_dua_ijk', 'chu_komencanto',
        'chu_interesighas_pri_kurso', 'loghkategorio',
        'chu_preferas_unuseksan_chambron', 'chu_malnoktemulo', 'chambro',
        'manghomendoj', 'manghotipo', 'antaupagos_ghis', 'pagmaniero',
        'chu_ueamembro',
        'unua_konfirmilo_sendita', 'dua_konfirmilo_sendita',
        'alighdato', 'malalighdato',
        'chu_alvenis', 'chu_havasmanghkuponon', 'chu_havasnomshildon',)
    change_list_template = "admin/change_list_filter_sidebar.html"
    search_fields = ('persona_nomo', 'familia_nomo', 'shildnomo',
        'retposhtadreso', 'adreso', 'urbo', 'loghlando__nomo', 'shildlando',
        'skype', 'facebook', 'mesaghiloj', 'alveno', 'foriro',
        'programa_kontribuo', 'organiza_kontribuo',
        'deziras_loghi_kun_nomo',
        'deziras_loghi_kun__persona_nomo',
        'deziras_loghi_kun__familia_nomo',
        'pagmaniera_komento', 'uea_kodo',)
    actions = ('sendi_amasan_retposhtajhon',)
    
    def get_actions(self, request):
        actions = super(PartoprenantoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.send_retposhtajho'):
            del actions['sendi_amasan_retposhtajhon']
        if not request.user.has_perm('alighi.delete_user'):
            del actions['delete_selected']
        return actions

    def save_formset(self, request, form, formset, change):
        if formset.model == SenditaOficialajho:
            objects = formset.save(commit=False)
            for obj in objects:
                if not obj.alshutinto:
                    obj.alshutinto = request.user
                obj.save()
        elif formset.model == Pago:
            objects = formset.save(commit=False)
            for obj in objects:
                if obj.pk is None and not obj.kreinto:
                    obj.kreinto = request.user
                obj.lasta_redaktanto = request.user
                obj.save()
        else:
            super(PartoprenantoAdmin, self).save_formset(
                request, form, formset, change)

    def sendi_amasan_retposhtajhon(self, request, queryset):
        querydict = [('alsendato', pp.id) for pp in queryset]
        dest = reverse('admin:sendi') + '?' + urllib.urlencode(querydict)
        return HttpResponseRedirect(dest)
    sendi_amasan_retposhtajhon.short_description = u'Sendi amasan retpoŝtaĵon'


    def get_urls(self):
        urls = super(PartoprenantoAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^sendi/$',  # (rp-\d+/)?(\d+(?:,\d+)*/)?$',
                self.admin_site.admin_view(self.sendi), name='sendi'))
        return my_urls + urls

    def sendi(self, request):
        if not request.user.has_perm('alighi.send_retposhtajho'):
            if request.path == reverse('admin:logout',
                                       current_app=self.admin_site.name):
                index_path = reverse('admin:index',
                                     current_app=self.admin_site.name)
                return HttpResponseRedirect(index_path)
            return self.admin_site.login(request)
        try:
            pk = int(request.REQUEST.get('retposhtajho'))
        except (ValueError, TypeError):
            pk = None
        rp = get_object_or_None(Retposhtajho, pk=pk)
        ids = set()
        for ppid in request.REQUEST.getlist('alsendato'):
            try:
                ids.add(int(ppid))
            except (ValueError, TypeError):
                pass
        alsendatoj = Partoprenanto.objects.filter(pk__in=ids)

        context = {
            'retposhtajho': rp,
            'alsendatoj': alsendatoj,
            'current_app': self.admin_site.name,
            'path': request.path,
            'title': u'Sendi retpoŝtaĵon'
        }

        if (alsendatoj and rp is not None and 'konfirmi' in request.POST):
            # send it
            errors = []
            for alsendato in alsendatoj:
                if not rp.sendi(alsendato):
                    errors.append(alsendato)
            context['errors'] = errors
            context['title'] = u'Sendo de retpoŝtaĵo {}'.format(rp)
            return render_to_response('admin/sendita.html',
                                      RequestContext(request, context))
        # montri la formularon
        context.update(partoprenantoj=Partoprenanto.objects.all(),
                       retposhtajhoj=Retposhtajho.objects.all())
        return render_to_response('admin/sendi.html',
                                  RequestContext(request, context))

    inlines = (PagoInline, NotoInline, OficialajhoInline,
        SenditaRetposhtajhoInline)

class PagtipoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    search_fields = ('nomo',)
    def get_actions(self, request):
        actions = super(PagtipoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_pagtipo'):
            del actions['delete_selected']
        return actions

class KrompagTipoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'sumo')
    list_editable = list_display[1:]
    search_fields = ('nomo',)
    def get_actions(self, request):
        actions = super(KrompagTipoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_krompagtipo'):
            del actions['delete_selected']
        return actions

class NomshildoAdmin(SpecialPermissionsAdmin, reversion.VersionAdmin):
    list_display = ('nomo', 'titolo_lokalingve', 'titolo_esperante',
                    'chu_havasnomshildon')
    list_editable = list_display[1:]
    list_filter = ('chu_havasnomshildon',)
    search_fields = list_display[:-1]
    def get_actions(self, request):
        actions = super(NomshildoAdmin, self).get_actions(request)
        if not request.user.has_perm('alighi.delete_nomshildo'):
            del actions['delete_selected']
        return actions

# class UEAValidecoAdmin(admin.ModelAdmin):
    # readonly_fields = ('kodo', 'lando', 'rezulto')
# admin.site.register(UEAValideco, UEAValidecoAdmin)

# inlines
class UserRespondecoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = Respondeco
    extra = 0
    # can_delete = False
    # verbose_name_plural = 'profile'
class UserPagoInline(SpecialPermissionsAdmin, admin.TabularInline):
    model = Pago
    fk_name = 'respondeculo'
    extra = 0

# class OficialajhoInline(SpecialPermissionsAdmin, admin.TabularInline):
    # model = SenditaOficialajho
    # extra = 0

# inline additions to User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class NewUserAdmin(UserAdmin, SpecialPermissionsAdmin, reversion.VersionAdmin):
    inlines = (UserRespondecoInline, NotoInline,
               UserPagoInline, OficialajhoInline)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, NewUserAdmin)

admin.site.register(Respondeco, RespondecoAdmin)
admin.site.register(Valuto, ValutoAdmin)
admin.site.register(Kurzo, KurzoAdmin)
admin.site.register(AghKategorio, AghKategorioAdmin)
admin.site.register(AlighKategorio, AlighKategorioAdmin)
admin.site.register(LandoKategorio, LandoKategorioAdmin)
admin.site.register(Lando, LandoAdmin)
admin.site.register(LoghKategorio, LoghKategorioAdmin)
admin.site.register(ManghoMendoTipo, ManghoMendoTipoAdmin)
# admin.site.register(ManghoMendo, ManghoMendoAdmin)
admin.site.register(ManghoTipo, ManghoTipoAdmin)
admin.site.register(ProgramKotizo, ProgramKotizoAdmin)
admin.site.register(Pagmaniero, PagmanieroAdmin)
admin.site.register(Retposhtajho, RetposhtajhoAdmin)
admin.site.register(MembrighaKategorio, MembrighaKategorioAdmin)
admin.site.register(SurlokaMembrigho, SurlokaMembrighoAdmin)
admin.site.register(Chambro, ChambroAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Pagtipo, PagtipoAdmin)
admin.site.register(KrompagTipo, KrompagTipoAdmin)
admin.site.register(Nomshildo, NomshildoAdmin)
admin.site.register(Noto, NotoAdmin)
admin.site.register(UEARabato, UEARabatoAdmin)
admin.site.register(SenditaRetposhtajho, SenditaRetposhtajhoAdmin)
admin.site.register(Partoprenanto, PartoprenantoAdmin)
admin.site.register(SenditaOficialajho, SenditaOficialajhoAdmin)
