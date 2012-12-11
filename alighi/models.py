# -*- encoding: utf-8 -*-
import datetime
import time

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils import eo, KOMENCA_DATO, FINIGHA_DATO, SEKSOJ

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
        
class Kurzo(models.Model):
    valuto = models.ForeignKey(Valuto)
    dato = models.DateField()
    kurzo = models.DecimalField(max_digits=12, decimal_places=5,
        help_text=eo('1 euxro = tiom'))
    # *** de la donita valuto al EUR
    def __unicode__(self):
        return eo(u'Kurzo por {} je {}'.format(self.valuto, self.dato))
    class Meta:
        unique_together = ('valuto', 'dato')
        verbose_name_plural = eo('Kurzoj')
        
class AghKategorio(models.Model):
    '''Kategorio de aĝo por kalkulado de kotizo'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(AghKategoriSistemo)
    limagho = models.IntegerField(eo('Limagxo'),
        help_text=eo('Partoprenanto kun agxo malpli ol tiu cxi agxo '
                     'eniras tiun cxi kategorion'))
    aldona_kotizo = models.DecimalField(max_digits=8, decimal_places=2,
        null=True, blank=True,
        help_text=eo('Aldona kotizo por cxiu jaro pli ol la minimuma '
                     'en tiu cxi kategorio'))

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
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(AlighKategoriSistemo)
    limdato = models.DateField(unique=True,
        help_text=eo('Partoprenanto, kiu aligxas gxis tiu cxi dato '
                     'eniras tiun cxi kategorion'))

    @classmethod
    def liveri_kategorion(cls, dato):
        rset = cls.objects.filter(limdato__gte=dato).order_by('limdato')
        return rset[0] if rset else None
    
    def __unicode__(self):
        return eo(u'Aligxkategorio {} gxis {}'.format(self.nomo, self.limdato))
    
    class Meta:
        verbose_name = eo('Aligxkategorio')
        verbose_name_plural = eo('Aligxkategorioj')

class LandoKategorio(models.Model):
    '''Kategorio de lando, por kalkulado de kotizo'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(LandoKategoriSistemo)

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
    def __unicode__(self):
        return u'{} ({})'.format(self.nomo, self.kategorio)
    class Meta:
        verbose_name_plural = eo('Landoj')

