# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

SEKSOJ = (
    ('v', 'vira'),
    ('i', 'ina'),
    ('a', 'alia'),
)

# XXX help text for each field
# XXX check defaults and nulls for ecah field

#class Respondeculo(models.Model): # XXX should be a user here
    #nomo = models.CharField(unique=True)
    #retposhtadreso = models.EmailField()

class Respondeco(models.Model):
    rolo = models.CharField(max_length=50)
    uzanto = models.ForeignKey(User)
    def __unicode__(self):
        return self.rolo
    class Meta:
        verbose_name_plural = 'Respondecoj'

class Valuto(models.Model):
    kodo = models.CharField(max_length=3)
    nomo = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.kodo
    class Meta:
        verbose_name_plural = 'Valutoj'
        
class Kurzo(models.Model):
    valuto = models.ForeignKey(Valuto)
    dato = models.DateField()
    kurzo = models.DecimalField(max_digits=12, decimal_places=5)
    # *** de la donita valuto al EUR
    def __unicode__(self):
        return u'Kurzo por {} je {}'.format(self.valuto, self.dato)
    class Meta:
        unique_together = ('valuto', 'dato')
        verbose_name_plural = 'Kurzoj'
        
#class AghKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

class AghKategorio(models.Model):
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(AghKategoriSistemo)
    limagho = models.IntegerField(
        help_text='Partoprenanto kun agho ghis tiu chi agho '
                  'eniras tiun chi kategorion')
    def __unicode__(self):
        return u'Aghkategorio ' + self.nomo
    class Meta:
        verbose_name_plural = 'Aghkategorioj'

#class AlighKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

class AlighKategorio(models.Model):
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(AlighKategoriSistemo)
    limdato = models.DateField(
        help_text='Partoprenanto, kiu alighas ghis tiu chi dato '
                  'eniras tiun chi kategorion')
    def __unicode__(self):
        return u'Alighkategorio ' + self.nomo
    class Meta:
        verbose_name_plural = 'Alighkategorioj'

class LandoKategorio(models.Model):
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(LandoKategoriSistemo)
    def __unicode__(self):
        return u'Landokategorio ' + self.nomo
    class Meta:
        verbose_name_plural = 'Landokategorioj'

class Lando(models.Model):
    nomo = models.CharField(max_length=50)
    kodo = models.CharField(max_length=2)
    kategorio = models.ForeignKey(LandoKategorio)
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Landoj'

#class LandoKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()

#class LandoKategoriLigo(models.Model):
    #lando = models.ForeignKey(Lando)
    #kategorio = models.ForeignKey(LandoKategorio)
    
#class LoghKategoriSistemo(models.Model):
    #nomo = models.CharField(max_length=60, unique=True)
    #priskribo = models.TextField()
    
class LoghKategorio(models.Model):
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    #sistemo = models.ForeignKey(LoghKategoriSistemo)
    #kondicho = models.IntegerField()
    plena_kosto = models.DecimalField(max_digits=8, decimal_places=2,
        help_text='Kosto por logho dum la tuta kongreso')
    unutaga_kosto = models.DecimalField(max_digits=8, decimal_places=2,
        help_text='Kosto por logho dum unu nokto')
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Loghkategorioj'

class ManghoMendo(models.Model):
    nomo = models.CharField(unique=True, max_length=50)
    # memzorge/matenmangho/tagmangho/vespermangho
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Manghomendoj'

class ManghoTipo(models.Model):
    nomo = models.CharField(unique=True, max_length=50)
    # vegetare/vegare/ktp
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Manghotipoj'

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

class Kotizero(models.Model):
    # ghenerala rabato au krompago au ero de normala kotizo,
    #   aplikebla al pluraj partoprenantoj lau difinita kondicho
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    kondicho = models.TextField(
        help_text='kondicho, kiu difinas, chu tiu chi kotizero aplikighas '
                  'al specifa partoprenanto')
        # will be a python expression evaluating to whether this applies
    kvanto = models.DecimalField(max_digits=8, decimal_places=2,
        help_text='Povas esti elcento au sumo en EUR')
    #valuto = models.CharField(max_length=3, blank=True)
    # devas estis EUR
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Kotizeroj'
    
class Pagmaniero(models.Model):
    # maniero transdoni monon, ekz. per peranto, surloke, unuopula rabato, ktp
    nomo = models.CharField(unique=True, max_length=50)
    priskribo = models.TextField(blank=True)
    chu_publika = models.BooleanField(default=False,
        help_text='Chu tiu chi pagmaniero estu elektebla por indiki, '
                  'kiel oni intencas pagi la antaupagon')
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Pagmanieroj'

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

class Retposhtajho(models.Model):
    # por amase senditaj retposhtajhoj
    nomo = models.CharField(unique=True, max_length=50)
    temo = models.CharField(max_length=100)
    teksto = models.TextField()
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Retposhtajhoj'

