# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.forms.models import inlineformset_factory
#from django.forms.widgets import RadioSelect

import models
from utils import eo, KOMENCA_DATO, FINIGHA_DATO, SEKSOJ, DATE_JAVASCRIPT

default_error_messages = {
    'required': eo(u'Cxi tiu kampo estas deviga.'),
    'invalid': eo(u'Enigu validan valoron.'),
    'min_length': eo(u'Certigu, ke tiu cxi valoro havas almenaux %(limit_value)d signojn (gxi havas %(show_value)d).'),
    'max_length': eo(u'Certigu, ke tiu cxi valoro havas maksimume %(limit_value)d signojn (gxi havas %(show_value)d).'),
    #'max_value': eo(u'Certigu, ke tiu cxi valoro estas malpli ol aux egala al %(limit_value)s.'),
    #'min_value': eo(u'Certigu, ke tiu cxi valoro estas pli ol aux egala al  %(limit_value)s.'),
}

def em(**kw):
    '''error message dict'''
    d = dict(default_error_messages, **kw)
    d['max_value'] = d['invalid']
    d['min_value'] = d['invalid']
    return d

REQUIRED_CSS_CLASS = u'required'
ERROR_CSS_CLASS = u'error'

# kampoj por interna uzo kiuj ne aperu en la publika formularo
PARTOPRENANTO_EXCLUDE = ('chambro', 'chu_invitletero_sendita',
    'deziras_loghi_kun', 'unua_konfirmilo_sendita',
    'dua_konfirmilo_sendita', 'alighdato', 'malalighdato',
    'chu_alvenis', 'chu_havasmanghkuponon', 'chu_havasnomshildon',
    'chu_surloka_membrigho', 'surlokmembrigha_kategorio',
    'surlokmembrigha_kotizo', 'chu_kontrolita',
)

# ĉiuj kampoj de Partoprenanto
#PARTOPRENANTO_CHIUJ = [f.name for f in models.Partoprenanto._meta.fields]

