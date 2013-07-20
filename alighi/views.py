# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.conf import settings
from django.http import Http404

import models
from utils import eo, KOMENCA_DATO, FINIGHA_DATO, SEKSOJ, esperanteca_dato
from javascript import all_javascript
from validators import *

import datetime

VERTICAL_CLASS = 'vertical-display'

NEVALIDA_DATO = u'Enigu validan valoron (en formato jjjj-mm-tt).'
INVALID_MODEL_CHOICE = eo(u'Faru elekton el la listo de haveblaj opcioj. '
        u'La valoro de vi provizita (%(value)s) ne validas.')
INVALID_CHOICE = eo(u'Faru elekton el la listo de haveblaj opcioj. '
        u'La valoro de vi provizita ne validas.')
INVALID_PK_CHOICE = eo(u'Faru elekton el la listo de haveblaj opcioj. '
        u'La valoro de vi provizita (%s) ne validas.')

default_error_messages = {
    'required': eo(u'Cxi tiu kampo estas deviga.'),
    'invalid': eo(u'Faru elekton el la listo de haveblaj opcioj. '
                  u'La valoro de vi provizita ne validas.'),
    'min_length': eo(u'Certigu, ke tiu cxi valoro havas almenaux %(limit_value)d signojn (gxi havas %(show_value)d).'),
    'max_length': eo(u'Certigu, ke tiu cxi valoro havas maksimume %(limit_value)d signojn (gxi havas %(show_value)d).'),
    'invalid_choice': INVALID_CHOICE,
}

default_error_messages['invalid_pk_value'] = INVALID_PK_CHOICE

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
#    def render(self):
#        return mark_safe(u'<ul class="%s">\n%s\n</ul>' %
#                         (VERTICAL_CLASS, u'\n'.join(
#            [u'<li>%s</li>' % force_unicode(w) for w in self])))

    def render(self):
        def procw(w):
            if int(w.choice_value) in self.disabled:
                w.attrs['disabled'] = True
            return w
        widgets = (procw(widget) for widget in self)
        return mark_safe(u'<ul class="%s">\n%s\n</ul>' %
                         (VERTICAL_CLASS, u'\n'.join(
            (u'<li>%s</li>' % force_unicode(w) for w in widgets))))


class RadioSelectSpecialClass(forms.RadioSelect):
    renderer = RadioFieldSpecialClassRenderer
    def __init__(self, *args, **kw):
        if 'disabled' in kw:
            self.disabled = kw['disabled']
            del kw['disabled']
        super(RadioSelectSpecialClass, self).__init__(*args, **kw)
    def get_renderer(self, *args, **kw):
        renderer = super(RadioSelectSpecialClass,
                         self).get_renderer(*args, **kw)
        renderer.disabled = self.disabled if hasattr(self, 'disabled') else {}
        return renderer

class CheckboxSpecialClass(forms.CheckboxSelectMultiple):
    def render(self, *args, **kw):
        orig = super(CheckboxSpecialClass, self).render(
            *args, **kw)
        if not orig.startswith(u'<ul>'):
            return orig
        return u'<ul class="{}">{}'.format(VERTICAL_CLASS,
                                           orig[4:])

paginfo = mark_safe(
    u'''<p>Via aliĝo ekvalidas post ricevo de antaŭpago je
    <strong>minimume 15 €</strong> (eblas antaŭpagi ankaŭ pli).
    La aliĝperiodo estas konsiderata laŭ la efektiva dato de alveno de la
    antaŭpago. La minimuma antaŭpago ne redoneblas, sed estas transdonebla
    al alia persono.</p>
    <p>Indiko de pagmaniero en tiu ĉi aliĝilo <strong>ne</strong> povas esti
    konsiderata pago-instrukcio. Vidu klarigojn
    <a href="http://www.uea.org/alighoj/pag_manieroj.html" target="_blank">
    kiel transpagi al UEA</a> (ne forgesu aldoni la
    <strong>administrajn kostojn</strong>
    tie menciatajn!), kaj ĉiam indiku la celon de la pago:
    "IJK2013 <em>via(j) nomo(j)</em>".
    Se vi havas problemon antaŭpagi vi devas sciigi nin pri tio:
    <a href="mailto:ijk@tejo.org">ijk@tejo.org</a>.</p>'''
)