class LoghKategorio(models.Model):
    '''Elektebla loĝkategorio'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(LoghKategoriSistemo)
    #kondicho = models.IntegerField()
    plena_kosto = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Kosto por logxo dum la tuta kongreso'))
    unutaga_kosto = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Kosto por logxo dum unu nokto'))
        
    def __unicode__(self):
        return self.nomo
        
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
        
    def __unicode__(self):
        return eo(u'{}, {}, {} : {} EUR'.format(
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
    priskribo = models.TextField(blank=True)
    chu_publika = models.BooleanField(default=True,
        verbose_name=eo('Cxu publika'),
        help_text=eo('Cxu tiu cxi pagmaniero estu elektebla por indiki, '
                     'kiel oni intencas pagi la antauxpagon'))
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = eo('Pagmanieroj')

class Retposhtajho(models.Model):
    '''Retpoŝta mesaĝo, por amase senditaj retposhtaĵoj'''
    nomo = models.CharField(unique=True, max_length=50)
    temo = models.CharField(max_length=100)
    teksto = models.TextField()
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name = eo('Retposxtajxo')
        verbose_name_plural = eo('Retposxtajxoj')

class MembrighaKategorio(models.Model):
    '''Por krei liston de kategorioj de surlokaj membriĝoj en UEA/TEJO'''
    nomo = models.CharField(unique=True, max_length=50,
        help_text=eo('Nomo de la kategorio de surloka membrigxo en TEJO/UEA'))
    #kotizo = models.DecimalField(max_digits=8, decimal_places=2,
        #help_text=eo('Sumo de la kotizo'))
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name = eo('Membrigxa Kategorio')
        verbose_name_plural = eo('Membrigxaj Kategorioj')

class Chambro(models.Model):
    '''Unuopa ĉambro por disdoni'''
    #renkontigho = models.ForeignKey(Renkontigho)
    nomo = models.CharField(unique=True, max_length=50)
    #etagho = models.CharField(max_length=150)
    litonombro = models.IntegerField(
        help_text=eo('nombro da litoj en la cxambro'))
        # maksimuma nombro da homoj kiuj povos loghi en tiu chi chambro
    loghkategorio = models.ForeignKey(LoghKategorio,
        verbose_name=eo('Logxkategorio'))
        # al kiu loghkategorio ghi taugas?
    #dulita = models.CharField(max_length=3)
    rimarko = models.CharField(blank=True, max_length=255)
    def __unicode__(self):
        return u'{} ({}), litoj: {}'.format(
            self.nomo, self.loghkategorio, self.litonombro)
    class Meta:
        verbose_name = eo('Cxambro')
        verbose_name_plural = eo('Cxambroj')

class UEARabato(models.Model):
    landokategorio = models.ForeignKey(LandoKategorio, unique=True)
    sumo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo('Rabato pro UEA-membreco en tiu cxi landokategorio'))

    @classmethod
    def liveri_rabaton(cls, lando):
        rabato = cls.objects.get(landokategorio=lando.kategorio)
        return rabato.sumo
        
    def __unicode__(self):
        return eo(u'{} EUR por {}'.format(
                        self.sumo, self.landokategorio))
    class Meta:
        verbose_name = eo('UEA-rabato')
        verbose_name_plural = eo('UEA-rabatoj')

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
    #alvenas_je = models.DateField(null=True, blank=True)
    foriro = models.CharField(blank=True, max_length=255)
    #foriras_je = models.DateField(null=True, blank=True)
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
    chambro = models.ForeignKey(Chambro,
        verbose_name=eo('Cxambro'), null=True, blank=True)
    manghotipo = models.ForeignKey(ManghoTipo, verbose_name=eo('Mangxotipo'),
        help_text=eo('Tipo de mangxo, ekz. vegetare, viande, ktp'))
    pagmaniero = models.ForeignKey(Pagmaniero,
        help_text=eo('Por la antauxpago'))
        # el la publikaj pagmanieroj, por la antaupago
    pagmaniera_komento = models.CharField(blank=True, max_length=50)
        # ekz por nomo de peranto
    #antaupago_ghis = models.DateField()
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
    #rimarkoj = models.TextField()
    # ******************** pri la programo
#class Partopreno(models.Model):
    #renkontigho = models.ForeignKey(Renkontigho)
    #partoprenanto = models.ForeignKey(Partoprenanto)
    # ******************** pri loghado
    # manghado
    # povas esti pluraj manghomendoj, do por tio vidu tiun tabelon
    # chu mi volas aperi en tiaj listoj:
    #dulita = models.CharField(max_length=3)
    #tema = models.TextField()
    #distra = models.TextField()
    #vespera = models.TextField()
    #muzika = models.TextField()
    #nokta = models.TextField()
    # ******************* kontribuo
    # ******************* de tie chi estas kampoj por interna uzo
    #alighkategoridato = models.DateField()
    # informoj por surloka kontrolo:
    #por rimarkoj, vidu la tabelon Noto

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
        return UEARabato.liveri_rabaton(self.loghlando)
        
    # methods
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
            loghkosto = (self.tagoj() *
                                self.loghkategorio.unutaga_kosto)
        uearabato = self.uearabato()
        programkotizo = self.programkotizo()

        return manghomenda_kosto + loghkosto + programkotizo - uearabato
    
    def __unicode__(self):
        return u'{} {}'.format(self.persona_nomo, self.familia_nomo)

    class Meta:
        verbose_name_plural = eo('Partoprenantoj')

class ManghoMendoTipo(models.Model):
    '''Tipo de manĝo kiun oni povas mendi (matenmanĝo, tagmanĝo, ktp)'''
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    kosto = models.DecimalField(max_digits=8, decimal_places=2)
    # memzorge/matenmangho/tagmangho/vespermangho
    def __unicode__(self):
        return eo(u'{} je {} EUR'.format(self.nomo, self.kosto))
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
        #order_with_respect_to = 'partoprenanto' # XXX this?

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
    uzanto = models.ForeignKey(User,
        help_text=eo('Respondeculo, kiu ricevis/notis la pagon'))
    pagmaniero = models.ForeignKey(Pagmaniero,
        help_text=eo('Kiamaniere ni ricevis la pagon'))
    pagtipo = models.ForeignKey(Pagtipo,
        help_text=eo(u'Tipo de pago, ekz. subvencio, antauxpago, ktp'))
    valuto = models.ForeignKey(Valuto) # XXX default should be EUR
    sumo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text=eo(u'Rabaton enigu kiel normalan pagon, krompagon '
                     u'enigu kun minusan sumon'))
    dato = NeEstontecaDato(error_messages={'estonteco':
        u'Pago ne povas esti en la estonteco.'})
    rimarko = models.CharField(blank=True, max_length=255)
        # uzu ekz. por indiki peranton

    def __unicode__(self):
        return eo(u'{} {} ({}) de {} je {}'.format(
            self.sumo, self.valuto, self.pagtipo, self.partoprenanto,
            self.dato))
    class Meta:
        verbose_name_plural = eo('Pagoj')

class MinimumaAntaupago(models.Model):
    '''Minimuma antaŭpago por partopreni'''
    #kotizosistemo = models.ForeignKey(KotizoSistemo)
    landokategorio = models.ForeignKey(LandoKategorio)
    oficiala_antaupago = models.DecimalField(eo('Oficiala antauxpago'),
        max_digits=8, decimal_places=2,
        help_text=eo('La sumon, kiun ni montras oficiale'))
    interna_antaupago = models.DecimalField(eo('Interna antauxpago'),
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text=eo('La sumon, kiun ni uzas por internaj kalkuloj, se alia'))
    # Kion ni montras ekstere kaj kion ni uzas por internaj kalkuloj
    def __unicode__(self):
        return eo(u'{} EUR por {}'.format(
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
    #renkontigho = models.ForeignKey(Renkontigho)
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

#class AghKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

#class AlighKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

#class LandoKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

#class LandoKategoriLigo(models.Model):
    #lando = models.ForeignKey(Lando)
    #kategorio = models.ForeignKey(LandoKategorio)

#class LoghKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

#class KotizoSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()
    #alighkategorisistemo = models.ForeignKey(AlighKategoriSistemo)
    #landokategorisistemo = models.ForeignKey(LandoKategoriSistemo)
    #aghkategorisistemo = models.ForeignKey(AghKategoriSistemo)
    #loghkategorisistemo = models.ForeignKey(LoghKategoriSistemo)
    #parttempdivisoro = models.FloatField()
    #malalighkondichsistemo = models.IntegerField() # XXX

#class KostoSistemo(models.Model): # XXX what is this for?
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

#class Renkontigho(models.Model):
    #nomo = models.CharField(max_length=255, unique=True)
    #mallongigo = models.CharField(max_length=30, unique=True)
    #temo = models.CharField(max_length=255)
    #loko = models.CharField(max_length=255)
    #de = models.DateField()
    #ghis = models.DateField()
    #kotizosistemo = models.ForeignKey(KotizoSistemo)
    #parttemppartoprendivido = models.IntegerField()

#class Kotizero(models.Model):
    ## ghenerala rabato au krompago au ero de normala kotizo,
    ##   aplikebla al pluraj partoprenantoj lau difinita kondicho
    #nomo = models.CharField(unique=True, max_length=50)
    #priskribo = models.TextField(blank=True)
    #kondicho = models.TextField(
        #help_text=eo('kondicxo, kiu difinas, cxu tiu cxi kotizero aplikigxas '
                     #'al specifa partoprenanto'))
        ## will be a python expression evaluating to whether this applies
    #kvanto = models.DecimalField(max_digits=8, decimal_places=2,
        #help_text=eo('Povas esti elcento aux sumo en EUR'))
    ##valuto = models.CharField(max_length=3, blank=True)
    ## devas estis EUR
    #def chu_aplikighas(self, partoprenanto):
        #'''kontrolu chu tiu chi kotizero aplikighas al
        #la donita partoprenanto'''
        #return eval(self.kondicho, {'partoprenanto': partoprenanto})
    #def javascript(self):
        #'''revenigi jhavaskriptajhon por kontroli, chu la kondicho aplikighas
        #al specifa homo (por enkrozila kontrolo)'''
        #subs = {'and': '&&', 'or': '||'}
        #k = re.sub(r'\b(?:and|or)\b',
                   #lambda m: subs[m.group(0)], self.kondicho)
        #return 'function (partoprenanto) {\n    return (' + k + ')\n}'
    #def __unicode__(self):
        #return self.nomo
    #class Meta:
        #verbose_name_plural = eo('Kotizeroj')

