from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms import *
#from django.forms.widgets import RadioSelect

import models
from utils import eo, KOMENCA_DATO, FINIGHA_DATO, SEKSOJ

default_error_messages = {
    'required': eo(u'Cxi tiu kampo estas deviga.'),
    'invalid': eo(u'Enigu validan valoron.'),
    'min_length': eo(u'Certigu, ke tiu cxi valoro havas almenaux %(limit_value)d signojn (gxi havas %(show_value)d).'),
    'max_length': eo(u'Certigu, ke tiu cxi valoro havas maksimume %(limit_value)d signojn (gxi havas %(show_value)d).'),
    'max_value': eo(u'Certigu, ke tiu cxi valoro estas malpli ol au egala al %(limit_value)s.'),
    'min_value': eo(u'Certigu, ke tiu cxi valoro estas pli ol au egala al  %(limit_value)s.'),
}

int_error_messages = dict(
        default_error_messages, invalid=eo(u'Enigu plenan numeron.'))

def error_dict(**kw):
    '''error message dict'''
    return dict(default_error_messages, **kw)

class PartoprenantoForm(ModelForm):
    required_css_class = 'required'
    sekso = ChoiceField(widget=RadioSelect, choices=SEKSOJ)
    mesaghiloj = CharField(required=False,
        label=eo('Aliaj mesagxiloj, kiujn vi volas aperigi en la '
                 'postkongresa listo de partoprenantoj'))
    shildnomo = CharField(required=False,
        label=eo('Kiel vi volas, ke via nomo aperu sur via sxildo?'))
    shildlando = CharField(required=False,
        label=eo('Kiel vi volas, ke via lando aperu sur via sxildo?'))
    pagmaniero = ModelChoiceField(models.Pagmaniero.objects, # XXX only public 
        label=eo('Kiamaniere vi pagos la antaupagon?'),
        error_messages=error_dict(
            required=eo('Necesas marki kiel vi pagos la antauxpagon')))
    ekde = DateField(initial=KOMENCA_DATO, label=eo('Mi partoprenos ekde'))
    ghis = DateField(initial=FINIGHA_DATO, label=eo('Mi partoprenos gxis'))
    alvenas_per = CharField(required=False, label=eo('Mi alvenas per'),
        help_text=eo('Ekz. flugnumero, se vi jam scias gxin'))
    #alvenas_je = DateField(required=False, label=eo('Mi alvenas je'))
    foriras_per = CharField(required=False, label=eo('Mi foriras per'),
        help_text=eo('Ekz. flugnumero, se vi jam scias gxin'))
    #foriras_je = DateField(required=False, label=eo('Mi foriras je'))
    chu_unua_dua_ijk = BooleanField(initial=False, required=False,
        label=eo('Tiu cxi estas mia unua au dua IJK'))
    interesighas_pri_antaukongreso = IntegerField(
        label=eo('Mi interesigxas pri antauxkongreso'))
    interesighas_pri_postkongreso = IntegerField(
        label=eo('Mi interesigxas pri postkongreso'))
    chu_bezonas_invitleteron = BooleanField(initial=False, required=False,
        label=eo('Mi bezonas invitleteron'))
    chu_ueamembro = BooleanField(
        required=False, initial=False, label=eo('Mi estas membro de UEA/TEJO'))
    loghkategorio = ModelChoiceField(models.LoghKategorio.objects,
        label=eo('Mi deziras logxi en'))
    chu_preferas_unuseksan_chambron = BooleanField(initial=False,
        required=False, label=eo('Mi preferas unuseksan cxambron'))
    chu_tuttaga_ekskurso = BooleanField(initial=True, required=False,
        label=eo('Mi aligxas al la tut-taga ekskurso'))
    manghomendo = ModelChoiceField(models.ManghoMendo.objects,
        label=eo('Mi mendas mangxojn'))
    manghotipo = ModelChoiceField(models.ManghoTipo.objects,
        label=eo('Mi mangxas'))
    deziras_loghi_kun_nomo = CharField(
        required=False, label=eo('Mi deziras logxi kun'))
    chu_retalisto = BooleanField(initial=True, required=False,
        label=eo('Mi permesas publikigi mian nomon en la reta listo de '
                 'partoprenantoj'))
    chu_postkongresalisto = BooleanField(initial=True, required=False,
        label=eo('Mi permesas publikigi mian nomon en '
                 'la postkongresa listo de partoprenantoj'))
    chu_komencanto = BooleanField(initial=True, required=False,
        label=eo('Mi estas komencanto'))
    chu_interesighas_pri_kurso = BooleanField(initial=True, required=False,
        label=eo('Mi interesigxas pri Esperanto-kurso'))
    programa_kontribuo = CharField(required=False,
        widget=Textarea, label=eo('Mi sxatus kontribui al la programo per:'))
    organiza_kontribuo = CharField(required=False,
        widget=Textarea, label=eo('Mi sxatus kontribui al organizado jene:'))
    class Meta:
        model = models.Partoprenanto
        exclude = ('chambro', 'chu_invitletero_sendita',
            'deziras_loghi_kun', 'unua_konfirmilo_sendita',
            'dua_konfirmilo_sendita', 'alighdato', 'malalighdato',
            'chu_alvenis', 'chu_havasmanghkuponon', 'chu_havasnomshildon',
            'chu_surloka_membrigho', 'surlokmembrigha_kategorio',
            'surlokmembrigha_kotizo', 'chu_kontrolita',
        )
        #widgets = {
            #'sekso': RadioSelect(choices=SEKSOJ)
        #}

def alighi(request):
    if request.method == 'POST':
        form = PartoprenantoForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/grautlon/')
    else:
        form = PartoprenantoForm()
    context = RequestContext(request, {'form': form})
    return render_to_response('alighi/alighi.html', context)