class RadioAndTextInput(forms.widgets.RadioInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.extra_label:
            textval = self.comment_value if self.is_checked() else u''
            textid = '{}_comment_{}'.format(
                self.attrs['id'], self.choice_value)
            textname = '{}_comment_{}'.format(self.name, self.choice_value)
            text = forms.TextInput().render(textname, textval, {'id': textid})
        else:
            text = u''
        return mark_safe(
            super(RadioAndTextInput, self).render(
                name, value[0], attrs, choices) + text)
    def __init__(self, name, value, attrs, choice, index, *args, **kw):
        if 'extra_label' in kw:
            self.extra_label = kw['extra_label']
            del kw['extra_label']
        else:
            self.extra_label = None
        super(RadioAndTextInput, self).__init__(
            name, value, attrs, choice, index, *args, **kw)
        self.choice_value = force_unicode(choice[0][0])
        self.value = force_unicode(value[0])
        self.comment_choice_value = force_unicode(choice[0][1])
        self.comment_value = force_unicode(value[1])
        if self.extra_label:
            self.choice_label += ', {}:'.format(self.extra_label)

class RadioFieldWithCommentRenderer(forms.widgets.RadioFieldRenderer):
    def __init__(self, name, value, attrs, choices, *args, **kw):
        if 'extra_labels' in kw:
            self.extra_labels = kw['extra_labels']
            del kw['extra_labels']
        else:
            self.extra_labels = [None] * len(choices)
        super(RadioFieldWithCommentRenderer, self).__init__(
            name, value, attrs, choices, *args, **kw)
        if not self.value:
            self.value = [None, u'']
    def render(self):
        lis = [force_unicode(w.render(self.name, self.value, self.attrs))
                        for w in self]
        lis = u'\n'.join(u'<li>{}</li>'.format(li) for li in lis)
        ul = u'<ul class="vertical-display infolist">\n{}\n</ul>'.format(lis)
        return mark_safe(ul)
    def _get_widget(self, choice, idx):
        return RadioAndTextInput(
            self.name, self.value, self.attrs.copy(), choice, idx,
            extra_label=self.extra_labels[idx])
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield self._get_widget(choice, i)
    def __getitem__(self, idx):
        choice = self.choices[idx]
        return self._get_widget(choice, idx)

class RadioSelectPagmanieroj(forms.RadioSelect):
    renderer = RadioFieldWithCommentRenderer
    def value_from_datadict(self, data, files, name):
        radioval = super(RadioSelectPagmanieroj, self).value_from_datadict(
            data, files, name)
        if radioval is None:
            textval = u''
        else:
            textval = data.get('{}_comment_{}'.format(name, radioval), u'')
        return [radioval, textval]
    def get_renderer(self, name, value, attrs=None, choices=()):
        if value is None: value = u''
        final_attrs = self.build_attrs(attrs)
        choices = list(self.choices)
        return self.renderer(name, value, final_attrs, choices,
            extra_labels=self.extra_labels)
    def get_selected_extra_label(self, pk):
        '''Given the primary key of the value
        that this widget returns from the form,
        return the value that the extra_label had for the selected item'''
        for (extra_label, choice) in zip(self.extra_labels, self.choices):
            if choice[0][0] == pk:
                return extra_label

class PagmanieroChoiceField(forms.ModelChoiceField):
    widget = RadioSelectPagmanieroj
    def __init__(self, queryset, **kw):
        super(PagmanieroChoiceField, self).__init__(queryset, **kw)
        if not hasattr(self.widget, 'extra_labels'):
            self.widget.extra_labels = [None] * len(self.choices)
    def prepare_value(self, value):
        if not value:
            value = [None, u'']
        if not isinstance(value, list):
            value = [value, u'']
        r = [super(PagmanieroChoiceField, self).prepare_value(value[0]),
                value[1]]
        return r
    def to_python(self, value):
        self.comment = value[1]
        return super(PagmanieroChoiceField, self).to_python(value[0])

    def _get_queryset(self):
        return self._queryset
    def _set_queryset(self, queryset):
        self._queryset = queryset
        self.widget.choices = self.choices
        self.widget.extra_labels = [o.komenta_etikedo for o in queryset]
    queryset = property(_get_queryset, _set_queryset)

class CustomLabelModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kw):
        if 'labelfunc' in kw:
            self._labelfunc = kw['labelfunc']
            del kw['labelfunc']
        super(CustomLabelModelChoiceField, self).__init__(*args, **kw)
    def label_from_instance(self, obj):
        if hasattr(self, '_labelfunc'):
            return self._labelfunc(obj)
        return super(CustomLabelModelChoiceField,
                     self).label_from_instance(obj)

