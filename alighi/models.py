# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class IjkAgxkategorioj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    priskribo = models.TextField()
    sistemoid = models.IntegerField(unique=True, db_column='sistemoID') # Field name made lowercase.
    limagxo = models.IntegerField()
    class Meta:
        db_table = u'ijk_agxkategorioj'

class IjkAgxkategorisistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    class Meta:
        db_table = u'ijk_agxkategorisistemoj'

class IjkAligxkategorioj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    priskribo = models.TextField()
    sistemoid = models.IntegerField(unique=True, db_column='sistemoID') # Field name made lowercase.
    limdato = models.IntegerField()
    nomo_lokalingve = models.CharField(max_length=60)
    class Meta:
        db_table = u'ijk_aligxkategorioj'

class IjkAligxkategorisistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    class Meta:
        db_table = u'ijk_aligxkategorisistemoj'

class IjkCxambroj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    renkontigxo = models.IntegerField(unique=True)
    nomo = models.CharField(max_length=60, unique=True)
    etagxo = models.CharField(max_length=150)
    litonombro = models.IntegerField()
    tipo = models.CharField(max_length=3)
    dulita = models.CharField(max_length=3)
    rimarkoj = models.CharField(max_length=300)
    class Meta:
        db_table = u'ijk_cxambroj'

class IjkEntajpantoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=150, unique=True)
    kodvorto = models.CharField(max_length=150)
    sendanto_nomo = models.CharField(max_length=90)
    retposxtadreso = models.CharField(max_length=150)
    partoprenanto_id = models.IntegerField(null=True, blank=True)
    aligi = models.CharField(max_length=3)
    vidi = models.CharField(max_length=3)
    sxangxi = models.CharField(max_length=3)
    cxambrumi = models.CharField(max_length=3)
    ekzporti = models.CharField(max_length=3)
    statistikumi = models.CharField(max_length=3)
    mono = models.CharField(max_length=3)
    estingi = models.CharField(max_length=3)
    retumi = models.CharField(max_length=3)
    rabati = models.CharField(max_length=3)
    inviti = models.CharField(max_length=3)
    administri = models.CharField(max_length=3)
    akcepti = models.CharField(max_length=3)
    teknikumi = models.CharField(max_length=3)
    class Meta:
        db_table = u'ijk_entajpantoj'

class IjkFikskostoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    kostosistemo = models.IntegerField(unique=True)
    kosto = models.DecimalField(max_digits=9, decimal_places=2)
    class Meta:
        db_table = u'ijk_fikskostoj'

class IjkIndividuajKrompagoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    partoprenoid = models.IntegerField(db_column='partoprenoID') # Field name made lowercase.
    valuto = models.CharField(max_length=9)
    kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    dato = models.DateField()
    tipo = models.CharField(max_length=300)
    entajpantoid = models.IntegerField(db_column='entajpantoID') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_individuaj_krompagoj'

class IjkIndividuajRabatoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    partoprenoid = models.IntegerField(db_column='partoprenoID') # Field name made lowercase.
    valuto = models.CharField(max_length=9)
    kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    dato = models.DateField()
    tipo = models.CharField(max_length=300)
    entajpantoid = models.IntegerField(db_column='entajpantoID') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_individuaj_rabatoj'

class IjkInvitpetoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    pasportnumero = models.CharField(max_length=150)
    pasporto_valida_de = models.DateField()
    pasporto_valida_gxis = models.DateField()
    pasporta_persona_nomo = models.CharField(max_length=150)
    pasporta_familia_nomo = models.CharField(max_length=150)
    pasporta_adreso = models.TextField()
    senda_adreso = models.TextField()
    senda_faksnumero = models.CharField(max_length=90, blank=True)
    invitletero_sendenda = models.CharField(max_length=3)
    invitletero_sendodato = models.DateField()
    class Meta:
        db_table = u'ijk_invitpetoj'

class IjkKategoriojDeLandoj(models.Model):
    sistemoid = models.IntegerField(primary_key=True, db_column='sistemoID') # Field name made lowercase.
    landoid = models.IntegerField(primary_key=True, db_column='landoID') # Field name made lowercase.
    kategorioid = models.IntegerField(db_column='kategorioID') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_kategorioj_de_landoj'

class IjkKondicxoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    kondicxoteksto = models.TextField()
    jxavaskripta_formo = models.TextField()
    class Meta:
        db_table = u'ijk_kondicxoj'

class IjkKostosistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    priskribo = models.TextField()
    entajpanto = models.IntegerField()
    class Meta:
        db_table = u'ijk_kostosistemoj'

class IjkKotizosistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    priskribo = models.TextField()
    entajpanto = models.IntegerField()
    aligxkategorisistemo = models.IntegerField()
    landokategorisistemo = models.IntegerField()
    agxkategorisistemo = models.IntegerField()
    logxkategorisistemo = models.IntegerField()
    parttempdivisoro = models.FloatField()
    malaligxkondicxsistemo = models.IntegerField()
    class Meta:
        db_table = u'ijk_kotizosistemoj'

class IjkKotizotabeleroj(models.Model):
    kotizosistemo = models.IntegerField(primary_key=True)
    aligxkategorio = models.IntegerField(primary_key=True)
    landokategorio = models.IntegerField(primary_key=True)
    agxkategorio = models.IntegerField(primary_key=True)
    logxkategorio = models.IntegerField(primary_key=True)
    kotizo = models.DecimalField(max_digits=8, decimal_places=2)
    class Meta:
        db_table = u'ijk_kotizotabeleroj'

class IjkKrompagoreguloj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    mallongigo = models.CharField(max_length=30)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    kondicxo = models.IntegerField()
    uzebla = models.CharField(max_length=3)
    lauxnokte = models.CharField(max_length=3)
    class Meta:
        db_table = u'ijk_krompagoreguloj'

class IjkKurzoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    valuto = models.CharField(max_length=9, unique=True)
    dato = models.DateField(unique=True)
    kurzo = models.DecimalField(max_digits=12, decimal_places=5)
    class Meta:
        db_table = u'ijk_kurzoj'

class IjkLandoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60)
    kodo = models.CharField(max_length=6)
    class Meta:
        db_table = u'ijk_landoj'

class IjkLandokategorioj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    priskribo = models.TextField()
    sistemoid = models.IntegerField(unique=True, db_column='sistemoID') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_landokategorioj'

class IjkLandokategorisistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    class Meta:
        db_table = u'ijk_landokategorisistemoj'

class IjkLitonoktoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    cxambro = models.IntegerField()
    litonumero = models.IntegerField()
    nokto_de = models.IntegerField()
    nokto_gxis = models.IntegerField()
    partopreno = models.IntegerField()
    rezervtipo = models.CharField(max_length=3)
    class Meta:
        db_table = u'ijk_litonoktoj'

class IjkLogxkategorioj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    priskribo = models.TextField()
    sistemoid = models.IntegerField(unique=True, db_column='sistemoID') # Field name made lowercase.
    kondicxo = models.IntegerField()
    class Meta:
        db_table = u'ijk_logxkategorioj'

class IjkLogxkategorisistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    class Meta:
        db_table = u'ijk_logxkategorisistemoj'

class IjkMalaligxkondicxoj(models.Model):
    sistemo = models.IntegerField(primary_key=True)
    aligxkategorio = models.IntegerField(primary_key=True)
    kondicxtipo = models.IntegerField()
    class Meta:
        db_table = u'ijk_malaligxkondicxoj'

class IjkMalaligxkondicxotipoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    mallongigo = models.CharField(max_length=30)
    priskribo = models.TextField()
    funkcio = models.CharField(max_length=150)
    parametro = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)
    uzebla = models.CharField(max_length=3)
    class Meta:
        db_table = u'ijk_malaligxkondicxotipoj'

class IjkMalaligxkondicxsistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    priskribo = models.TextField()
    aligxkategorisistemo = models.IntegerField()
    class Meta:
        db_table = u'ijk_malaligxkondicxsistemoj'

class IjkMinimumajAntauxpagoj(models.Model):
    kotizosistemo = models.IntegerField(primary_key=True)
    landokategorio = models.IntegerField(primary_key=True)
    oficiala_antauxpago = models.DecimalField(max_digits=8, decimal_places=2)
    interna_antauxpago = models.DecimalField(max_digits=8, decimal_places=2)
    class Meta:
        db_table = u'ijk_minimumaj_antauxpagoj'

