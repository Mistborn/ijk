# -*- encoding: utf-8 -*-
import datetime
import time
import json
import urllib
import smtplib
import traceback
import ast
import re

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings

from utils import eo, KOMENCA_DATO, FINIGHA_DATO, SEKSOJ, json_default, esperanteca_dato

# south
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], [r'^alighi\.models\.NeEstontecaDato'])

class Respondeco(models.Model):
    '''Respondeculo por iu afero, por aŭtomataj sciigoj'''
    rolo = models.CharField(max_length=50)
    uzanto = models.ForeignKey(User)
    def __unicode__(self):
        return self.rolo
    class Meta:
        verbose_name_plural = eo('Respondecoj')

class Valuto(models.Model):
    kodo = models.CharField(max_length=3)
    nomo = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.kodo
    class Meta:
        verbose_name_plural = eo('Valutoj')

try:
    EUR = Valuto.objects.get(kodo='EUR')
except Valuto.DoesNotExist:
    EUR = None

class Kurzo(models.Model):
    valuto = models.ForeignKey(Valuto)
    dato = models.DateField()
    kurzo = models.DecimalField(max_digits=12, decimal_places=5,
        help_text=eo('1 euxro = tiom'))
    # *** de la donita valuto al euroj
    def __unicode__(self):
        return eo(u'Kurzo por {} je {}'.format(self.valuto, self.dato))
    class Meta:
        unique_together = ('valuto', 'dato')
        verbose_name_plural = eo('Kurzoj')

class AghKategorio(models.Model):
    '''Kategorio de aĝo por kalkulado de kotizo'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.CharField(blank=True, max_length=250)
    limagho = models.IntegerField(eo('Limagxo'),
        help_text=eo('Partoprenanto kun agxo malpli ol tiu cxi agxo '
                     'eniras tiun cxi kategorion'))
    aldona_kotizo = models.DecimalField(max_digits=8, decimal_places=2,
        null=True, blank=True,
        help_text=eo('Aldona kotizo por cxiu jaro pli ol la minimuma '
                     'en tiu cxi kategorio'))

    @classmethod
    def javascript(cls):
        obj = {item.limagho: [item.id, item.aldona_kotizo]
                    for item in cls.objects.all()}
        return 'window.limaghoj = {}'.format(
                    json.dumps(obj, default=json_default))

    @staticmethod
    def liveri_aghon_lau_naskighdato(dato):
        if isinstance(dato, basestring):
            dato = datetime.date(*time.strptime(dato, '%Y-%m-%d')[:3])
        return (KOMENCA_DATO - dato).days / 365.25

    @classmethod
    def kalkuli_aldonan_kotizon(self, agho):
        if not self.aldona_kotizo:
            return 0
        if isinstance(agho, (datetime.date, basestring)):
            agho = cls.liveri_aghon_lau_naskighdato(agho)
        cls = self.__class__
        lt = cls.objects.filter(limagho__lt=self.limagho).order_by('limagho')
        minimuma = lt[-1].limagho if lt else 1
        return (agho - minimuma + 1) * self.aldona_kotizo

    @classmethod
    def liveri_kategorion(cls, agho):
        if isinstance(agho, (datetime.date, basestring)):
            agho = cls.liveri_aghon_lau_naskighdato(agho)
        rset = cls.objects.filter(limagho__gt=agho).order_by('limagho')
        return rset[0] if rset else None

    def __unicode__(self):
        return eo(u'Agxkategorio {}'.format(self.nomo))

    class Meta:
        verbose_name = eo('Agxkategorio')
        verbose_name_plural = eo('Agxkategorioj')

class AlighKategorio(models.Model):
    '''Kategorio de aliĝo laŭ dato, por kalkulado de kotizo'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.CharField(blank=True, max_length=250)
    limdato = models.DateField(unique=True,
        help_text=eo('Partoprenanto, kiu aligxas gxis tiu cxi dato '
                     'eniras tiun cxi kategorion'))

    @classmethod
    def infolist(cls):
        return [u'{} ĝis {}'.format(o.nomo, esperanteca_dato(o.limdato))
                for o in cls.objects.order_by('limdato')]

    @classmethod
    def javascript(cls):
        obj = {o.id: o.limdato.isoformat() for o in cls.objects.all()}
        return 'window.limdatoj = {}'.format(
                    json.dumps(obj, default=json_default))

    @classmethod
    def liveri_kategorion(cls, dato):
        rset = cls.objects.filter(limdato__gte=dato).order_by('limdato')
        return rset[0] if rset else None

    def __unicode__(self):
        #return self.limdato
        return eo(u'Aligxkategorio {} gxis {}'.format(self.nomo, self.limdato))

    class Meta:
        verbose_name = eo('Aligxkategorio')
        verbose_name_plural = eo('Aligxkategorioj')