partoprenanto_fields_dict = dict(
    persona_nomo=forms.CharField(max_length=50,
        error_messages=em(required='Enigu vian personan nomon'),
        validators=[nomo_validator]),
    familia_nomo=forms.CharField(max_length=50,
        error_messages=em(required='Enigu vian familian nomon'),
        validators=[nomo_validator]),
    shildnomo=forms.CharField(required=False,
        label=eo('Kromnomo'), validators=[kromnomo_validator]),
    sekso=forms.ChoiceField(widget=forms.RadioSelect, choices=SEKSOJ,
        error_messages=em(required='Elektu vian sekson')),
    naskighdato=forms.DateField(label=eo('Naskigxdato'),
        validators=[naskighdato],
        error_messages=em(
            required='Elektu vian naskiĝdaton', invalid=NEVALIDA_DATO,
            estonteco=u'Aliĝanto ne povas naskiĝi en la estonteco.')),
    retposhtadreso=forms.EmailField(label=eo('Retposxtadreso'),
        error_messages=em(required='Enigu vian retpoŝtadreson',
                          invalid='Enigu validan retpoŝtadreson')),
    adreso=forms.CharField(required=False, widget=forms.Textarea),
    urbo=forms.CharField(max_length=50, required=False),
    poshtkodo=forms.CharField(
        max_length=15, label=eo('Posxtkodo'), required=False,
        validators=[poshtkodo_validator]),
    loghlando=forms.ModelChoiceField(
        models.Lando.objects, label=eo('Logxlando'),
        error_messages=em(required='Elektu vian loĝlandon')),
    shildlando=forms.CharField(required=False,
        label=eo('Mi volas, ke mia lando aperu sur mia sxildo jene:'),
        validators=[shildlando_validator]),
    chu_bezonas_invitleteron=forms.BooleanField(
        initial=False, required=False,
        label=eo('Mi bezonas invitleteron'),
        help_text=eo(u'Kromkosto: {} €'.format(models.KrompagTipo.liveri_koston('invitletero')))),
    telefono=forms.CharField(max_length=50, required=False,
        label='Poŝtelefon-numero', validators=[telefono_validator]),
    skype=forms.CharField(max_length=50, required=False,
        validators=[skype_validator]),
    facebook=forms.CharField(max_length=50, required=False),
    mesaghiloj=forms.CharField(required=False,
        label=eo('Aliaj mesagxiloj'),
        help_text=eo(u'Kiujn vi volas aperigi '
                     u'en la postkongresa listo de  partoprenantoj')),
    chu_retalisto=forms.BooleanField(initial=True, required=False,
        label=eo(u'Sur la retejo de IJK, en listo de aligxintoj')),
    chu_postkongresalisto=forms.BooleanField(initial=True, required=False,
        label=eo(u'Kun kontaktinformoj en la postkongresa adresaro de '              'partoprenintoj'),
        help_text=eo('Haveble nur por tiuj, kiuj efektive partoprenis')),
    ekde=forms.DateField(
        initial=KOMENCA_DATO, label=eo('Mi partoprenos ekde'),
        error_messages=em(required='Elektu la daton, kiam vi alvenos',
                          invalid=NEVALIDA_DATO)),
    ghis=forms.DateField(
        initial=FINIGHA_DATO, label=eo('Mi partoprenos gxis'),
        error_messages=em(required='Elektu la daton, kiam vi forlasos',
                          invalid=NEVALIDA_DATO)),
    alveno=forms.CharField(required=False, label=eo('Mi alvenas per/je')),
    foriro=forms.CharField(required=False, label=eo('Mi foriras per/je')),
    interesighas_pri_antaukongreso=forms.IntegerField(
        required=True, widget=forms.RadioSelect(
        choices=[(0, 'ne')] +
            [(i, '{}-taga'.format(i)) for i in (2, 3, 5)]),
        label=eo('Mi interesigxas pri antauxkongreso'),
        error_messages=em(
            invalid=u'Elektu inter "ne" kaj nombro de tagoj (2 ĝis 5)')),
    interesighas_pri_postkongreso=forms.IntegerField(
        required=True, widget=forms.RadioSelect(
        choices=[(0, 'ne')] +
            [(i, '{}-taga'.format(i)) for i in (2, 3, 5)]),
        # max_value=5, min_value=2,
        label=eo('Mi interesigxas pri postkongreso'),
        error_messages=em(
            invalid=u'Elektu inter "ne" kaj nombro de tagoj (2 ĝis 5)')),
    chu_tuttaga_ekskurso=forms.BooleanField(initial=True, required=False,
        label=eo('Mi aligxas al la tut-taga ekskurso')),
    chu_unua_dua_ijk=forms.BooleanField(initial=False, required=False,
        label=eo('Tiu cxi estas mia unua aux dua IJK')),
    chu_komencanto=forms.BooleanField(initial=False, required=False,
        label=eo('Mi estas komencanto')),
    chu_interesighas_pri_kurso=forms.BooleanField(
        initial=False, required=False,
        label=eo('Mi interesigxas pri Esperanto-kurso')),
    programa_kontribuo=forms.CharField(required=False,
        widget=forms.Textarea,
        label=eo('Mi volas kontribui al la programo per')),
    organiza_kontribuo=forms.CharField(required=False,
        widget=forms.Textarea,
        label=eo('Mi povas kontribui al organizado per')),
    loghkategorio=forms.ModelChoiceField(models.LoghKategorio.objects,
        label=eo('Mi volas logxi en'),
        widget=RadioSelectSpecialClass(
            disabled=set(lk.id for lk in
                     models.LoghKategorio.objects.filter(chu_havebla=False))),
        empty_label=None,
        help_text=models.LoghKategorio.helptext(),
        error_messages=em(required='Elektu kie vi volas loĝi')),
    deziras_loghi_kun_nomo=forms.CharField(
        required=False, label=eo('Mi deziras logxi kun')),
    chu_preferas_unuseksan_chambron=forms.BooleanField(initial=False,
        required=False, label=eo('Mi preferas unuseksan cxambron')),
    chu_malnoktemulo=forms.BooleanField(
        initial=False, required=False, label=eo('Mi estas malnoktemulo')),
    manghotipo=forms.ModelChoiceField(models.ManghoTipo.objects,
        label=eo('Mangxotipo'), widget=forms.RadioSelect,
        required=True, initial=None,
        empty_label=None,
        error_messages=em(required='Elektu kian manĝon vi volas')),
    manghomendoj=forms.ModelMultipleChoiceField(label=eo('Mi volas mendi'),
        required=False, widget=CheckboxSpecialClass,
        queryset=models.ManghoMendoTipo.objects,
        initial=models.ManghoMendoTipo.objects.all(),
        error_messages=em(invalid_choice='Ne, ne, ne: %r')),
    antaupagos_ghis=CustomLabelModelChoiceField(models.AlighKategorio.objects,
        label=eo('Mi antauxpagos gxis'), required=True, initial=None,
        labelfunc=lambda o: esperanteca_dato(o.limdato),
        widget=RadioSelectSpecialClass, empty_label=None,
        error_messages=em(
            required=eo('Elektu gxis kiam vi faros la antauxpagon'))),
    pagmaniero=PagmanieroChoiceField(
        models.Pagmaniero.objects.filter(chu_publika=True),
        label=eo('Mi antauxpagos per'),
        widget=RadioSelectPagmanieroj, empty_label=None,
        help_text=paginfo,
        error_messages=em(
            required=eo('Elektu kiel vi pagos la antauxpagon'))),
    chu_ueamembro=forms.BooleanField(
        required=False, initial=False,
        label=eo('Mi estas/estos membro de TEJO/UEA en 2013')),
    uea_kodo=forms.CharField(max_length=6, min_length=6, required=False,
        label=eo('UEA-kodo'), validators=[ueakodo_validator],
        error_messages=em(
            min_length=u'Certigu ke ĉi-tiu valoro havas ekzakte 6 signojn',
            max_length=u'Certigu ke ĉi-tiu valoro havas ekzakte 6 signojn')),
    alighila_kotizo=forms.CharField(widget=forms.HiddenInput, required=False)
)

