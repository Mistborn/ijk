# -*- encoding: utf-8 -*-
import datetime
import urllib
import json

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# uearezultoj = [
    # (False, u'Nekonata UEA-kodo aŭ nekongrua lando'),
    # (True, u'UEA-kodo ekzistas kaj kongruas kun la lando'),
    # (False, u'Nevalida UEA-kodo'),
# ]

# def ueakonformas(kodo, lando):
    # if not kodo or not lando:
        # return
    # url = 'http://db.uea.org/alighoj/kontr.php?la={}_{}'.format(
        # kodo.lower(), lando.lower())
    # try:
        # r = int(urllib.urlopen(url).read().strip())
    # except ValueError:
        # return None
    # return uearezultoj[r]

def nonfuturedatevalidator(date):
    if date > datetime.date.today():
        raise ValidationError('La dato ne povas esti en la estonteco',
                              code='estonteco')

def naskighdato(date):
    nonfuturedatevalidator(date)
    if date < datetime.date(1914, 1, 1):
        raise ValidationError(
            u'La naskiĝdato ne povas esti antaŭ la 1-a de januaro, 1914',
            code=u'naskighdato')
    if date > datetime.date(2011, 12, 31):
        raise ValidationError(
            u'La naskiĝdato ne povas esti post 2011',
            code=u'naskighdato')

ueakodo_validator = RegexValidator(r'^[a-zA-Z]{4}\-[a-zA-Z]$',
    u'Malĝusta formato. '
        u'UEA-kodo konsistas el 4 literoj, divido-streko, kaj 1 litero.',
    'ueakodo')

telefono_validator = RegexValidator('^\+[1-9]{1}[ -]?([0-9][ -]?){6,12}$',
    # r'^\+[1-9]\d{0,2}(?:-[0-9]+)+$',
    u'Malbona formato de telefonnumero. '
    u'Bonvolu uzi +[lando-kodo]-[prefikso]-[numero].',
    u'telefono')

skype_regex_validator = RegexValidator(r'^[a-zA-Z][a-zA-Z0-9.,_-]{5,31}$',
     "Nevalida valoro por skype-nomo.", 'skype_form')

def skype_validator(value):
    skype_regex_validator(value)
    url = ('https://login.skype.com/json/validator?'
           'new_username={}'.format(value))
    result = json.loads(urllib.urlopen(url).read())
    if not (str(result['status']) == '406' and
            result['data']['markup'] == "Skype Name not available"):
        raise ValidationError('Tiu Skype-nomo ne ekzistas', code='skype')

nomo_validator = RegexValidator(r"(?u)^([^\W\d_]|[ '-])+$",
    "Enigu nur literojn, spacetojn, apostrofon, kaj divido-strekon",
    'nomo')

shildlando_validator = RegexValidator(r"(?u)^([^\W\d_]|[ .()'-])+$",
    "Enigu nur literojn, spacetojn, punkton, krampojn, apostrofon, "
    "kaj divido-strekon",
    'shildlando')

kromnomo_validator = RegexValidator(u"(?u)^[\w .'_!?-]+$",
    u'Enigu validan valoron. '
    u'Validas nur literoj, ciferoj, spaceto, kaj simboloj el inter .\'-_!?',
    'kromnomo')  # nur literoj [unikode], ciferoj, spaco, punkto, ', -, _, !, ?

poshtkodo_validator = RegexValidator(u'^[A-Z0-9 -]+$',
    'Enigu validan valoron. '
    'Validas majusklaj literoj, ciferoj, spaceto, kaj divido-streko',
    'poshtkodo')

def havebla_loghkategorio(obj):
    if not obj.chu_havebla:
        raise ValidationError(u'Ne plu restas lokoj. '
                              u'Bonvolu elekti alian loĝkategorion.',
                              code='nehavebla')

