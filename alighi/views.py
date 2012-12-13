# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
#from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

import models
from utils import eo, KOMENCA_DATO, FINIGHA_DATO, SEKSOJ
from javascript import all_javascript

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

class RadioFieldSpecialClassRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        return mark_safe(u'<ul class="vertical-display">\n'
                         u'%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
                % force_unicode(w) for w in self]))

class RadioSelectSpecialClass(forms.RadioSelect):
    renderer = RadioFieldSpecialClassRenderer

paginfo = mark_safe(
    u'''<p>Via aliĝo ekvalidas post ricevo de antaŭpago je
    <strong>minimume 15 €</strong> (eblas antaŭpagi ankaŭ pli).
    La aliĝperiodo estas konsiderata laŭ la efektiva dato de alveno de la
    antaŭpago. La minimuma antaŭpago ne redoneblas, sed estas transdonebla
    al alia persono.</p>
    <p>Indiko de pagmaniero en tiu ĉi aliĝilo <strong>ne</strong> povas esti
    konsiderata pago-instrukcio. Vidu klarigojn
    <a href="http://www.uea.org/alighoj/pag_manieroj.html">kiel transpagi al
    UEA</a> (ne forgesu aldoni la <strong>administrajn kostojn</strong>
    tie menciatajn!), kaj ĉiam indiku la celon de la pago:
    "IJK2013 <em>via(j) nomo(j)</em>".
    Se vi havas problemon antaŭpagi vi devas sciigi nin pri tio:
    <a href="mailto:ijk@tejo.org">ijk@tejo.org</a>.</p>'''
)
    
class RadioFieldInfoListRenderer(forms.widgets.RadioFieldRenderer):
    infolist = models.AlighKategorio.infolist()
    def render(self):
        info = u'<ul class="infolist">{}</ul>'.format(
            '\n'.join(u'<li>{}</li>'.format(i) for i in self.infolist))
        return mark_safe(
            u'<div class="vertical-display">{}<ul>\n{}\n</ul></div>'.format(
                info, u'\n'.join(
                    [u'<li>%s</li>' % force_unicode(w) for w in self])))

class RadioSelectInfoList(forms.RadioSelect):
    renderer = RadioFieldInfoListRenderer
                    
partoprenanto_fields_dict = dict(
    persona_nomo = forms.CharField(max_length=50,
        error_messages=em(required='Enigu vian personan nomon')),
    familia_nomo = forms.CharField(max_length=50,
        error_messages=em(required='Enigu vian familian nomon')),
    shildnomo = forms.CharField(required=False,
        label=eo('Kromnomo'), help_text='Por la ŝildo'),
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
        label=eo('Mi volas, ke mia lando aperu sur mia sxildo jene:')),
    chu_bezonas_invitleteron = forms.BooleanField(initial=False, required=False,
        label=eo('Mi bezonas invitleteron')),
    telefono = forms.CharField(max_length=50, required=False,
        label='Poŝtelefon-numero', help_text='Se vi indikos ĝin, '
            'ni povos sendi al vi SMS-on okaze de lastmomentaj sciigoj.'),
    skype = forms.CharField(max_length=50, required=False),
    facebook = forms.CharField(max_length=50, required=False),
    mesaghiloj = forms.CharField(required=False,
        label=eo('Aliaj mesagxiloj, kiujn vi volas aperigi en la '
                 'postkongresa listo de partoprenantoj')),
    chu_retalisto = forms.BooleanField(initial=True, required=False,
        label=eo(u'Sur la retejo de IJK, en listo de aligxintoj')),
    chu_postkongresalisto = forms.BooleanField(initial=True, required=False,
        label=eo('Kun kontaktinformoj en la postkongresa adresaro de '              'partoprenintoj'),
        help_text=eo('Haveble nur por tiuj, kiuj efektive partoprenis')),
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
    interesighas_pri_antaukongreso = forms.IntegerField(
        required=False, widget=forms.RadioSelect(
        choices=[(None, 'ne')] +
            [(i, '{}-taga'.format(i)) for i in (2, 3, 5)]),
        max_value=5, min_value=2,
        label=eo('Mi interesigxas pri antauxkongreso'),
        error_messages=em(invalid='Enigu nombron inter 2 kaj 5')),
    interesighas_pri_postkongreso = forms.IntegerField(
        required=False, widget=forms.RadioSelect(
        choices=[(None, 'ne')] +
            [(i, '{}-taga'.format(i)) for i in (2, 3, 5)]),
        max_value=5, min_value=2,
        label=eo('Mi interesigxas pri postkongreso'),
        error_messages=em(invalid='Enigu nombron inter 2 kaj 5')),
    chu_tuttaga_ekskurso = forms.BooleanField(initial=True, required=False,
        label=eo('Mi aligxas al la tut-taga ekskurso')),
    chu_unua_dua_ijk = forms.BooleanField(initial=False, required=False,
        label=eo('Tiu cxi estas mia unua aux dua IJK')),
    chu_komencanto = forms.BooleanField(initial=False, required=False,
        label=eo('Mi estas komencanto')),
    chu_interesighas_pri_kurso = forms.BooleanField(
        initial=False, required=False,
        label=eo('Mi interesigxas pri Esperanto-kurso')),
    programa_kontribuo = forms.CharField(required=False,
        widget=forms.Textarea,
        label=eo('Mi volas kontribui al la programo per')),
    organiza_kontribuo = forms.CharField(required=False,
        widget=forms.Textarea,
        label=eo('Mi povas kontribui al organizado per')),
    loghkategorio = forms.ModelChoiceField(models.LoghKategorio.objects,
        label=eo('Mi volas logxi en'),
        widget=RadioSelectSpecialClass, empty_label=None,
        #initial=models.LoghKategorio.objects.all()[0],
        error_messages=em(required='Elektu kie vi volas loĝi')),
    deziras_loghi_kun_nomo = forms.CharField(
        required=False, label=eo('Mi deziras logxi kun')),
    chu_preferas_unuseksan_chambron = forms.BooleanField(initial=False,
        required=False, label=eo('Mi preferas unuseksan cxambron')),
    chu_malnoktemulo = forms.BooleanField(
        #help_text=u'Se vi ŝatas dormi frue, sciigu nin',
        initial=False, required=False, label=eo('Mi estas malnoktemulo')),
    manghotipo = forms.ModelChoiceField(models.ManghoTipo.objects,
        label=eo('Mangxotipo'), widget=forms.RadioSelect,
        required=True, initial=None,
        empty_label=None,
        #initial=models.ManghoTipo.objects.get(nomo='Viande'),
        error_messages=em(required='Elektu kian manĝon vi volas')),
    pagmaniero = forms.ModelChoiceField(
        models.Pagmaniero.objects.filter(chu_publika=True),
        label=eo('Mi antauxpagos per'),
        widget=RadioSelectInfoList, empty_label=None,
        help_text=paginfo, error_messages=em(
            required=eo('Elektu kiel vi pagos la antauxpagon'))),
    pagmaniera_komento = forms.CharField(max_length=50, required=False),
    chu_ueamembro = forms.BooleanField(
        required=False, initial=False,
        label=eo('Mi estas/estos membro de UEA/TEJO en 2013'),
        help_text=u'Individuaj membroj de TEJO/UEA ricevas rabaton ĉe IJK '
                  u'(kategorio MG ne validas por la rabato).'),
    uea_kodo = forms.CharField(max_length=18, required=False,
        label=eo('UEA-kodo'))
)