#class Krompago(models.Model):
    #speco = models.ForeignKey(Kotizero)
    ##kotizosistemo = models.ForeignKey(KotizoSistemo)
    #kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    #valuto = models.CharField(max_length=3, blank=True)

#class KrompagoRegulo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #mallongigo = models.CharField(max_length=30)
    #priskribo = models.TextField()
    #kondicho = models.ForeignKey(Kondicho)
    #uzebla = models.BooleanField()
    #launokte = models.BooleanField()

#class RegulaKrompago(models.Model):
    #regulo = models.ForeignKey(KrompagoRegulo)
    ##kotizosistemo = models.ForeignKey(KotizoSistemo)
    #kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    #valuto = models.CharField(max_length=9)

#class IndividuaKrompago(models.Model):
    #partopreno = models.ForeignKey(Partopreno)
    #valuto = models.CharField(max_length=9)
    #kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    #dato = models.DateField()
    #tipo = models.CharField(max_length=300)

#class IndividuaRabato(models.Model):
    #partopreno = models.ForeignKey(Partopreno)
    #valuto = models.CharField(max_length=9)
    #kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    #dato = models.DateField()
    #tipo = models.CharField(max_length=300)

#class InvitLetero(models.Model):
    #pasportnumero = models.CharField(max_length=150)
    #pasporto_valida_de = models.DateField()
    #pasporto_valida_ghis = models.DateField()
    #pasporta_persona_nomo = models.CharField(max_length=150)
    #pasporta_familia_nomo = models.CharField(max_length=150)
    #pasporta_adreso = models.TextField()
    #senda_adreso = models.TextField()
    #senda_faksnumero = models.CharField(max_length=90, blank=True)
    #invitletero_sendota = models.BooleanField()
    #invitletero_sendodato = models.DateField()