class LandoKategorio(models.Model):
    '''Kategorio de lando, por kalkulado de kotizo'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.CharField(blank=True, max_length=255)

    @staticmethod
    def liveri_kategorion(lando):   # for consistency
        return lando.kategorio

    def __unicode__(self):
        return eo(u'Landokategorio ' + self.nomo)

    class Meta:
        verbose_name = eo('Landokategorio')
        verbose_name_plural = eo('Landokategorioj')

class Lando(models.Model):
    '''Loĝlando de partoprenanto'''
    nomo = models.CharField(max_length=50)
    kodo = models.CharField(max_length=2)
    kategorio = models.ForeignKey(LandoKategorio)

    @classmethod
    def javascript(cls):
        obj = {item.id: item.kategorio.id for item in cls.objects.all()}
        return 'window.landoj = {}'.format(
                    json.dumps(obj, default=json_default))

    def __unicode__(self):
        #return self.nomo
        return u'{} ({})'.format(self.nomo, self.kategorio)
    class Meta:
        verbose_name_plural = eo('Landoj')

class LoghKategorio(models.Model):
    '''Elektebla loĝkategorio'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.CharField(blank=True, max_length=250)
    plena_kosto = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Kosto por logxo dum la tuta kongreso'))
    unutaga_kosto = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Kosto por logxo dum unu nokto'))

    @classmethod
    def javascript(cls):
        obj = {item.id: [item.plena_kosto, item.unutaga_kosto]
                    for item in cls.objects.all()}
        return 'window.loghkategorioj = {}'.format(
                    json.dumps(obj, default=json_default))

    @classmethod
    def helptext(cls):
        rows = cls.objects.order_by('pk')
        r = []
        plentempaj = u''.join(
            u'<li>{} &mdash; {} €</li>'.format(escape(row.nomo),
                                         escape(row.plena_kosto))
                for row in rows)
        unutagaj = u''.join(
            u'<li>{} &mdash; {} €</li>'.format(escape(row.nomo),
                                         escape(row.unutaga_kosto))
                for row in rows)
        r.append(u'Plentempaj kostoj: <ul>{}</ul>'.format(plentempaj))
        r.append(u'Unutagaj kostoj: <ul>{}</ul>'.format(unutagaj))
        return mark_safe('\n'.join(r))

    def __unicode__(self):
        return self.nomo
        #~ return u'{} - plentempe: {} €, partatempe: {} € por tago'.format(
            #~ self.nomo, self.plena_kosto, self.unutaga_kosto)

    class Meta:
        verbose_name = eo('Logxkategorio')
        verbose_name_plural = eo('Logxkategorioj')

class ManghoTipo(models.Model):
    '''Tipo de manĝo, ekz. vegetare, koŝere, ktp'''
    nomo = models.CharField(unique=True, max_length=50)
    # vegetare/vegane/ktp

    def __unicode__(self):
        return self.nomo

    class Meta:
        verbose_name = eo('Mangxotipo')
        verbose_name_plural = eo('Mangxotipoj')

class ProgramKotizo(models.Model):
    '''Kotizo por la programo mem, kalkulita lau aĝo, lando, kaj aliĝdato'''
    aghkategorio = models.ForeignKey(AghKategorio,
        verbose_name=eo('Agxkategorio'))
    landokategorio = models.ForeignKey(LandoKategorio,
        verbose_name=eo('Landokategorio'))
    alighkategorio = models.ForeignKey(AlighKategorio,
        verbose_name=eo('Aligxkategorio'))
    kotizo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Programkotizo en euxroj por tiu cxi grupo'))

    def kalkuli_finan_kotizon(self, agho):
        aldono = self.aghkategorio.kalkuli_aldonan_kotizon(agho)
        return self.kotizo + aldono

    @classmethod
    def javascript(cls):
        aghokeys = [o.aghkategorio.id for o in cls.objects.all()]
        obj = {}
        for aghk in AghKategorio.objects.all():
            obj[aghk.id] = {}
            for landok in LandoKategorio.objects.all():
                obj[aghk.id][landok.id] = {}
                for alighk in AlighKategorio.objects.all():
                    k = cls.objects.filter(
                            aghkategorio=aghk, landokategorio=landok,
                                alighkategorio=alighk)
                    obj[aghk.id][landok.id][alighk.id] = (k[0].kotizo
                                if k else None)
        return 'window.programkotizoj = {}'.format(
                    json.dumps(obj, default=json_default))

    def __unicode__(self):
        return eo(u'{}, {}, {} : {} €'.format(
            self.aghkategorio, self.landokategorio, self.alighkategorio,
            self.kotizo))
    class Meta:
        verbose_name = eo('Programkotizo')
        verbose_name_plural = eo('Programkotizoj')
        unique_together = ('aghkategorio', 'landokategorio', 'alighkategorio')