class SurlokMembrighaKategorio(models.Model):
    # por registri surlokajn membrighojn en uea/tejo
    nomo = models.CharField(unique=True, max_length=50,
        help_text='Nomo de la kategorio de surloka membrigho en TEJO/UEA')
    kotizo = models.DecimalField(max_digits=8, decimal_places=2,
        help_text='Sumo de la kotizo')
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name = 'Surlokmembrigha Kategorio'
        verbose_name_plural = 'Surlokmembrighaj Kategorioj'

class Chambro(models.Model): # unuopa chambro por disdoni
    #renkontigho = models.ForeignKey(Renkontigho)
    nomo = models.CharField(unique=True, max_length=50)
    #etagho = models.CharField(max_length=150)
    litonombro = models.IntegerField(help_text='nombro da litoj en la chambro')
        # maksimuma nombro da homoj kiuj povos loghi en tiu chi chambro
    loghkategorio = models.ForeignKey(LoghKategorio)
        # al kiu loghkategorio ghi taugas?
    #dulita = models.CharField(max_length=3)
    rimarko = models.CharField(blank=True, max_length=255)
    def __unicode__(self):
        return self.nomo
    class Meta:
        verbose_name_plural = 'Chambroj'

class Partoprenanto(models.Model):
    persona_nomo = models.CharField(max_length=50)
    familia_nomo = models.CharField(max_length=50)
    retposhto = models.EmailField()
    mesaghiloj = models.TextField(blank=True,
        help_text='Aliaj mesaghiloj, kiujn vi volas aperigi en la '
                  'postkongresa listo de partoprenantoj')
    shildnomo = models.CharField(blank=True, max_length=25)
    sekso = models.CharField(max_length=1, choices=SEKSOJ)
    naskighdato = models.DateField()
    adreso = models.TextField(blank=True)
    urbo = models.CharField(blank=True, max_length=50)
    poshtkodo = models.CharField(blank=True, max_length=15)
    loghlando = models.ForeignKey(Lando)
    shildlando = models.CharField(blank=True, max_length=50)
    telefono = models.CharField(blank=True, max_length=50)
    #fakso = models.CharField(blank=True)
    pagmaniero = models.ForeignKey(Pagmaniero,
        help_text='Kiamaniere vi pagos la antaupagon')
        # el la publikaj pagmanieroj, por la antaupago
    pagmaniera_komento = models.CharField(blank=True, max_length=50)
        # ekz por nomo de peranto
    alvenas_per = models.CharField(blank=True, max_length=255,
        help_text='Ekz. flugnumero, se vi jam scias ghin')
    alvenas_je = models.DateField(null=True)
    foriras_per = models.CharField(blank=True, max_length=255,
        help_text='Ekz. flugnumero, se vi jam scias ghin')
    foriras_je = models.DateField(null=True)
    chu_unua_dua_ijk = models.BooleanField(
        default=False, help_text='Chu via unua au dua IJK?')
    interesighas_pri_antaukongreso = models.IntegerField(null=True)
        # kiom da tagoj
    interesighas_pri_postkongreso = models.IntegerField(null=True)
        # kiom da tagoj
    chu_bezonas_invitleteron = models.BooleanField(
        'Chu vi bezonas invitleteron?', default=False)
    chu_invitletero_sendita = models.BooleanField(default=False)