#class Fikskostoj(models.Model):
    ## XXX foreign key to kostosistemo but what is a kostosistemo
    #nomo = models.CharField(max_length=60, unique=True)
    #kostosistemo = models.ForeignKey(KostoSistemo)
    #kosto = models.DecimalField(max_digits=9, decimal_places=2)

#class Kondicho(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()
    #kondichoteksto = models.TextField()
    ## jhavaskripta_formo = models.TextField() # XXX say what?

#class KotizoTabelero(models.Model):
    #kotizosistemo = models.ForeignKey(KotizoSistemo)
    #alighkategorio = models.ForeignKey(AlighKategorio)
    #landokategorio = models.ForeignKey(LandoKategorio)
    #aghkategorio = models.ForeignKey(AghKategorio)
    #loghkategorio = models.ForeignKey(LoghKategorio)
    #kotizo = models.DecimalField(max_digits=8, decimal_places=2)

#class PersonKostoTipo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()
    #kondicho = models.CharField(max_length=150)
    #uzebla = models.BooleanField() # chu montri en la ghenerala listo
    #launokte = models.BooleanField() # launokte au unufoje

#class PersonKosto(models.Model):
    #tipo = models.ForeignKey(PersonKostoTipo)
    #kostosistemo = models.ForeignKey(KostoSistemo)
    #maks_haveblaj = models.IntegerField()
    #min_uzendaj = models.IntegerField()
    #kosto_uzata = models.DecimalField(max_digits=8, decimal_places=2)
    #kosto_neuzata = models.DecimalField(max_digits=8, decimal_places=2)