class ManghoMendoForm(forms.Form):
    manghomendoj = forms.ModelMultipleChoiceField(label=eo('Mi volas mendi'),
        required=False, widget=CheckboxSpecialClass,
        queryset=models.ManghoMendoTipo.objects,
        initial=models.ManghoMendoTipo.objects.all(),
        error_messages=em(invalid_choice='Ne, ne, ne: %r'))

class NotoForm(forms.ModelForm):
    enhavo = forms.CharField(widget=forms.Textarea,
        required=False, label=eo('Aldonaj rimarkoj'))
    class Meta:
        model = models.Noto
        fields = ('enhavo',)

class PartoprenantoBaseForm(forms.ModelForm):
    def as_ul(self):
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            normal_row=u'<li%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</li>',
            error_row=u'<li>%s</li>',
            row_ender='</li>',
            help_text_html=u' <div class="helptext">%s</div>',
            errors_on_separate_row=False)

def partoprenanto_form_factory(name, fieldnames):
    '''Krei formularan klason por prezenti la kampojn en fieldnames
    el la tabelo Partoprenanto'''
    meta = forms.ModelForm.__metaclass__
    bases = (PartoprenantoBaseForm,)
    d = {f: partoprenanto_fields_dict[f] for f in fieldnames}
    d['required_css_class'] = REQUIRED_CSS_CLASS
    d['error_css_class'] = ERROR_CSS_CLASS
    class Meta:
        model = models.Partoprenanto
        exclude = PARTOPRENANTO_EXCLUDE
        fields = fieldnames
    d['Meta'] = Meta
    return meta(name, bases, d)