partoprenanto_fields_dict = dict(
    persona_nomo = forms.CharField(max_length=50,
        error_messages=em(required='Enigu vian personan nomon')),
    familia_nomo = forms.CharField(max_length=50,
        error_messages=em(required='Enigu vian familian nomon')),
    shildnomo = forms.CharField(required=False,
        label=eo('Kiel vi volas, ke via nomo aperu sur via sxildo?')),
    sekso = forms.ChoiceField(widget=forms.RadioSelect, choices=SEKSOJ,
        error_messages=em(required='Elektu vian sekson')),
    naskighdato = forms.DateField(label=eo('Naskigxdato'),
        error_messages=em(required='Elektu vian naskiĝdaton')),
    retposhtadreso = forms.EmailField(label=eo('Retposxtadreso'),
        error_messages=em(required='Enigu vian retpoŝtadreson',
                          invalid='Enigu validan retpoŝtadreson')),
    adreso = forms.CharField(required=False, widget=forms.Textarea),
    urbo = forms.CharField(max_length=50, required=False),
    poshtkodo = forms.CharField(
        max_length=15, label=eo('Posxtkodo'), required=False),
    loghlando = forms.ModelChoiceField(
        models.Lando.objects, label=eo('Logxlando'),
        error_messages=em(required='Elektu vian loĝlandon')),
    shildlando = forms.CharField(required=False,
        label=eo('Kiel vi volas, ke via lando aperu sur via sxildo?')),
    chu_bezonas_invitleteron = forms.BooleanField(initial=False, required=False,
        label=eo('Mi bezonas invitleteron')),
    telefono = forms.CharField(max_length=50, required=False),
    skype = forms.CharField(max_length=50, required=False),
    facebook = forms.CharField(max_length=50, required=False),
    mesaghiloj = forms.CharField(required=False,
        label=eo('Aliaj mesagxiloj, kiujn vi volas aperigi en la '
                 'postkongresa listo de partoprenantoj')),
    chu_retalisto = forms.BooleanField(initial=True, required=False,
        label=eo('Mi permesas publikigi mian nomon en la reta listo de '
                 'partoprenantoj')),
    chu_postkongresalisto = forms.BooleanField(initial=True, required=False,
        label=eo('Mi permesas publikigi mian nomon en '
                 'la postkongresa listo de partoprenantoj')),
    ekde = forms.DateField(
        initial=KOMENCA_DATO, label=eo('Mi partoprenos ekde'),
        error_messages=em(required='Elektu la daton, kiam vi alvenos')),
    ghis = forms.DateField(
        initial=FINIGHA_DATO, label=eo('Mi partoprenos gxis'),
        error_messages=em(required='Elektu la daton, kiam vi forlasos')),
    alveno = forms.CharField(required=False, label=eo('Mi alvenas per/je'),
        help_text=eo('Ekz. flugnumero kaj horo, se vi jam scias gxin')),
    #alvenas_je = forms.DateField(required=False, label=eo('Mi alvenas je'))
    foriro = forms.CharField(required=False, label=eo('Mi foriras per/je'),
        help_text=eo('Ekz. flugnumero kaj horo, se vi jam scias gxin')),
    #foriras_je = forms.DateField(required=False, label=eo('Mi foriras je'))
    interesighas_pri_antaukongreso = forms.IntegerField(required=False,
        max_value=5, min_value=2,
        label=eo('Mi interesigxas pri antauxkongreso'),
        error_messages=em(invalid='Enigu nombron inter 2 kaj 5')),
    interesighas_pri_postkongreso = forms.IntegerField(required=False,
        max_value=5, min_value=2,
        label=eo('Mi interesigxas pri postkongreso'),
        error_messages=em(invalid='Enigu nombron inter 2 kaj 5')),
    chu_tuttaga_ekskurso = forms.BooleanField(initial=True, required=False,
        label=eo('Mi aligxas al la tut-taga ekskurso')),
    chu_unua_dua_ijk = forms.BooleanField(initial=False, required=False,
        label=eo('Tiu cxi estas mia unua au dua IJK')),
    chu_komencanto = forms.BooleanField(initial=False, required=False,
        label=eo('Mi estas komencanto')),
    chu_interesighas_pri_kurso = forms.BooleanField(
        initial=False, required=False,
        label=eo('Mi interesigxas pri Esperanto-kurso')),
    programa_kontribuo = forms.CharField(required=False,
        widget=forms.Textarea,
        label=eo('Mi volas kontribui al la programo per:')),
    organiza_kontribuo = forms.CharField(required=False,
        widget=forms.Textarea,
        label=eo('Mi volas kontribui al organizado per:')),
    loghkategorio = forms.ModelChoiceField(models.LoghKategorio.objects,
        label=eo('Mi volas logxi en'),
        error_messages=em(required='Elektu kie vi volas loĝi')),
    deziras_loghi_kun_nomo = forms.CharField(
        required=False, label=eo('Mi deziras logxi kun')),
    chu_preferas_unuseksan_chambron = forms.BooleanField(initial=False,
        required=False, label=eo('Mi preferas unuseksan cxambron')),
    manghotipo = forms.ModelChoiceField(models.ManghoTipo.objects,
        label=eo('Mi volas mangxi'),
        error_messages=em(required='Elektu kian manĝon vi volas')),
    # XXX manghomendo
    #manghomendo = forms.ModelChoiceField(models.ManghoMendo.objects,
        #label=eo('Mi mendas mangxojn'))
    pagmaniero = forms.ModelChoiceField(
        models.Pagmaniero.objects.filter(chu_publika=True),
        label=eo('Kiamaniere vi pagos la antaupagon?'),
        error_messages=em(required=eo('Elektu kiel vi pagos la antauxpagon'))),
    pagmaniera_komento = forms.CharField(max_length=50, required=False),
    chu_ueamembro = forms.BooleanField(
        required=False, initial=False, label=eo('Mi estas membro de UEA/TEJO'),
        help_text='Membroj de UEA/TEJO ricevas rabaton ĉe IJK'),
    uea_kodo = forms.CharField(max_length=18, required=False,
        label=eo('UEA-kodo'))
)