class Pagmaniero(models.Model):
    '''maniero transdoni monon,
    ekz. per peranto, surloke, unuopula rabato, ktp'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.CharField(blank=True, max_length=250,
        verbose_name=eo('Publika priskribo'))
    komenta_etikedo = models.CharField(blank=True, max_length=250,
        verbose_name=eo('Komenta etikedo'), default=u'',
        help_text=eo('Etikedo por la komenta kampo en la aligxformularo'))
    chu_publika = models.BooleanField(default=True,
        verbose_name=eo('Cxu publika'),
        help_text=eo('Cxu tiu cxi pagmaniero estu elektebla por indiki, '
                     'kiel oni intencas pagi la antauxpagon'))
    chu_nurisraela = models.BooleanField(default=False,
        verbose_name=eo('Cxu nur-israela'),
        help_text=eo('Cxu tiu cxi pagmaniero estas ebla nur en Israelo'))

    @classmethod
    def javascript(cls):
        return u''


    def __unicode__(self):
        return self.nomo + (u' (nur en Israelo)' if self.chu_nurisraela
                                                else u'')
    class Meta:
        verbose_name_plural = eo('Pagmanieroj')

class KrompagTipo(models.Model):
    '''Aldonaj pagoj por diversaj aferoj, kiel ekz. ekskurso, invitletero'''
    nomo = models.SlugField()
    sumo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Plusa por krompago (aldona kosto), '
                     'minusa por rabato'))
    @classmethod
    def javascript(cls):
        d = {o.nomo: o.sumo for o in cls.objects.all()}
        return 'window.krompagtipoj = {}'.format(
                    json.dumps(d, default=json_default))

    @classmethod
    def liveri_koston(cls, key):
        try:
            return cls.objects.get(nomo=key).sumo
        except cls.DoesNotExist:
            return u''

    def __unicode__(self):
        return self.nomo

    class Meta:
        verbose_name = eo('KrompagTipo')
        verbose_name_plural = eo('KrompagTipoj')

class Retposhtajho(models.Model):
    '''Retpoŝta mesaĝo, por amasa/aŭtomata sendo'''
    nomo = models.CharField(unique=True, max_length=50)
    sendadreso = models.EmailField(blank=False, default=settings.FROM_EMAIL)
    temo = models.CharField(max_length=100)
    teksto = models.TextField()

    @classmethod
    def get_by_nomo(cls, nomo):
        try:
            return cls.objects.get(nomo=nomo)
        except cls.DoesNotExist:
            return None

    @staticmethod
    def eval_cond(cond, yes, no, partoprenanto):
        try:
            cond = ('{' + cond.strip() + '!r}').format(
                partoprenanto=partoprenanto)
        except LookupError:
            return u''
        try:
            cond = ast.literal_eval(cond)
        except ValueError:
            return u''
        if cond:
            result = yes
        else:
            result = no
        return re.sub(r'\\([?:\\])', r'\1', result.strip())

    def cond_interpolate(self, partoprenanto):
        '''interpolate directives like
        #{partoprenanto.chu_malnoktemulo ? dormu! : festu! }'''
        def sub(string):
            return re.sub(r'#{([^{}]+)(?<!\\)\?([^{}]+)(?<!\\):([^{}]+)}',
                          lambda m: self.eval_cond(m.group(1), m.group(2),
                                                   m.group(3), partoprenanto),
                          string)
        return sub(self.temo), sub(self.teksto)

    def interpolate(self, partoprenanto):
        ## pwrapper = PartoprenantoWrapper(partoprenanto)
        temo, teksto = self.cond_interpolate(partoprenanto)
        teksto = teksto.format(partoprenanto=partoprenanto)
        temo = temo.format(partoprenanto=partoprenanto)
        # FIXME: for now we're just letting exceptions propagate
        return (temo, teksto)

    def sendi(self, partoprenanto):
        temo, teksto = self.interpolate(partoprenanto)
        sendajho = SenditaRetposhtajho(
            temo = temo,
            teksto = teksto,
            sendadreso = self.sendadreso,
            ricevanto = partoprenanto.retposhtadreso,
            partoprenanto = partoprenanto,
            retposhtajho = self)
        try:
            send_mail(self.temo, teksto, self.sendadreso,
                [partoprenanto.retposhtadreso], fail_silently=False)
        except smtplib.SMTPException:
            sendajho.traceback = traceback.format_exc()
        sendajho.save()

    def __unicode__(self):
        return self.nomo

    class Meta:
        verbose_name = eo('Retposxtajxo')
        verbose_name_plural = eo('Retposxtajxoj')