#class Partopreno(models.Model):
    #renkontigho = models.ForeignKey(Renkontigho)
    #partoprenanto = models.ForeignKey(Partoprenanto)
    ekde = models.DateField('Partoprenos ekde')
    ghis = models.DateField('Partoprenos ghis')
    chu_ueamembro = models.BooleanField(
        default=True, help_text='Mi estas membro de UEA/TEJO')
    uea_kodo = models.CharField('Mia UEA-kodo', max_length=18, blank=True)
    loghkategorio = models.ForeignKey(LoghKategorio)
    chambro = models.ForeignKey(Chambro, blank=True)
    chu_tuttaga_ekskurso = models.BooleanField(
        'Mi alighas al tut-taga ekskurso', default=True)
    manghomendo = models.ForeignKey(ManghoMendo)
    manghotipo = models.ForeignKey(ManghoTipo)
    unua_konfirmilo_sendita = models.DateField(null=True)
    dua_konfirmilo_sendita = models.DateField(null=True)
    deziras_loghi_kun_nomo = models.CharField(
        'Mi deziras loghi kun', blank=True, max_length=50)
    deziras_loghi_kun = models.ForeignKey('Partoprenanto', null=True)
    # chu mi volas aperi en tiaj listoj:
    chu_retalisto = models.BooleanField(default=True,
        help_text='Mi permesas publikigi mian nomon en la reta listo de partoprenantoj')
    chu_postkongresalisto = models.BooleanField(default=True,
        help_text='Mi permesas publikigi mian nomon en la postkongresa listo de partoprenantoj')
    chu_komencanto = models.BooleanField(help_text='Mi estas komencanto', default=True)
    chu_interesighas_pri_kurso = models.BooleanField(default=True,
        help_text='Mi interesighas pri Esperanto-kurso')
    #antaupago_ghis = models.DateField()
    #dulita = models.CharField(max_length=3)
    #tema = models.TextField()
    #distra = models.TextField()
    #vespera = models.TextField()
    #muzika = models.TextField()
    #nokta = models.TextField()
    programa_kontribuo = models.TextField(blank=True,
        help_text='Mi shatus kontribui al la programo jene:')
    organiza_kontribuo = models.TextField(blank=True,
        help_text='Mi shatus kontribui al organizado jene:')
    alighdato = models.DateField(auto_now_add=True)
    malalighdato = models.DateField(null=True)
    #alighkategoridato = models.DateField()
    # informoj por surloka kontrolo:
    chu_alvenis = models.BooleanField(default=False)
    chu_havasmanghkuponon = models.BooleanField(default=False)
    chu_havasnomshildon = models.BooleanField(default=False)
    #rimarkoj = models.TextField()
    #por rimarkoj, vidu la tabelon Noto
        # por pagoj
    chu_surloka_membrigho = models.BooleanField(default=False)
    surlokmembrigha_kategorio = models.ForeignKey(SurlokMembrighaKategorio)
    surlokmembrigha_kotizo = models.DecimalField(max_digits=8, decimal_places=2)

    chu_kontrolita = models.BooleanField(default=False)

    #surloka_membrokotizo = models.CharField(max_length=3)
    #membrokotizo = models.DecimalField(max_digits=8, decimal_places=2)
    #tejo_membro_laudire = models.CharField(max_length=3)
    #tejo_membro_kontrolita = models.CharField(max_length=3)
    #tejo_membro_kotizo = models.DecimalField(max_digits=8, decimal_places=2)
    # XXX membreco
    def __unicode__(self):
        return u'{} {}'.format(self.persona_nomo, self.familia_nomo)
    class Meta:
        verbose_name_plural = 'Partoprenantoj'

class Pago(models.Model):
    partoprenanto = models.ForeignKey(Partoprenanto)
    uzanto = models.ForeignKey(User,
            help_text='Respondeculo, kiu ricevis/notis la pagon')
    pagmaniero = models.ForeignKey(Pagmaniero)
    valuto = models.ForeignKey(Valuto) # XXX default should be EUR
    sumo = models.DecimalField(max_digits=8, decimal_places=2)
    dato = models.DateField()
    rimarko = models.CharField(blank=True, max_length=255) # uzu ekz. por indiki peranton
    def __unicode__(self):
        return u'{} {} de {} je {}'.format(
            self.valuto, self.sumo, self.partoprenanto, self.dato)
    class Meta:
        verbose_name_plural = 'Pagoj'

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

class MinimumaAntaupago(models.Model):
    #kotizosistemo = models.ForeignKey(KotizoSistemo)
    landokategorio = models.ForeignKey(LandoKategorio)
    oficiala_antaupago = models.DecimalField(max_digits=8, decimal_places=2)
    interna_antaupago = models.DecimalField(max_digits=8, decimal_places=2)
    # Kion ni montras ekstere kaj kion ni uzas por internaj kalkuloj
    def __unicode__(self):
        return u'Minimuma antaupago de {} por landkategorio {}'.format(self.oficiala_antaupago, self.landokategorio)
    class Meta:
        verbose_name_plural = 'Minimumaj Antaupagoj'

class Nomshildo(models.Model):
    # specialaj nomshildoj por nepartoprenantoj
    nomo = models.CharField(max_length=50)
    titolo_lokalingve = models.CharField(max_length=50)
    titolo_esperante = models.CharField(max_length=50)
    #funkcio_lokalingve = models.CharField()
    #funkcio_esperante = models.CharField()
    #renkontigho = models.ForeignKey(Renkontigho)
    chu_havasnomshildon = models.BooleanField(default=False)
    def __unicode__(self):
        return u'Nomshildo por ' + self.nomo
    class Meta:
        verbose_name_plural = 'Nomshildoj'

class Noto(models.Model):
    partoprenanto = models.ForeignKey(Partoprenanto, null=True)
    uzanto = models.ForeignKey(User, null=True)
    #kiu = models.CharField(max_length=300) # noto de
    #kunkiu = models.CharField(max_length=300) # pri komunicado kun
    dato = models.DateTimeField(auto_now_add=True)
    #temo = models.CharField()
    enhavo = models.TextField()
    chu_prilaborita = models.BooleanField(default=False)
    revidu = models.DateTimeField(help_text='Kiam memorigi pri tio chi', null=True) # kiam memorigi prie
    def __unicode__(self):
        return u'{}{}'.format(self.enhavo[:27], '...' if len(self.enhavo) > 27 else '')
    class Meta:
        verbose_name_plural = 'Notoj'

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