#ManghoMendoFormset = inlineformset_factory(
    #models.Partoprenanto, models.ManghoMendo, can_delete=False)

class ManghoMendoForm(forms.Form):
    manghomendoj = forms.ModelMultipleChoiceField(label=eo('Mi volas mendi'),
        required=False, widget=forms.CheckboxSelectMultiple,
        queryset=models.ManghoMendoTipo.objects,
        initial=models.ManghoMendoTipo.objects.all())
        #choices=[(tipo.id, unicode(tipo))
                    #for tipo in models.ManghoMendoTipo.objects.all()])

class NotoForm(forms.ModelForm):
    enhavo = forms.CharField(widget=forms.Textarea,
        required=False, label=eo('Aldonaj komentoj'))
    class Meta:
        model = models.Noto
        fields = ('enhavo',)
#class PartoprenantoForm(forms.ModelForm):
    #required_css_class = u'required'
    
    #persona_nomo = forms.CharField(max_length=50,
        #error_messages=em(required='Enigu vian personan nomon'))
    #familia_nomo = forms.CharField(max_length=50,
        #error_messages=em(required='Enigu vian familian nomon'))
    #shildnomo = forms.CharField(required=False,
        #label=eo('Kiel vi volas, ke via nomo aperu sur via sxildo?'))
    #sekso = forms.ChoiceField(widget=forms.RadioSelect, choices=SEKSOJ,
        #error_messages=em(required='Elektu vian sekson'))
    #naskighdato = forms.DateField(label=eo('Naskigxdato'),
        #error_messages=em(required='Elektu vian naskiĝdaton'))
    #retposhtadreso = forms.EmailField(label=eo('Retposxtadreso'),
        #error_messages=em(required='Enigu vian retpoŝtadreson',
                          #invalid='Enigu validan retpoŝtadreson'))
    #adreso = forms.CharField(required=False, widget=forms.Textarea)
    #urbo = forms.CharField(max_length=50, required=False)
    #poshtkodo = forms.CharField(
        #max_length=15, label=eo('Posxtkodo'), required=False)
    #loghlando = forms.ModelChoiceField(
        #models.Lando.objects, label=eo('Logxlando'),
        #error_messages=em(required='Elektu vian loĝlandon'))
    #shildlando = forms.CharField(required=False,
        #label=eo('Kiel vi volas, ke via lando aperu sur via sxildo?'))
    #chu_bezonas_invitleteron = forms.BooleanField(initial=False, required=False,
        #label=eo('Mi bezonas invitleteron'))
    #telefono = forms.CharField(max_length=50, required=False)
    #skype = forms.CharField(max_length=50, required=False)
    #facebook = forms.CharField(max_length=50, required=False)
    #mesaghiloj = forms.CharField(required=False,
        #label=eo('Aliaj mesagxiloj, kiujn vi volas aperigi en la '
                 #'postkongresa listo de partoprenantoj'))
    #chu_retalisto = forms.BooleanField(initial=True, required=False,
        #label=eo('Mi permesas publikigi mian nomon en la reta listo de '
                 #'partoprenantoj'))
    #chu_postkongresalisto = forms.BooleanField(initial=True, required=False,
        #label=eo('Mi permesas publikigi mian nomon en '
                 #'la postkongresa listo de partoprenantoj'))
    #ekde = forms.DateField(
        #initial=KOMENCA_DATO, label=eo('Mi partoprenos ekde'),
        #error_messages=em(required='Elektu la daton, kiam vi alvenos'))
    #ghis = forms.DateField(
        #initial=FINIGHA_DATO, label=eo('Mi partoprenos gxis'),
        #error_messages=em(required='Elektu la daton, kiam vi forlasos'))
    #alvenas_per = forms.CharField(required=False, label=eo('Mi alvenas per'),
        #help_text=eo('Ekz. flugnumero, se vi jam scias gxin'))
    ##alvenas_je = forms.DateField(required=False, label=eo('Mi alvenas je'))
    #foriras_per = forms.CharField(required=False, label=eo('Mi foriras per'),
        #help_text=eo('Ekz. flugnumero, se vi jam scias gxin'))
    ##foriras_je = forms.DateField(required=False, label=eo('Mi foriras je'))
    #interesighas_pri_antaukongreso = forms.IntegerField(required=False,
        #max_value=5, min_value=2,
        #label=eo('Mi interesigxas pri antauxkongreso'),
        #error_messages=em(invalid='Enigu nombron inter 2 kaj 5'))
    #interesighas_pri_postkongreso = forms.IntegerField(required=False,
        #max_value=5, min_value=2,
        #label=eo('Mi interesigxas pri postkongreso'),
        #error_messages=em(invalid='Enigu nombron inter 2 kaj 5'))
    #chu_tuttaga_ekskurso = forms.BooleanField(initial=True, required=False,
        #label=eo('Mi aligxas al la tut-taga ekskurso'))
    #chu_unua_dua_ijk = forms.BooleanField(initial=False, required=False,
        #label=eo('Tiu cxi estas mia unua au dua IJK'))
    #chu_komencanto = forms.BooleanField(initial=True, required=False,
        #label=eo('Mi estas komencanto'))
    #chu_interesighas_pri_kurso = forms.BooleanField(
        #initial=True, required=False,
        #label=eo('Mi interesigxas pri Esperanto-kurso'))
    #programa_kontribuo = forms.CharField(required=False,
        #widget=forms.Textarea,
        #label=eo('Mi volas kontribui al la programo per:'))
    #organiza_kontribuo = forms.CharField(required=False,
        #widget=forms.Textarea,
        #label=eo('Mi volas kontribui al organizado per:'))
    #loghkategorio = forms.ModelChoiceField(models.LoghKategorio.objects,
        #label=eo('Mi volas logxi en'),
        #error_messages=em(required='Elektu kie vi volas loĝi'))
    #deziras_loghi_kun_nomo = forms.CharField(
        #required=False, label=eo('Mi deziras logxi kun'))
    #chu_preferas_unuseksan_chambron = forms.BooleanField(initial=False,
        #required=False, label=eo('Mi preferas unuseksan cxambron'))
    #manghotipo = forms.ModelChoiceField(models.ManghoTipo.objects,
        #label=eo('Mi volas mangxi'),
        #error_messages=em(required='Elektu kian manĝon vi volas'))
    ## XXX manghomendo
    ##manghomendo = forms.ModelChoiceField(models.ManghoMendo.objects,
        ##label=eo('Mi mendas mangxojn'))
    #pagmaniero = forms.ModelChoiceField(
        #models.Pagmaniero.objects.filter(chu_publika=True),
        #label=eo('Kiamaniere vi pagos la antaupagon?'),
        #error_messages=em(required=eo('Elektu kiel vi pagos la antauxpagon')))
    #pagmaniera_komento = forms.CharField(max_length=50, required=False)
    #chu_ueamembro = forms.BooleanField(
        #required=False, initial=False, label=eo('Mi estas membro de UEA/TEJO'),
        #help_text='Membroj de UEA/TEJO ricevas rabaton ĉe IJK')
    ##uea_kodo = 

    #class Meta:
        #model = models.Partoprenanto
        #exclude = PARTOPRENANTO_EXCLUDE

