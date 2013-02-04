# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Respondeco'
        db.create_table('alighi_respondeco', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rolo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('uzanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('alighi', ['Respondeco'])

        # Adding model 'Valuto'
        db.create_table('alighi_valuto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kodo', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('nomo', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('alighi', ['Valuto'])

        # Adding model 'Kurzo'
        db.create_table('alighi_kurzo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valuto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Valuto'])),
            ('dato', self.gf('django.db.models.fields.DateField')()),
            ('kurzo', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=5)),
        ))
        db.send_create_signal('alighi', ['Kurzo'])

        # Adding unique constraint on 'Kurzo', fields ['valuto', 'dato']
        db.create_unique('alighi_kurzo', ['valuto_id', 'dato'])

        # Adding model 'AghKategorio'
        db.create_table('alighi_aghkategorio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('priskribo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('limagho', self.gf('django.db.models.fields.IntegerField')()),
            ('aldona_kotizo', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('alighi', ['AghKategorio'])

        # Adding model 'AlighKategorio'
        db.create_table('alighi_alighkategorio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('priskribo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('limdato', self.gf('django.db.models.fields.DateField')(unique=True)),
        ))
        db.send_create_signal('alighi', ['AlighKategorio'])

        # Adding model 'LandoKategorio'
        db.create_table('alighi_landokategorio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('priskribo', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('alighi', ['LandoKategorio'])

        # Adding model 'Lando'
        db.create_table('alighi_lando', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('kodo', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('kategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.LandoKategorio'])),
        ))
        db.send_create_signal('alighi', ['Lando'])

        # Adding model 'LoghKategorio'
        db.create_table('alighi_loghkategorio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('priskribo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('plena_kosto', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('unutaga_kosto', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('alighi', ['LoghKategorio'])

        # Adding model 'ManghoTipo'
        db.create_table('alighi_manghotipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('alighi', ['ManghoTipo'])

        # Adding model 'ProgramKotizo'
        db.create_table('alighi_programkotizo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aghkategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.AghKategorio'])),
            ('landokategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.LandoKategorio'])),
            ('alighkategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.AlighKategorio'])),
            ('kotizo', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('alighi', ['ProgramKotizo'])

        # Adding unique constraint on 'ProgramKotizo', fields ['aghkategorio', 'landokategorio', 'alighkategorio']
        db.create_unique('alighi_programkotizo', ['aghkategorio_id', 'landokategorio_id', 'alighkategorio_id'])

        # Adding model 'Pagmaniero'
        db.create_table('alighi_pagmaniero', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('priskribo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('komenta_etikedo', self.gf('django.db.models.fields.CharField')(default=u'', max_length=250, blank=True)),
            ('chu_publika', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('chu_nurisraela', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('alighi', ['Pagmaniero'])

        # Adding model 'KrompagTipo'
        db.create_table('alighi_krompagtipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('sumo', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('alighi', ['KrompagTipo'])

        # Adding model 'Retposhtajho'
        db.create_table('alighi_retposhtajho', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('sendadreso', self.gf('django.db.models.fields.EmailField')(default=u'ijk@tejo.org', max_length=75)),
            ('temo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('teksto', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('alighi', ['Retposhtajho'])

        # Adding model 'MembrighaKategorio'
        db.create_table('alighi_membrighakategorio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('alighi', ['MembrighaKategorio'])

        # Adding model 'Chambro'
        db.create_table('alighi_chambro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('litonombro', self.gf('django.db.models.fields.IntegerField')()),
            ('loghkategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.LoghKategorio'])),
            ('rimarko', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('alighi', ['Chambro'])

        # Adding model 'UEARabato'
        db.create_table('alighi_uearabato', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('landokategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.LandoKategorio'], unique=True)),
            ('sumo', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('alighi', ['UEARabato'])

        # Adding model 'Partoprenanto'
        db.create_table('alighi_partoprenanto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona_nomo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('familia_nomo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('shildnomo', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('sekso', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('naskighdato', self.gf('django.db.models.fields.DateField')()),
            ('retposhtadreso', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('adreso', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('urbo', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('poshtkodo', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('loghlando', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Lando'])),
            ('shildlando', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('chu_bezonas_invitleteron', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chu_invitletero_sendita', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('mesaghiloj', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('chu_retalisto', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('chu_postkongresalisto', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ekde', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 8, 19, 0, 0))),
            ('ghis', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 8, 26, 0, 0))),
            ('alveno', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('foriro', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('interesighas_pri_antaukongreso', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('interesighas_pri_postkongreso', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('chu_tuttaga_ekskurso', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('chu_unua_dua_ijk', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chu_komencanto', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('chu_interesighas_pri_kurso', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('programa_kontribuo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('organiza_kontribuo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('loghkategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.LoghKategorio'])),
            ('deziras_loghi_kun_nomo', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('deziras_loghi_kun', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Partoprenanto'], null=True, blank=True)),
            ('chu_preferas_unuseksan_chambron', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chu_malnoktemulo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chambro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Chambro'], null=True, blank=True)),
            ('manghotipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.ManghoTipo'])),
            ('antaupagos_ghis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.AlighKategorio'], null=True)),
            ('pagmaniero', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Pagmaniero'])),
            ('pagmaniera_komento', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('chu_ueamembro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uea_kodo', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('chu_kontrolita', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unua_konfirmilo_sendita', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dua_konfirmilo_sendita', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('alighdato', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('malalighdato', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('chu_alvenis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chu_havasmanghkuponon', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chu_havasnomshildon', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('alighi', ['Partoprenanto'])

        # Adding model 'ManghoMendoTipo'
        db.create_table('alighi_manghomendotipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('priskribo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('kosto', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('alighi', ['ManghoMendoTipo'])

        # Adding model 'ManghoMendo'
        db.create_table('alighi_manghomendo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partoprenanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Partoprenanto'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.ManghoMendoTipo'])),
        ))
        db.send_create_signal('alighi', ['ManghoMendo'])

        # Adding unique constraint on 'ManghoMendo', fields ['partoprenanto', 'tipo']
        db.create_unique('alighi_manghomendo', ['partoprenanto_id', 'tipo_id'])

        # Adding model 'SurlokaMembrigho'
        db.create_table('alighi_surlokamembrigho', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partoprenanto', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alighi.Partoprenanto'], unique=True)),
            ('kategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.MembrighaKategorio'])),
            ('kotizo', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('valuto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Valuto'])),
        ))
        db.send_create_signal('alighi', ['SurlokaMembrigho'])

        # Adding model 'Pagtipo'
        db.create_table('alighi_pagtipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('alighi', ['Pagtipo'])

        # Adding model 'Pago'
        db.create_table('alighi_pago', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partoprenanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Partoprenanto'])),
            ('uzanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pagmaniero', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Pagmaniero'])),
            ('pagtipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Pagtipo'])),
            ('valuto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Valuto'])),
            ('sumo', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('dato', self.gf('alighi.models.NeEstontecaDato')()),
            ('rimarko', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('alighi', ['Pago'])

        # Adding model 'MinimumaAntaupago'
        db.create_table('alighi_minimumaantaupago', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('landokategorio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.LandoKategorio'])),
            ('oficiala_antaupago', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('interna_antaupago', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('alighi', ['MinimumaAntaupago'])

        # Adding model 'Nomshildo'
        db.create_table('alighi_nomshildo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nomo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('titolo_lokalingve', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('titolo_esperante', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('chu_havasnomshildon', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('alighi', ['Nomshildo'])

        # Adding model 'Noto'
        db.create_table('alighi_noto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partoprenanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Partoprenanto'], null=True, blank=True)),
            ('uzanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('dato', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('enhavo', self.gf('django.db.models.fields.TextField')()),
            ('chu_prilaborita', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('revidu', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('alighi', ['Noto'])

        # Adding model 'UEAValideco'
        db.create_table('alighi_ueavalideco', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kodo', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('lando', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('rezulto', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('alighi', ['UEAValideco'])

        # Adding unique constraint on 'UEAValideco', fields ['kodo', 'lando']
        db.create_unique('alighi_ueavalideco', ['kodo', 'lando'])

        # Adding model 'SenditaRetposhtajho'
        db.create_table('alighi_senditaretposhtajho', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('temo', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('teksto', self.gf('django.db.models.fields.TextField')()),
            ('sendadreso', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('ricevanto', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('partoprenanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Partoprenanto'], null=True)),
            ('retposhtajho', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Retposhtajho'], null=True)),
            ('traceback', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('dato', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('alighi', ['SenditaRetposhtajho'])


    def backwards(self, orm):
        # Removing unique constraint on 'UEAValideco', fields ['kodo', 'lando']
        db.delete_unique('alighi_ueavalideco', ['kodo', 'lando'])

        # Removing unique constraint on 'ManghoMendo', fields ['partoprenanto', 'tipo']
        db.delete_unique('alighi_manghomendo', ['partoprenanto_id', 'tipo_id'])

        # Removing unique constraint on 'ProgramKotizo', fields ['aghkategorio', 'landokategorio', 'alighkategorio']
        db.delete_unique('alighi_programkotizo', ['aghkategorio_id', 'landokategorio_id', 'alighkategorio_id'])

        # Removing unique constraint on 'Kurzo', fields ['valuto', 'dato']
        db.delete_unique('alighi_kurzo', ['valuto_id', 'dato'])

        # Deleting model 'Respondeco'
        db.delete_table('alighi_respondeco')

        # Deleting model 'Valuto'
        db.delete_table('alighi_valuto')

        # Deleting model 'Kurzo'
        db.delete_table('alighi_kurzo')

        # Deleting model 'AghKategorio'
        db.delete_table('alighi_aghkategorio')

        # Deleting model 'AlighKategorio'
        db.delete_table('alighi_alighkategorio')

        # Deleting model 'LandoKategorio'
        db.delete_table('alighi_landokategorio')

        # Deleting model 'Lando'
        db.delete_table('alighi_lando')

        # Deleting model 'LoghKategorio'
        db.delete_table('alighi_loghkategorio')

        # Deleting model 'ManghoTipo'
        db.delete_table('alighi_manghotipo')

        # Deleting model 'ProgramKotizo'
        db.delete_table('alighi_programkotizo')

        # Deleting model 'Pagmaniero'
        db.delete_table('alighi_pagmaniero')

        # Deleting model 'KrompagTipo'
        db.delete_table('alighi_krompagtipo')

        # Deleting model 'Retposhtajho'
        db.delete_table('alighi_retposhtajho')

        # Deleting model 'MembrighaKategorio'
        db.delete_table('alighi_membrighakategorio')

        # Deleting model 'Chambro'
        db.delete_table('alighi_chambro')

        # Deleting model 'UEARabato'
        db.delete_table('alighi_uearabato')

        # Deleting model 'Partoprenanto'
        db.delete_table('alighi_partoprenanto')

        # Deleting model 'ManghoMendoTipo'
        db.delete_table('alighi_manghomendotipo')

        # Deleting model 'ManghoMendo'
        db.delete_table('alighi_manghomendo')

        # Deleting model 'SurlokaMembrigho'
        db.delete_table('alighi_surlokamembrigho')

        # Deleting model 'Pagtipo'
        db.delete_table('alighi_pagtipo')

        # Deleting model 'Pago'
        db.delete_table('alighi_pago')

        # Deleting model 'MinimumaAntaupago'
        db.delete_table('alighi_minimumaantaupago')

        # Deleting model 'Nomshildo'
        db.delete_table('alighi_nomshildo')

        # Deleting model 'Noto'
        db.delete_table('alighi_noto')

        # Deleting model 'UEAValideco'
        db.delete_table('alighi_ueavalideco')

        # Deleting model 'SenditaRetposhtajho'
        db.delete_table('alighi_senditaretposhtajho')


    models = {
        'alighi.aghkategorio': {
            'Meta': {'object_name': 'AghKategorio'},
            'aldona_kotizo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limagho': ('django.db.models.fields.IntegerField', [], {}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'alighi.alighkategorio': {
            'Meta': {'object_name': 'AlighKategorio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limdato': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'alighi.chambro': {
            'Meta': {'object_name': 'Chambro'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'litonombro': ('django.db.models.fields.IntegerField', [], {}),
            'loghkategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.LoghKategorio']"}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'rimarko': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'alighi.krompagtipo': {
            'Meta': {'object_name': 'KrompagTipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sumo': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'alighi.kurzo': {
            'Meta': {'unique_together': "(('valuto', 'dato'),)", 'object_name': 'Kurzo'},
            'dato': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kurzo': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '5'}),
            'valuto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Valuto']"})
        },
        'alighi.lando': {
            'Meta': {'object_name': 'Lando'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.LandoKategorio']"}),
            'kodo': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'nomo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alighi.landokategorio': {
            'Meta': {'object_name': 'LandoKategorio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'alighi.loghkategorio': {
            'Meta': {'object_name': 'LoghKategorio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'plena_kosto': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'priskribo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'unutaga_kosto': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'alighi.manghomendo': {
            'Meta': {'unique_together': "(('partoprenanto', 'tipo'),)", 'object_name': 'ManghoMendo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partoprenanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Partoprenanto']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.ManghoMendoTipo']"})
        },
        'alighi.manghomendotipo': {
            'Meta': {'object_name': 'ManghoMendoTipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kosto': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'alighi.manghotipo': {
            'Meta': {'object_name': 'ManghoTipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'alighi.membrighakategorio': {
            'Meta': {'object_name': 'MembrighaKategorio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'alighi.minimumaantaupago': {
            'Meta': {'object_name': 'MinimumaAntaupago'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interna_antaupago': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'landokategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.LandoKategorio']"}),
            'oficiala_antaupago': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'alighi.nomshildo': {
            'Meta': {'object_name': 'Nomshildo'},
            'chu_havasnomshildon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'titolo_esperante': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'titolo_lokalingve': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alighi.noto': {
            'Meta': {'ordering': "('partoprenanto',)", 'object_name': 'Noto'},
            'chu_prilaborita': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dato': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enhavo': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partoprenanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Partoprenanto']", 'null': 'True', 'blank': 'True'}),
            'revidu': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uzanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'alighi.pagmaniero': {
            'Meta': {'object_name': 'Pagmaniero'},
            'chu_nurisraela': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_publika': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'komenta_etikedo': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '250', 'blank': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'alighi.pago': {
            'Meta': {'ordering': "('partoprenanto',)", 'object_name': 'Pago'},
            'dato': ('alighi.models.NeEstontecaDato', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pagmaniero': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Pagmaniero']"}),
            'pagtipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Pagtipo']"}),
            'partoprenanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Partoprenanto']"}),
            'rimarko': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sumo': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'uzanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'valuto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Valuto']"})
        },
        'alighi.pagtipo': {
            'Meta': {'object_name': 'Pagtipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'alighi.partoprenanto': {
            'Meta': {'ordering': "('familia_nomo',)", 'object_name': 'Partoprenanto'},
            'adreso': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'alighdato': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'alveno': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'antaupagos_ghis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.AlighKategorio']", 'null': 'True'}),
            'chambro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Chambro']", 'null': 'True', 'blank': 'True'}),
            'chu_alvenis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_bezonas_invitleteron': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_havasmanghkuponon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_havasnomshildon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_interesighas_pri_kurso': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chu_invitletero_sendita': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_komencanto': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chu_kontrolita': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_malnoktemulo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_postkongresalisto': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chu_preferas_unuseksan_chambron': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_retalisto': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chu_tuttaga_ekskurso': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chu_ueamembro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chu_unua_dua_ijk': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deziras_loghi_kun': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Partoprenanto']", 'null': 'True', 'blank': 'True'}),
            'deziras_loghi_kun_nomo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dua_konfirmilo_sendita': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ekde': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'familia_nomo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'foriro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ghis': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 26, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interesighas_pri_antaukongreso': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'interesighas_pri_postkongreso': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loghkategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.LoghKategorio']"}),
            'loghlando': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Lando']"}),
            'malalighdato': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'manghotipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.ManghoTipo']"}),
            'mesaghiloj': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'naskighdato': ('django.db.models.fields.DateField', [], {}),
            'organiza_kontribuo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pagmaniera_komento': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'pagmaniero': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Pagmaniero']"}),
            'persona_nomo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'poshtkodo': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'programa_kontribuo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'retposhtadreso': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sekso': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'shildlando': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'shildnomo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'uea_kodo': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'unua_konfirmilo_sendita': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'urbo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'alighi.programkotizo': {
            'Meta': {'unique_together': "(('aghkategorio', 'landokategorio', 'alighkategorio'),)", 'object_name': 'ProgramKotizo'},
            'aghkategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.AghKategorio']"}),
            'alighkategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.AlighKategorio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kotizo': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'landokategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.LandoKategorio']"})
        },
        'alighi.respondeco': {
            'Meta': {'object_name': 'Respondeco'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rolo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'uzanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'alighi.retposhtajho': {
            'Meta': {'object_name': 'Retposhtajho'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'sendadreso': ('django.db.models.fields.EmailField', [], {'default': "u'ijk@tejo.org'", 'max_length': '75'}),
            'teksto': ('django.db.models.fields.TextField', [], {}),
            'temo': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'alighi.senditaretposhtajho': {
            'Meta': {'object_name': 'SenditaRetposhtajho'},
            'dato': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partoprenanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Partoprenanto']", 'null': 'True'}),
            'retposhtajho': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Retposhtajho']", 'null': 'True'}),
            'ricevanto': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sendadreso': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'teksto': ('django.db.models.fields.TextField', [], {}),
            'temo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'traceback': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'alighi.surlokamembrigho': {
            'Meta': {'ordering': "('partoprenanto',)", 'object_name': 'SurlokaMembrigho'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.MembrighaKategorio']"}),
            'kotizo': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'partoprenanto': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alighi.Partoprenanto']", 'unique': 'True'}),
            'valuto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Valuto']"})
        },
        'alighi.uearabato': {
            'Meta': {'object_name': 'UEARabato'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landokategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.LandoKategorio']", 'unique': 'True'}),
            'sumo': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'alighi.ueavalideco': {
            'Meta': {'unique_together': "(('kodo', 'lando'),)", 'object_name': 'UEAValideco'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kodo': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'lando': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'rezulto': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'alighi.valuto': {
            'Meta': {'object_name': 'Valuto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kodo': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'nomo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['alighi']