PartoprenantoFormBase = partoprenanto_form_factory(
            'PartoprenantoForm', partoprenanto_fields_dict.keys())
class PartoprenantoForm(PartoprenantoFormBase):
    def clean_ekde(self):
        if 'ekde' not in self.cleaned_data:
            return
        ekde = self.cleaned_data['ekde']
        if ekde > FINIGHA_DATO:
            raise ValidationError(u'Vi ne povas partopreni ekde dato post '
                                  u'la fino de la kongreso')
        return ekde
    def clean_ghis(self):
        if 'ghis' not in self.cleaned_data:
            return
        ghis = self.cleaned_data['ghis']
        if ghis < KOMENCA_DATO:
            raise ValidationError(u'Vi ne povas partopreni ĝis dato antaŭ '
                                  u'la komenco de la kongreso')
        return ghis
    def clean(self):
        cleaned_data = super(PartoprenantoForm, self).clean()
        if ('uea_kodo' in cleaned_data and cleaned_data['uea_kodo'] and
                'loghlando'  in cleaned_data):
            uea_kodo = cleaned_data['uea_kodo']
            loghlando = cleaned_data['loghlando'].kodo
            result, msg = models.UEAValideco.chu_valida(uea_kodo, loghlando)
            if not result:
                self._errors['uea_kodo'] = self.error_class([msg])
                del cleaned_data['uea_kodo']
        if 'pagmaniero' in cleaned_data:
            pw = self.fields['pagmaniero'].widget
            extra_label = pw.get_selected_extra_label(
                          cleaned_data['pagmaniero'].pk)
            # if an extra_label is defined in the db,
            # then the comment is required
            if extra_label and not self.fields['pagmaniero'].comment:
                self._errors['pagmaniero'] = self.error_class(
                    [u'Necesas enigi kroman informon'])
                del cleaned_data['pagmaniero']
        if cleaned_data.get('chu_bezonas_invitleteron', False):
            # se la partoprenanto bezonas invitleteron, la adresaj kampoj estas
            # plenigendaj
            msg = u'Se vi bezonas invitleteron, necesas provizi {}'
            if not cleaned_data.get('adreso', u'').strip():
                self._errors['adreso'] = self.error_class(
                    [msg.format('adreson')])
                del cleaned_data['adreso']
            if not cleaned_data.get('poshtkodo', u'').strip():
                self._errors['poshtkodo'] = self.error_class(
                    [msg.format(u'poŝtkodon')])
                del cleaned_data['poshtkodo']
            if not cleaned_data.get('urbo', u'').strip():
                self._errors['urbo'] = self.error_class(
                    [msg.format(u'urbon')])
                del cleaned_data['urbo']
        return cleaned_data

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
        return mark_safe(
            u'<li class="helptext-below">{}</li>'.format(
                self.value))
    @classmethod
    def make_form(cls, val):
        class FormInfoClass(cls):
            value = val
        return FormInfoClass