#class PartialFormType(forms.models.ModelFormMetaclass):
    #def __new__(meta, name, bases, d):
        #new = super(PartialFormType, meta).__new__(meta, name, bases, d)
        #if (hasattr(new, 'base_fields') and hasattr(new, 'Meta') and
                    #hasattr(new.Meta, 'fields')):
            #fields = new.Meta.fields
            #for key in new.base_fields.keys():
                #if key not in fields:
                    #del new.base_fields[key]
        #return new

        
#class PartoprenantoFormParto1(PartoprenantoForm):
    ##__metaclass__ = PartialFormType
    #class Meta:
        #fields = ('persona_nomo', 'familia_nomo', 'shildnomo', 'sekso',
                  #'naskighdato', 'retposhtadreso', 'adreso', 'urbo',
                  #'poshtkodo', 'loghlando', 'shildlando',)
        #model = models.Partoprenanto

def partoprenanto_form_factory(name, fieldnames):
    '''Krei formularan klason por prezenti la kampojn en fieldnames
    el la tabelo Partoprenanto'''
    meta = forms.ModelForm.__metaclass__
    bases = (forms.ModelForm,)
    d = {f: partoprenanto_fields_dict[f] for f in fieldnames}
    d['required_css_class'] = REQUIRED_CSS_CLASS
    d['error_css_class'] = ERROR_CSS_CLASS
    class Meta:
        model = models.Partoprenanto
        exclude = PARTOPRENANTO_EXCLUDE
        fields = fieldnames
    d['Meta'] = Meta
    return meta(name, bases, d)