class MembrighaKategorio(models.Model):
    '''Por krei liston de kategorioj de surlokaj membriĝoj en UEA/TEJO'''
    nomo = models.CharField(unique=True, max_length=50,
        help_text=eo('Nomo de la kategorio de surloka membrigxo en TEJO/UEA'))
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name = eo('Membrigxa Kategorio')
        verbose_name_plural = eo('Membrigxaj Kategorioj')

class Chambro(models.Model):
    '''Unuopa ĉambro por disdoni'''
    nomo = models.CharField(unique=True, max_length=50)
    litonombro = models.IntegerField(
        help_text=eo('nombro da litoj en la cxambro'))
        # maksimuma nombro da homoj kiuj povos loghi en tiu chi chambro
    loghkategorio = models.ForeignKey(LoghKategorio,
        verbose_name=eo('Logxkategorio'))
        # al kiu loghkategorio ghi taugas?
    rimarko = models.CharField(blank=True, max_length=255)
    def __unicode__(self):
        return u'{} ({}), litoj: {}'.format(
            self.nomo, self.loghkategorio, self.litonombro)
    class Meta:
        verbose_name = eo('Cxambro')
        verbose_name_plural = eo('Cxambroj')

class UEARabato(models.Model):
    landokategorio = models.OneToOneField(LandoKategorio)
    sumo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Rabato pro UEA-membreco en tiu cxi landokategorio'))

    @classmethod
    def infoline(cls):
        return u', '.join(u'{}: {} €'.format(o.landokategorio, o.sumo)
            for o in cls.objects.order_by('landokategorio'))

    @classmethod
    def javascript(cls):
        obj = {o.landokategorio.id: o.sumo for o in cls.objects.all()}
        return 'window.uearabatoj = {}'.format(
                    json.dumps(obj, default=json_default))

    @classmethod
    def rabato(cls, lando):
        r = cls.objects.get(landokategorio=lando.kategorio)
        return r.sumo

    def __unicode__(self):
        return eo(u'{} € por {}'.format(
                        self.sumo, self.landokategorio))
    class Meta:
        verbose_name = eo('UEA-rabato')
        verbose_name_plural = eo('UEA-rabatoj')

class PartoprenantoWrapper(object):
    '''Wrapper around a Partoprenanto object to change the string
    representation of some of the fields,
    for use in interpolation into emails.'''
    def __init__(self, partoprenanto):
        self.partoprenanto = partoprenanto
    def __getattr__(self, name):
        attr = getattr(self.partoprenanto, name)
        if isinstance(attr, bool):
            attr = 'jes' if attr else 'ne'
        return attr