class IjkMonujo(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    renkontigxo = models.IntegerField()
    kvanto = models.IntegerField()
    kauzo = models.CharField(max_length=600)
    tempo = models.DateTimeField()
    kvitanconumero = models.IntegerField()
    alkiu = models.CharField(max_length=60, db_column='alKiu') # Field name made lowercase.
    kiamonujo = models.CharField(max_length=30, db_column='kiaMonujo') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_monujo'

class IjkNomsxildoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    titolo_lokalingve = models.CharField(max_length=45)
    titolo_esperante = models.CharField(max_length=45)
    nomo = models.CharField(max_length=90)
    funkcio_lokalingve = models.CharField(max_length=120)
    funkcio_esperante = models.CharField(max_length=120)
    renkontigxoid = models.IntegerField(db_column='renkontigxoID') # Field name made lowercase.
    havasnomsxildon = models.CharField(max_length=3, db_column='havasNomsxildon') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_nomsxildoj'

class IjkNotoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    partoprenantoid = models.IntegerField(db_column='partoprenantoID') # Field name made lowercase.
    kiu = models.CharField(max_length=300)
    kunkiu = models.CharField(max_length=300, db_column='kunKiu') # Field name made lowercase.
    tipo = models.CharField(max_length=30)
    dato = models.DateTimeField()
    subjekto = models.CharField(max_length=300)
    enhavo = models.TextField()
    prilaborata = models.CharField(max_length=3)
    revidu = models.DateTimeField()
    class Meta:
        db_table = u'ijk_notoj'

class IjkNotojPorEntajpantoj(models.Model):
    notoid = models.IntegerField(db_column='notoID') # Field name made lowercase.
    entajpantoid = models.IntegerField(db_column='entajpantoID') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_notoj_por_entajpantoj'

class IjkPagoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    partoprenoid = models.IntegerField(db_column='partoprenoID') # Field name made lowercase.
    valuto = models.CharField(max_length=9)
    kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    dato = models.DateField()
    tipo = models.CharField(max_length=300)
    entajpantoid = models.IntegerField(db_column='entajpantoID') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_pagoj'

class IjkPartoprenantoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=150)
    personanomo = models.CharField(max_length=150)
    sxildnomo = models.CharField(max_length=150)
    sekso = models.CharField(max_length=3)
    naskigxdato = models.DateField()
    adresaldonajxo = models.CharField(max_length=150)
    strato = models.CharField(max_length=150)
    provinco = models.CharField(max_length=150)
    posxtkodo = models.CharField(max_length=150)
    urbo = models.CharField(max_length=150)
    lando = models.IntegerField()
    sxildlando = models.CharField(max_length=150)
    telefono = models.CharField(max_length=150)
    telefakso = models.CharField(max_length=150)
    retposxto = models.CharField(max_length=150)
    retposxta_varbado = models.CharField(max_length=3)
    ueakodo = models.CharField(max_length=18)
    class Meta:
        db_table = u'ijk_partoprenantoj'

class IjkPartoprenoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    renkontigxoid = models.IntegerField(db_column='renkontigxoID') # Field name made lowercase.
    partoprenantoid = models.IntegerField(db_column='partoprenantoID') # Field name made lowercase.
    ordigoid = models.DecimalField(decimal_places=3, max_digits=11, db_column='ordigoID') # Field name made lowercase.
    agxo = models.IntegerField()
    nivelo = models.CharField(max_length=3)
    rimarkoj = models.TextField()
    retakonfirmilo = models.CharField(max_length=3)
    germanakonfirmilo = models.CharField(max_length=3)
    number_1akonfirmilosendata = models.DateField(db_column=u'1akonfirmilosendata') # Field renamed because it wasn't a valid Python identifier.
    number_2akonfirmilosendata = models.DateField(db_column=u'2akonfirmilosendata') # Field renamed because it wasn't a valid Python identifier.
    partoprentipo = models.CharField(max_length=3)
    de = models.DateField()
    gxis = models.DateField()
    vegetare = models.CharField(max_length=3)
    gejmembro = models.CharField(max_length=3, db_column='GEJmembro') # Field name made lowercase.
    surloka_membrokotizo = models.CharField(max_length=3)
    membrokotizo = models.DecimalField(max_digits=8, decimal_places=2)
    tejo_membro_laudire = models.CharField(max_length=3)
    tejo_membro_kontrolita = models.CharField(max_length=3)
    tejo_membro_kotizo = models.DecimalField(max_digits=8, decimal_places=2)
    kkren = models.CharField(max_length=3, db_column='KKRen') # Field name made lowercase.
    domotipo = models.CharField(max_length=3)
    kunmangxas = models.CharField(max_length=3)
    listo = models.CharField(max_length=3)
    intolisto = models.CharField(max_length=3)
    pagmaniero = models.CharField(max_length=90)
    antauxpago_gxis = models.DateField()
    kunkiu = models.CharField(max_length=150, db_column='kunKiu') # Field name made lowercase.
    kunkiuid = models.IntegerField(db_column='kunKiuID') # Field name made lowercase.
    cxambrotipo = models.CharField(max_length=3)
    dulita = models.CharField(max_length=3)
    tema = models.TextField()
    distra = models.TextField()
    vespera = models.TextField()
    muzika = models.TextField()
    nokta = models.TextField()
    aligxdato = models.DateField()
    malaligxdato = models.DateField()
    aligxkategoridato = models.DateField()
    alvenstato = models.CharField(max_length=3)
    asekuri = models.CharField(max_length=3)
    havas_asekuron = models.CharField(max_length=3)
    kontrolata = models.CharField(max_length=3)
    havasmangxkuponon = models.CharField(max_length=3, db_column='havasMangxkuponon') # Field name made lowercase.
    havasnomsxildon = models.CharField(max_length=3, db_column='havasNomsxildon') # Field name made lowercase.
    class Meta:
        db_table = u'ijk_partoprenoj'

class IjkParttempkotizosistemoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    baza_kotizosistemo = models.IntegerField(unique=True)
    por_noktoj = models.IntegerField(unique=True)
    kondicxo = models.IntegerField(unique=True)
    faktoro = models.DecimalField(max_digits=8, decimal_places=2)
    sub_kotizosistemo = models.IntegerField()
    class Meta:
        db_table = u'ijk_parttempkotizosistemoj'

class IjkPersonkostoj(models.Model):
    tipo = models.IntegerField(primary_key=True)
    kostosistemo = models.IntegerField(primary_key=True)
    maks_haveblaj = models.IntegerField()
    min_uzendaj = models.IntegerField()
    kosto_uzata = models.DecimalField(max_digits=8, decimal_places=2)
    kosto_neuzata = models.DecimalField(max_digits=8, decimal_places=2)
    class Meta:
        db_table = u'ijk_personkostoj'

class IjkPersonkostotipoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    kondicxo = models.CharField(max_length=150)
    uzebla = models.CharField(max_length=3)
    lauxnokte = models.CharField(max_length=3)
    class Meta:
        db_table = u'ijk_personkostotipoj'