PartoprenantoForm = partoprenanto_form_factory(
            'PartoprenantoForm', partoprenanto_fields_dict.keys())

#ftest = ('persona_nomo', 'familia_nomo', 'shildnomo', 'sekso',
         #'naskighdato', 'retposhtadreso', 'adreso', 'urbo',
         #'poshtkodo', 'loghlando', 'shildlando',)

formdivisions = [
    [['persona_nomo', 'familia_nomo', 'shildnomo', 'sekso', 'naskighdato',
        'retposhtadreso', 'adreso', 'urbo', 'poshtkodo', 'loghlando',
        'shildlando', 'chu_bezonas_invitleteron',]],
    [['telefono', 'skype', 'facebook', 'mesaghiloj', 'chu_retalisto',
        'chu_postkongresalisto',]],
    [['ekde', 'ghis', 'alveno', 'foriro', 'interesighas_pri_antaukongreso',
        'interesighas_pri_postkongreso',  'chu_tuttaga_ekskurso',
        'chu_unua_dua_ijk', 'chu_komencanto',
    'chu_interesighas_pri_kurso',]],
    [['programa_kontribuo', 'organiza_kontribuo', 'loghkategorio',
        'deziras_loghi_kun_nomo', 'chu_preferas_unuseksan_chambron',
        'manghotipo',], ManghoMendoForm,
        ['pagmaniero', 'pagmaniera_komento', 'chu_ueamembro', 'uea_kodo',],
        NotoForm]
]

form_class_list = []
for (i, division) in enumerate(formdivisions):
    cur = []
    for (j, subdiv) in enumerate(division):
        if type(subdiv) is list:
            cur.append(partoprenanto_form_factory(
                'PartoprenantoFormParto{}_{}'.format(i, j), subdiv))
        else:
            cur.append(subdiv)
    form_class_list.append(cur)
#[partoprenanto_form_factory(
    #'PartoprenantoFormParto{}'.format(i), seq)
        #for (i, seq) in enumerate(formdivisions)]

#PartoprenantoFormParto1 = partoprenanto_form_factory(
    #'myform', ftest)

def alighi(request):
    if request.method == 'POST':
        mmform = ManghoMendoForm(request.POST)
        nform = NotoForm(request.POST)
        ppform = PartoprenantoForm(request.POST)
        if (mmform.is_valid() and nform.is_valid() and ppform.is_valid()):
            partoprenanto = ppform.save()
            mm = [models.ManghoMendo(partoprenanto=partoprenanto, tipo=tipo)
                    for tipo in mmform.cleaned_data['manghomendoj']]
            for manghomendo in mm:
                manghomendo.save()
            noto = nform.save(commit=False)
            if noto.enhavo:
                noto.partoprenanto = partoprenanto
                # XXX kiu devas esti respondeca pri tiuj ĉi aferoj?
                noto.save()
            return HttpResponseRedirect('/gratulon/')
        else:
            pageforms = [[form(request.POST) for form in div]
                    for div in form_class_list]
        #if all(all(form.is_valid() for form in div) for div in pageforms):
    else:
        pageforms = [[form() for form in div] for div in form_class_list]
    context = RequestContext(request,
            {'formdivs': pageforms, 'JAVASCRIPT': DATE_JAVASCRIPT})
    return render_to_response('alighi/alighi.html', context)
