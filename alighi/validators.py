# -*- encoding: utf-8 -*-
import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

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
    if date > datetime.date(2007, 12, 31):
        raise ValidationError(
            u'La naskiĝdato ne povas esti post 2007',
            code=u'naskighdato')

ueakodo_validator = RegexValidator(r'^[a-zA-Z]{4}\-[a-zA-Z]$',
    u'Malĝusta formato. '
        u'UEA-kodo konsistas el 4 literoj, divido-streko, kaj 1 litero.',
    'ueakodo')

telefono_validator = RegexValidator('^\+[1-9]{1}[ -]?([0-9][ -]?){6,12}$',
    #r'^\+[1-9]\d{0,2}(?:-[0-9]+)+$',
    u'Malbona formato de telefonnumero. '
    u'Bonvolu uzi +[lando-kodo]-[prefikso]-[numero].',
    u'telefono')

skype_validator = RegexValidator(r'^[a-zA-Z][a-zA-Z0-9.,_-]{5,31}$',
     "Nevalida valoro por skype-nomo.", 'skype')

nomo_validator = RegexValidator(r"(?u)^[a-zA-Z '-]+$",
    "Enigu nur literojn, spacetojn, apostrofo, kaj divido-strekon",
    'nomo')

shildlando_validator = RegexValidator(r"(?u)^[a-zA-Z .,-]+$",
    "Enigu nur literojn, spacetojn, punkton, komon, kaj divido-strekon",
    'shildlando')
    
kromnomo_validator = RegexValidator(u"(?u)^[\w .'_!?-]+$",
    u'Enigu validan valoron. '
    u'Validas nur literoj, ciferoj, spaceto, kaj simboloj el inter .\'-_!?',
    'kromnomo') # nur literoj [unikode], ciferoj, spaco, punkto, ', -, _, !, ?

poshtkodo_validator = RegexValidator(u'^[A-Z0-9 -]+$',
    'Enigu validan valoron. '
    'Validas literoj, ciferoj, spaceto, kaj divido-streko', 'poshtkodo')