class Partoprenanto(models.Model):
    '''Partoprenanto en la kongreso'''
    persona_nomo = models.CharField(max_length=50)
    familia_nomo = models.CharField(max_length=50)
    shildnomo = models.CharField(eo('Sxildnomo'), blank=True, max_length=50)
    sekso = models.CharField(max_length=1, choices=SEKSOJ)
    naskighdato = models.DateField(eo('Naskigxdato'))
    retposhtadreso = models.EmailField(eo('Retposxtadreso'))
    adreso = models.TextField(blank=True)
    urbo = models.CharField(blank=True, max_length=50)
    poshtkodo = models.CharField(eo('Posxtkodo'), blank=True, max_length=15)
    loghlando = models.ForeignKey(Lando, verbose_name=eo('Logxlando'))
    shildlando = models.CharField(eo('Sxildlando'), blank=True, max_length=50)
    chu_bezonas_invitleteron = models.BooleanField(
        eo('Cxu bezonas invitleteron'), default=False)
    chu_invitletero_sendita = models.BooleanField(
        eo('Cxu invitletero sendita'), default=False)
    telefono = models.CharField(blank=True, max_length=50)
    skype = models.CharField(blank=True, max_length=50)
    facebook = models.CharField(blank=True, max_length=50)
    mesaghiloj = models.CharField(
        eo('Aliaj mesagxiloj'), max_length=255, blank=True)
    chu_retalisto = models.BooleanField(
        eo('Cxu konsentas aperi en la reta listo'), default=True)
    chu_postkongresalisto = models.BooleanField(
        eo('Cxu konsentas aperi en la postkongresa listo'), default=True)
    ekde = models.DateField(default=KOMENCA_DATO)
    ghis = models.DateField(eo('Gxis'), default=FINIGHA_DATO)
    alveno = models.CharField(blank=True, max_length=255)
    foriro = models.CharField(blank=True, max_length=255)
    interesighas_pri_antaukongreso = models.IntegerField(
        eo('Interesigxas pri antauxkongreso'), null=True, blank=True,
        help_text='kiom da tagoj')
    interesighas_pri_postkongreso = models.IntegerField(
        eo('Interesigxas pri postkongreso'), null=True, blank=True,
        help_text='kiom da tagoj')
    chu_tuttaga_ekskurso = models.BooleanField(
        eo('Cxu aligxas al la tut-taga ekskurso'), default=True)
    chu_unua_dua_ijk = models.BooleanField(eo('Cxu unua aux dua IJK'),
        default=False)
    chu_komencanto = models.BooleanField(eo('Cxu komencanto'), default=True)
    chu_interesighas_pri_kurso = models.BooleanField(
        eo('Cxu interesigxas pri E-kurso'), default=True)
    programa_kontribuo = models.TextField(blank=True)
    organiza_kontribuo = models.TextField(blank=True)
    loghkategorio = models.ForeignKey(LoghKategorio,
        verbose_name=eo('Logxkategorio'))
    deziras_loghi_kun_nomo = models.CharField(
        eo('Deziras logxi kun (nomo)'), blank=True, max_length=50)
    deziras_loghi_kun = models.ForeignKey('Partoprenanto',
        null=True, blank=True, verbose_name=eo('Deziras logxi kun'),
        help_text=eo('Elektu cxi tie la alian partoprenanton indikitan '
                     'supre, post kiam li-sxi aligxos')) #*
    chu_preferas_unuseksan_chambron = models.BooleanField(
        eo('Cxu preferas unuseksan cxambron'), default=False)
    chu_malnoktemulo = models.BooleanField(
        eo('Cxu malnoktemulo'), default=False)
    chambro = models.ForeignKey(Chambro,
        verbose_name=eo('Cxambro'), null=True, blank=True)
    manghotipo = models.ForeignKey(ManghoTipo, verbose_name=eo('Mangxotipo'),
        help_text=eo('Tipo de mangxo, ekz. vegetare, viande, ktp'))
    antaupagos_ghis = models.ForeignKey(AlighKategorio,
        verbose_name=eo('Antauxpagos gxis'), null=True,
        help_text=eo('Kio estis enigita en la alighformularo'))
    pagmaniero = models.ForeignKey(Pagmaniero,
        help_text=eo('Por la antauxpago'))
        # el la publikaj pagmanieroj, por la antaupago
    pagmaniera_komento = models.CharField(blank=True, max_length=250)
        # ekz por nomo de peranto
    chu_ueamembro = models.BooleanField(eo('Cxu membro de UEA/TEJO'),
        default=False)
    uea_kodo = models.CharField(eo('UEA-kodo'), max_length=18, blank=True)
    chu_kontrolita = models.BooleanField(
        eo('Cxu kontrolita'), default=False) #*
    unua_konfirmilo_sendita = models.DateField(null=True, blank=True) #*
    dua_konfirmilo_sendita = models.DateField(null=True, blank=True) #*
    alighdato = models.DateField(eo('Aligxdato'), auto_now_add=True) #*
    malalighdato = models.DateField(eo('Malaligxdato'), null=True, blank=True,
        help_text=eo('Se la partoprenanto malaligxis')) #*
    chu_alvenis = models.BooleanField(eo('Cxu alvenis'), default=False) #*
    chu_havasmanghkuponon = models.BooleanField(
        eo('Cxu havas mangxkuponon'), default=False) #*
    chu_havasnomshildon = models.BooleanField(
        eo('Cxu havas nomsxildon'), default=False) #*

    def manghomendoj(self):
        return ManghoMendo.objects.filter(partoprenanto=self)

    def chu_plentempa(self):
        return self.ekde == KOMENCA_DATO and self.ghis == FINIGHA_DATO

    def tagoj(self):
        '''suma numbro da tagoj de tiu chi partoprenanto'''
        return (self.ghis - self.ekde).days

    def programkotizo(self):
        aghkategorio = AghKategorio.liveri_kategorion(self.naskighdato)
        landokategorio = self.loghlando.kategorio
        alighkategorio = AlighKategorio.liveri_kategorion(self.alighdato)
            # XXX vershajne devas esti la dato de la antaupago
        programkotizo = ProgramKotizo.objects.get(
            aghkategorio=aghkategorio,
            landokategorio=landokategorio,
            alighkategorio=alighkategorio)
        return programkotizo.kalkuli_finan_kotizon(self.naskighdato)

    def uearabato(self):
        if not self.chu_ueamembro:
            return 0
        return UEARabato.rabato(self.loghlando)

    def kotizo(self):
        '''Liveri la bazan kotizon de tiu ĉi partoprenanto
        Formulo por kotizo:
            [manĝokosto lau la elekto] +
            [loĝkosto lau elekto kaj lau kvanto de tagoj] -
            [rabato pro UEA-membreco] + [program-kotizo]'''
        manghomenda_kosto = sum(item.tipo.kosto
                    for item in self.manghomendoj())
        if self.chu_plentempa:
            loghkosto = self.loghkategorio.plena_kosto
        else:
            loghkosto = self.tagoj() * self.loghkategorio.unutaga_kosto
        uearabato = self.uearabato()
        programkotizo = self.programkotizo()

        return manghomenda_kosto + loghkosto + programkotizo - uearabato

    def __getattr__(self, name):
        if name.endswith('_jn'):
            val = getattr(self, name[:-3])
            return 'jes' if val else 'ne'
        return getattr(super(Partoprenanto, self), name)

    def __unicode__(self):
        return u'{} {}'.format(self.persona_nomo, self.familia_nomo)

    class Meta:
        verbose_name_plural = eo('Partoprenantoj')
        ordering = ('familia_nomo',)