class MembroKategorioFormInfo(FormInfo):
    value = models.UEARabato.infoline()

class MultiField(forms.Field):
    widget = forms.MultiWidget
    def __init__(self, fields, **kw):  # required, label, initial, widget, help_text):
        self.fields = fields
        if 'widget' not in kw:
            kw['widget'] = self.widget(
                widgets=[field.widget for field in fields])
        super(MultiField, self).__init__(**kw)

vianda_kosto = models.KrompagTipo.liveri_koston('viando')
formdivisions = [
    ('Personaj informoj', [
        ['persona_nomo', 'familia_nomo', 'shildnomo', ],
        FormInfo.make_form(u'Por la nomŝildo'),
        ['sekso', 'naskighdato',
        'adreso', 'urbo', 'poshtkodo', 'loghlando', 'shildlando',
        'chu_bezonas_invitleteron'],
        FormInfo.make_form(u'Se vi bezonas invitleteron, nepre indiku '
        u'plenan adreson, poŝtkodon, kaj urbon.'), ['retposhtadreso',
        'chu_komencanto', 'chu_interesighas_pri_kurso']
    ]),
    ('Komunikiloj', [
        ['telefono'], FormInfo.make_form(u'Enigu numeron en formato '
            u'+[lando-kodo]-[prefikso]-[numero]. Se vi indikos ĝin, '
            u'ni povos sendi al vi SMS-on okaze de lastmomentaj sciigoj.'),
        ['skype', 'facebook', 'mesaghiloj'],
        partoprenanto_fieldset_factory(
            'Mi permesas publikigi mian nomon, urbon kaj landon:',
            ['chu_retalisto', 'chu_postkongresalisto', ])
    ]),
    ('Partopreno', [
        ['ekde', 'ghis', 'chu_unua_dua_ijk'],
        ['alveno'], FormInfo.make_form(
            eo('Ekz. flugnumero kaj horo, se vi jam scias gxin')),
        ['foriro'], FormInfo.make_form(
            eo('Ekz. flugnumero kaj horo, se vi jam scias gxin')),
        ['chu_tuttaga_ekskurso',
        'interesighas_pri_antaukongreso',
        'interesighas_pri_postkongreso',
        'programa_kontribuo', 'organiza_kontribuo']
    ]),
    (eo('Logxado'), [
        ['loghkategorio', 'chu_preferas_unuseksan_chambron',
        'chu_malnoktemulo', 'deziras_loghi_kun_nomo', ]
    ]),
    (eo('Mangxado'), [ManghoMendoForm, ['manghotipo', ],
        FormInfo.make_form(
            u'Kromkosto de vianda manĝo: {} €'.format(vianda_kosto))
        ]),
    (eo('Pago'), [
        ['chu_ueamembro'], FormInfo.make_form(u'<p>{}</p><p>{}</p>'.format(
            u'Individuaj membroj de TEJO/UEA ricevas rabaton ĉe IJK '
                  u'(kategorio MG ne validas por la rabato).',
            models.UEARabato.infoline()
        )),
        ['uea_kodo', 'antaupagos_ghis', 'pagmaniero'], NotoForm,
        FormInfo.make_form(u'Sciigu nin pri ajna grava detalo rilate vin; '
            u'ekz. specifaj bezonoj pri manĝoj aŭ ĉu vi venos kun infanoj.'),
        ['alighila_kotizo']
    ])
]