#class Litonokto(models.Model): # XXX how is this supposed to work?
    #chambro = models.ForeignKey(Chambro)
    #litonumero = models.IntegerField()
    #nokto_de = models.IntegerField()
    #nokto_ghis = models.IntegerField()
    #partopreno = models.IntegerField()
    #rezervtipo = models.CharField(max_length=3)

#class MalalighKondichSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()
    #alighkategorisistemo = models.ForeignKey(AlighKategoriSistemo)

#class MalalighKondichoTipo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #mallongigo = models.CharField(max_length=30)
    #priskribo = models.TextField()
    #funkcio = models.CharField(max_length=150)
    #parametro = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)
    #uzebla = models.BooleanField()

#class MalalighKondicho(models.Model):
    #sistemo = models.ForeignKey(MalalighKondichSistemo)
    #alighkategorio = models.ForeignKey(AlighKategorio)
    #kondichtipo = models.ForeignKey(MalalighKondichoTipo)

    
#class NotojPorEntajpanto(models.Model): # shajne por ligi notojn kun uzulojn
    #noto = models.ForeignKey(Noto)
    #entajpanto = models.IntegerField(db_column='entajpantoID')

#class ParttempKotizoSistemo(models.Model):
    #baza_kotizosistemo = models.ForeignKey(KotizoSistemo)
    #por_noktoj = models.IntegerField(unique=True)
        ## tiom da noktoj oni rajtas resti en tiu tarifo
    #kondicho = models.IntegerField(unique=True) # XXX what is this?
        ## Tiu kondicho aldone devas esti plenumita
        ## XXX Prob should be a foreign key to Kondicho
    #faktoro = models.DecimalField(max_digits=8, decimal_places=2)
        ## ni obligas la kotizojn de la elektita sistemo per tiu faktoro.
    #sub_kotizosistemo = models.ForeignKey(KotizoSistemo)
        ## la kotizoj de tiu sistemo estos uzataj

#class Protokolo(models.Model):
    #deveno = models.CharField(max_length=600)
    #ilo = models.CharField(max_length=600)
    #entajpanto = models.CharField(max_length=60)
    #tempo = models.DateTimeField()
    #ago = models.CharField(max_length=60)

#class Teksto(models.Model):  # XXX temo (ekz. por retposhtajhoj)?
    ##renkontigho = models.ForeignKey(Renkontigho)
    #mesagho = models.CharField(max_length=90, unique=True)
    #teksto = models.TextField()

# -------------------------

#class Monujo(models.Model): # XXX kio estas ties celo?
    #renkontigho = models.ForeignKey(Renkontigho)
    #kvanto = models.IntegerField()
    #kauzo = models.CharField(max_length=600)
    #tempo = models.DateTimeField()
    #kvitanconumero = models.IntegerField()
    #alkiu = models.CharField(max_length=60)
    #kiamonujo = models.CharField(max_length=30)

#class Renkkonfiguroj(models.Model):
    #renkontigho = models.ForeignKey(Renkontighoj)
    #opcioid = models.CharField(max_length=90, unique=True)
        ## XXX what's an opcio?
    #valoro = models.TextField()

#class RenkontighaKonfiguro(models.Model): # XXX what for?
    #renkontigho = models.ForeignKey(Renkontigho)
    #tipo = models.CharField(max_length=60, unique=True)
    #interna = models.CharField(max_length=60, unique=True)
    #grupo = models.IntegerField()
    #teksto = models.CharField(max_length=300)
    #aldona_komento = models.CharField(max_length=300)

#class Sercho(models.Model):
    #nomo = models.CharField(max_length=150, unique=True)
    #priskribo = models.TextField()
    #sercho = models.TextField()