class ManghoMendoTipo(models.Model):
    '''Tipo de manĝo kiun oni povas mendi (matenmanĝo, tagmanĝo, ktp)'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    kosto = models.DecimalField(max_digits=8, decimal_places=2)
    # memzorge/matenmangho/tagmangho/vespermangho

    @classmethod
    def javascript(cls):
        d = {obj.id: obj.kosto for obj in cls.objects.all()}
        return '''window.manghomendotipoj = {}'''.format(json.dumps(d,
            default=json_default))

    def __unicode__(self):
        return eo(u'{} je {} €'.format(self.nomo, self.kosto))

    class Meta:
        verbose_name = eo('Mangxomendotipo')
        verbose_name_plural = eo('Mangxomendotipoj')

class ManghoMendo(models.Model):
    '''Unuopa manĝomendo de partoprenanto'''
    partoprenanto = models.ForeignKey(Partoprenanto)
    tipo = models.ForeignKey(ManghoMendoTipo)
    def __unicode__(self):
        return eo(u'Mangxomendo de {} por {}'.format(
                  self.partoprenanto, self.tipo.nomo))
    class Meta:
        verbose_name = eo('Mangxomendo')
        verbose_name_plural = eo('Mangxomendoj')
        unique_together = ('partoprenanto', 'tipo')

class SurlokaMembrigho(models.Model):
    '''Por registri surlokajn membriĝojn en UEA/TEJO'''
    partoprenanto = models.OneToOneField(Partoprenanto)
    kategorio = models.ForeignKey(MembrighaKategorio,
        help_text=eo(u'Nomo de la membreco-kategorio en TEJO/UEA'))
    kotizo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo(u'Laux la logxlando de la partoprenanto'))
    valuto = models.ForeignKey(Valuto)
    def __unicode__(self):
        return eo(u'{}: {}'.format(self.partoprenanto, self.kategorio))
    class Meta:
        verbose_name = eo('Surloka Membrigxo')
        verbose_name_plural = eo('Surlokaj Membrigxoj')
        ordering = ('partoprenanto',)

class Pagtipo(models.Model):
    '''Tipo de pago, ekz. subvencio, antaŭpago, ktp'''
    nomo = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = eo('Pagtipoj')

class NeEstontecaDato(models.DateField):
    '''Dato, kiu ne povas esti en la estonteco'''
    def __init__(self, *args, **kw):
        super(NeEstontecaDato, self).__init__(*args, **kw)
        self.error_messages['estonteco'] = self.error_messages.get(
            u'estonteco', u'La dato ne povas esti en la estonteco.')
    def validate(self, value, instance):
        if value and value > datetime.date.today():
            msg = self.error_messages['estonteco']
            raise ValidationError(msg)
        return super(NeEstontecaDato, self).validate(value, instance)

class Pago(models.Model):
    '''Unuopa pago de unuopa partoprenanto'''
    partoprenanto = models.ForeignKey(Partoprenanto)
    respondeculo = models.ForeignKey(User, related_name='pagorespondeculo',
        help_text=eo('Respondeculo, kiu ricevis/notis la pagon'))
    kreinto = models.ForeignKey(User, related_name='pagokreinto',
        help_text=eo('Uzanto, kiu kreis la rikordon de tiu cxi pago'),
        null=True, blank=True, editable=False)
    lasta_redaktanto = models.ForeignKey(User, related_name='pagoredaktanto',
        help_text=eo('Uzanto, kiu laste redaktis tiun cxi pagon'),
        null=True, blank=True, editable=False)
    pagmaniero = models.ForeignKey(Pagmaniero,
        help_text=eo('Kiamaniere ni ricevis la pagon'))
    pagtipo = models.ForeignKey(Pagtipo,
        help_text=eo(u'Tipo de pago, ekz. subvencio, antauxpago, ktp'))
    valuto = models.ForeignKey(Valuto, default=EUR)
    sumo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo(u'Rabaton enigu kiel normalan pagon, krompagon '
                     u'enigu kiel minusan sumon'))
    dato = NeEstontecaDato(error_messages={'estonteco':
        u'Pago ne povas esti en la estonteco.'})
    rimarko = models.CharField(blank=True, max_length=255,
        help_text=eo('Ekz. por indiki peranton, konto por UEA gxiro, ktp'))

    def __unicode__(self):
        return eo(u'{} {} ({}) de {} je {}'.format(
            self.sumo, self.valuto, self.pagtipo, self.partoprenanto,
            self.dato))
    class Meta:
        verbose_name_plural = eo('Pagoj')
        ordering = ('partoprenanto',)

class MinimumaAntaupago(models.Model):
    '''Minimuma antaŭpago por partopreni'''
    landokategorio = models.ForeignKey(LandoKategorio)
    oficiala_antaupago = models.DecimalField(eo('Oficiala antauxpago'),
        max_digits=8, decimal_places=2,
        help_text=eo('La sumo, kiun ni montras oficiale'))
    interna_antaupago = models.DecimalField(eo('Interna antauxpago'),
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text=eo('La sumo, kiun ni uzas por internaj kalkuloj, se alia'))
    # Kion ni montras ekstere kaj kion ni uzas por internaj kalkuloj

    @classmethod
    def javascript(cls):
        obj = {o.landokategorio.id: o.oficiala_antaupago
                        for o in cls.objects.all()}
        return 'window.minimumaj_antaupagoj = {}'.format(
                        json.dumps(obj, default=json_default))

    def __unicode__(self):
        return eo(u'{} € por {}'.format(
                  self.oficiala_antaupago, self.landokategorio))
    class Meta:
        verbose_name = eo('Minimuma Antauxpago')
        verbose_name_plural = eo('Minimumaj Antauxpagoj')

class Nomshildo(models.Model):
    '''Specialaj nomŝildoj por nepartoprenantoj'''
    nomo = models.CharField(max_length=50)
    titolo_lokalingve = models.CharField(max_length=50)
    titolo_esperante = models.CharField(max_length=50)
    #funkcio_lokalingve = models.CharField()
    #funkcio_esperante = models.CharField()
    chu_havasnomshildon = models.BooleanField(eo('Cxu havas nomsxildon'),
        default=False)
    def __unicode__(self):
        return eo(u'Nomsxildo por ' + self.nomo)
    class Meta:
        verbose_name = eo('Nomsxildo')
        verbose_name_plural = eo('Nomsxildoj')

class Noto(models.Model):
    '''Memorigo por pritraktado'''
    partoprenanto = models.ForeignKey(Partoprenanto, null=True, blank=True)
    uzanto = models.ForeignKey(User, null=True, blank=True)
    #kiu = models.CharField(max_length=300) # noto de
    #kunkiu = models.CharField(max_length=300) # pri komunicado kun
    dato = models.DateTimeField(auto_now_add=True)
    #temo = models.CharField()
    enhavo = models.TextField()
    chu_prilaborita = models.BooleanField(eo('Cxu prilaborita'), default=False)
    revidu = models.DateTimeField(null=True, blank=True,
        help_text=eo('Kiam memorigi pri tio cxi'))
    def __unicode__(self):
        tondajho = u'{}{}'.format(eo(self.enhavo[:47]), u'...' if len(self.enhavo) > 47 else u'')
        signo = u'\u2714 ' if self.chu_prilaborita else u''
        nomo = (u'{} :'.format(self.partoprenanto)
                        if self.partoprenanto else '')
        return u'{}{} {}'.format(signo, nomo, tondajho)
    class Meta:
        verbose_name_plural = eo('Notoj')
        ordering = ('partoprenanto',)

class UEAValideco(models.Model):
    CHOICES = list(enumerate((
        u'Nekonata UEA-kodo aŭ nekongrua lando '
            u'(lasu malplena se vi ne memoras vian kodon)',
        u'UEA-kodo ekzistas kaj kongruas kun la lando',
        u'Nevalida UEA-kodo (lasu malplena se vi ne memoras vian kodon)')))

    kodo = models.CharField(max_length=6, editable=False)
    lando = models.CharField(max_length=2, editable=False)
    rezulto = models.IntegerField(null=True, editable=False, choices=CHOICES)

    def __unicode__(self):
        return u'{}_{}: {}'.format(self.kodo, self.lando, self.rezulto)

    @classmethod
    def chu_valida(cls, kodo, lando):
        kodo = kodo.lower()
        lando = lando.lower()
        try:
            x = cls.objects.get(kodo=kodo, lando=lando)
        except cls.DoesNotExist:
            pass
        else:
            return (x.rezulto == 1,
                    cls.CHOICES[x.rezulto][1]
                        if x.rezulto is not None else u'')
        url = 'http://db.uea.org/alighoj/kontr.php?la={}_{}'.format(
            kodo.lower(), lando.lower())
        try:
            r = int(urllib.urlopen(url).read().strip())
        except ValueError:
            r = None
        cls(kodo=kodo, lando=lando, rezulto=r).save()
        return (r == 1, cls.CHOICES[r][1] if r is not None else u'')

    class Meta:
        unique_together = ('kodo', 'lando')

class SenditaRetposhtajho(models.Model):
    # this table is append-only
    temo = models.CharField(max_length=250, blank=False, editable=False)
    teksto = models.TextField(blank=False, editable=False)
    sendadreso = models.EmailField(blank=False, editable=False)
    ricevanto = models.EmailField(blank=False, editable=False)
    partoprenanto = models.ForeignKey(Partoprenanto, null=True, editable=False)
    retposhtajho = models.ForeignKey(Retposhtajho, null=True, editable=False)
    # no traceback means it succeeded
    traceback = models.TextField(blank=True, editable=False)
    dato = models.DateField(auto_now_add=True, editable=False)

    def chu_sukcese(self):
        return not self.traceback
    chu_sukcese.boolean = True
    chu_sukcese.short_description = 'Ĉu sukcese'

    def __unicode__(self):
        return u'"{}" al <{}>'.format(self.temo, self.ricevanto)

    class Meta:
        verbose_name = eo('Sendita Retposxtajxo')
        verbose_name_plural = eo('Senditaj Retposxtajxoj')

## class SenditaOficialajho(models.Model):
    ## pass
##
    ## def __unicode__(self):
        ## pass
##
    ## class Meta:
        ## verbose_name = eo('Sendita Oficialajxo')
        ## verbose_name_plural = eo('Senditaj Oficialajxoj')