form_class_list = []
tablist = []
for (i, (tag, division)) in enumerate(formdivisions):
    tablist.append(tag)
    cur = []
    for (j, subdiv) in enumerate(division):
        if type(subdiv) is list:
            cur.append(partoprenanto_form_factory(
                'PartoprenantoFormParto{}_{}'.format(i, j), subdiv))
        else:
            cur.append(subdiv)
    form_class_list.append(cur)

tabs = mark_safe(
    u'<ul>{}</ul>'.format(
        u''.join(
            u'<li class="tab"><a href="#tab-{}">{}</a></li>'.format(i, tab)
                for (i, tab) in enumerate(tablist))))

def alighi(request):
    if settings.HIDE_ALIGHILO:
        raise Http404
    has_errors = False
    if request.method == 'POST':
        nform = NotoForm(request.POST)
        ppform = PartoprenantoForm(request.POST)
        if (nform.is_valid() and ppform.is_valid()):
            partoprenanto = ppform.save(commit=False)
            partoprenanto.pagmaniera_komento = \
                ppform.fields['pagmaniero'].comment
            partoprenanto.save()
            ppform.save_m2m()
            noto = nform.save(commit=False)
            if noto.enhavo:
                noto.partoprenanto = partoprenanto
                # TODO kiu devas esti respondeca pri tiuj ĉi aferoj?
                noto.save()
            retposhtajho = models.Retposhtajho.get_by_nomo(
                settings.ALIGHILO_RICEVITA)
            if retposhtajho is not None:
                retposhtajho.sendi(partoprenanto)
            return HttpResponseRedirect(reverse('gratulon'))
        else:
            has_errors = True
            errors = nform.errors.copy()
            errors.update(ppform.errors)
            def adderrors(form):
                form._errors = errors.copy()
                return form
            pageforms = [[adderrors(form(request.POST)) for form in div]
                    for div in form_class_list]
    else:
        pageforms = [[form() for form in div] for div in form_class_list]
    context = RequestContext(request,
            {'formdivs': pageforms,
             'JAVASCRIPT': all_javascript(),
             'tabs': tabs,
             'has_errors': has_errors,
             'scripts': ['js/alighi.min.js']})
    return render_to_response('alighi/alighi.html', context)

def gratulon(request):
    context = RequestContext(request)
    return render_to_response('alighi/gratulon.html', context)

def bazo(request):
    context = RequestContext(request)
    return render_to_response('base.html', context)

def alighintoj(request):
    context = RequestContext(request, {'alighintoj':
                                       models.Partoprenanto.alighintoj()})
    return render_to_response('alighi/alighintoj.html', context)