class ManghoMendoForm(forms.Form):
    manghomendoj = forms.ModelMultipleChoiceField(label=eo('Mi volas mendi'),
        required=False, widget=forms.CheckboxSelectMultiple,
        queryset=models.ManghoMendoTipo.objects,
        initial=models.ManghoMendoTipo.objects.all())
        #choices=[(tipo.id, unicode(tipo))
                    #for tipo in models.ManghoMendoTipo.objects.all()])

class NotoForm(forms.ModelForm):
    enhavo = forms.CharField(widget=forms.Textarea,
        required=False, label=eo('Aldonaj rimarkoj'),
        help_text='Sciigu nin pri ajna grava detalo rilate vin; '
            'ekz. specifaj bezonoj pri manĝoj aŭ ĉu vi venos kun infanoj.')
    class Meta:
        model = models.Noto
        fields = ('enhavo',)

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

def partoprenanto_fieldset_factory(label, fieldlist):
    cls = partoprenanto_form_factory(
        'PartoprenantoFieldset_{}'.format(label), fieldlist)
    class FieldSet(cls):
        fieldset_label = label
        def as_ul(self):
            return mark_safe(
                u'\n<li class="fieldset">'
                u'<div class="fieldset-label">{}</div>\n'
                u'<ul>{}</ul>\n</li>\n'.format(
                        self.fieldset_label, super(FieldSet, self).as_ul()))
    return FieldSet

class FormInfo(object):
    def __init__(self, *args, **kw):
        pass
    def as_ul(self):
        return mark_safe(u'<li><span class="info">'
                            u'{}</span></li>'.format(self.value))

class MembroKategorioFormInfo(FormInfo):
    value = models.UEARabato.infoline()


#def info_factory(val):
    #class FormInfo(object):
        #def __init__(self, *args, **kw):
            #pass
        #def as_ul(self):
            #return mark_safe(u'<li><span class="info">'
                             #u'{}</span></li>'.format(val))
    #return FormInfo
    
formdivisions = [
    [
        ['persona_nomo', 'familia_nomo', 'shildnomo', 'sekso', 'naskighdato',
        'retposhtadreso', 'adreso', 'urbo', 'poshtkodo', 'loghlando',
        'shildlando', 'chu_bezonas_invitleteron',]],
    [
        ['telefono', 'skype', 'facebook', 'mesaghiloj'],
        partoprenanto_fieldset_factory(
            'Mi permesas publikigi mian nomon, urbon kaj landon:', ['chu_retalisto', 'chu_postkongresalisto',])],
    [
        ['ekde', 'ghis', 'alveno', 'foriro', 'interesighas_pri_antaukongreso',
        'interesighas_pri_postkongreso', 'chu_tuttaga_ekskurso',
        'chu_unua_dua_ijk', 'chu_komencanto', 'chu_interesighas_pri_kurso',
        'programa_kontribuo', 'organiza_kontribuo']],
    [
        ['loghkategorio', 'deziras_loghi_kun_nomo',
        'chu_preferas_unuseksan_chambron', 'chu_malnoktemulo', 'manghotipo',], ManghoMendoForm,
        ['pagmaniero', 'pagmaniera_komento', 'chu_ueamembro'],
        MembroKategorioFormInfo, ['uea_kodo'], NotoForm]
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
            return HttpResponseRedirect(reverse('gratulon'))
        else:
            pageforms = [[form(request.POST) for form in div]
                    for div in form_class_list]
    else:
        pageforms = [[form() for form in div] for div in form_class_list]
    context = RequestContext(request,
            {'formdivs': pageforms, 'JAVASCRIPT': all_javascript()})
    return render_to_response('alighi/alighi.html', context)

def gratulon(request):
    return render_to_response('alighi/gratulon.html', {})