class IjkProtokolo(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    deveno = models.CharField(max_length=600)
    ilo = models.CharField(max_length=600)
    entajpanto = models.CharField(max_length=60)
    tempo = models.DateTimeField()
    ago = models.CharField(max_length=60)
    class Meta:
        db_table = u'ijk_protokolo'

class IjkRabatoreguloj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    mallongigo = models.CharField(max_length=30)
    entajpanto = models.IntegerField()
    priskribo = models.TextField()
    kondicxo = models.IntegerField()
    uzebla = models.CharField(max_length=3)
    lauxnokte = models.CharField(max_length=3)
    class Meta:
        db_table = u'ijk_rabatoreguloj'

class IjkRegulajKrompagoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    regulo = models.IntegerField(unique=True)
    kotizosistemo = models.IntegerField(unique=True)
    kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    valuto = models.CharField(max_length=9)
    class Meta:
        db_table = u'ijk_regulaj_krompagoj'

class IjkRegulajRabatoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    regulo = models.IntegerField(unique=True)
    kotizosistemo = models.IntegerField(unique=True)
    kvanto = models.DecimalField(max_digits=8, decimal_places=2)
    valuto = models.CharField(max_length=9)
    class Meta:
        db_table = u'ijk_regulaj_rabatoj'

class IjkRenkkonfiguroj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    renkontigxoid = models.IntegerField(unique=True, db_column='renkontigxoID') # Field name made lowercase.
    opcioid = models.CharField(max_length=90, unique=True, db_column='opcioID') # Field name made lowercase.
    valoro = models.TextField()
    class Meta:
        db_table = u'ijk_renkkonfiguroj'

class IjkRenkontigxajKonfiguroj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    renkontigxoid = models.IntegerField(unique=True, db_column='renkontigxoID') # Field name made lowercase.
    tipo = models.CharField(max_length=60, unique=True)
    interna = models.CharField(max_length=60, unique=True)
    grupo = models.IntegerField()
    teksto = models.CharField(max_length=300)
    aldona_komento = models.CharField(max_length=300)
    class Meta:
        db_table = u'ijk_renkontigxaj_konfiguroj'

class IjkRenkontigxo(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=300, unique=True)
    mallongigo = models.CharField(max_length=30, unique=True)
    temo = models.CharField(max_length=300)
    loko = models.CharField(max_length=300)
    de = models.DateField()
    gxis = models.DateField()
    kotizosistemo = models.IntegerField()
    plej_frue = models.DateField()
    meze = models.DateField()
    malfrue = models.DateField()
    parttemppartoprendivido = models.IntegerField()
    juna = models.IntegerField()
    maljuna = models.IntegerField()
    adminrespondeculo = models.CharField(max_length=150)
    adminretadreso = models.CharField(max_length=300)
    sekurkopiojretadreso = models.CharField(max_length=300)
    invitleterorespondeculo = models.CharField(max_length=150)
    invitleteroretadreso = models.CharField(max_length=300)
    temarespondulo = models.CharField(max_length=150)
    temaretadreso = models.CharField(max_length=300)
    distrarespondulo = models.CharField(max_length=150)
    distraretadreso = models.CharField(max_length=300)
    vesperarespondulo = models.CharField(max_length=150)
    vesperaretadreso = models.CharField(max_length=300)
    muzikarespondulo = models.CharField(max_length=150)
    muzikaretadreso = models.CharField(max_length=300)
    noktarespondulo = models.CharField(max_length=150)
    noktaretadreso = models.CharField(max_length=300)
    novularespondulo = models.CharField(max_length=150)
    novularetadreso = models.CharField(max_length=300)
    class Meta:
        db_table = u'ijk_renkontigxo'

class IjkRetposxto(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=60, unique=True)
    subjekto = models.CharField(max_length=300)
    korpo = models.TextField()
    class Meta:
        db_table = u'ijk_retposxto'

class IjkSercxoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    nomo = models.CharField(max_length=150, unique=True)
    priskribo = models.TextField()
    entajpanto = models.IntegerField()
    sercxo = models.TextField()
    class Meta:
        db_table = u'ijk_sercxoj'

class IjkTekstoj(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    renkontigxoid = models.IntegerField(unique=True, db_column='renkontigxoID') # Field name made lowercase.
    mesagxoid = models.CharField(max_length=90, unique=True, db_column='mesagxoID') # Field name made lowercase.
    teksto = models.TextField()
    class Meta:
        db_table = u'ijk_tekstoj'

class IjkTempTradukoj(models.Model):
    dosiero = models.CharField(max_length=300, primary_key=True)
    cheno = models.CharField(max_length=765, primary_key=True)
    class Meta:
        db_table = u'ijk_temp_tradukoj'

class IjkTradukoj(models.Model):
    dosiero = models.CharField(max_length=300)
    cheno = models.CharField(max_length=765, primary_key=True)
    iso2 = models.CharField(max_length=15)
    traduko = models.TextField()
    tradukinto = models.CharField(max_length=765, blank=True)
    komento = models.TextField()
    stato = models.IntegerField()
    dato = models.DateTimeField()
    class Meta:
        db_table = u'ijk_tradukoj'

