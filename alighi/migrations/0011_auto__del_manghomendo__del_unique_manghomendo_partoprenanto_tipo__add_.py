# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ManghoMendo', fields ['partoprenanto', 'tipo']
        db.delete_unique('alighi_manghomendo', ['partoprenanto_id', 'tipo_id'])

        # Deleting model 'ManghoMendo'
        db.delete_table('alighi_manghomendo')

        # Adding field 'Lando.xnomo'
        db.add_column('alighi_lando', 'xnomo',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=55),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ManghoMendo'
        db.create_table('alighi_manghomendo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partoprenanto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.Partoprenanto'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alighi.ManghoMendoTipo'])),
        ))
        db.send_create_signal('alighi', ['ManghoMendo'])

        # Adding unique constraint on 'ManghoMendo', fields ['partoprenanto', 'tipo']
        db.create_unique('alighi_manghomendo', ['partoprenanto_id', 'tipo_id'])

        # Deleting field 'Lando.xnomo'
        db.delete_column('alighi_lando', 'xnomo')


    models = {
        'alighi.aghkategorio': {
            'Meta': {'object_name': 'AghKategorio'},
            'aldona_kotizo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limagho': ('django.db.models.fields.IntegerField', [], {}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'alighi.alighkategorio': {
            'Meta': {'object_name': 'AlighKategorio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limdato': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
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
            'Meta': {'ordering': "('kodo',)", 'object_name': 'Lando'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kategorio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.LandoKategorio']"}),
            'kodo': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'nomo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'xnomo': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'alighi.landokategorio': {
            'Meta': {'object_name': 'LandoKategorio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'priskribo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'alighi.loghkategorio': {
            'Meta': {'object_name': 'LoghKategorio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nomo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'plena_kosto': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'priskribo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'unutaga_kosto': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
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
            'priskribo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'alighi.pago': {
            'Meta': {'ordering': "('partoprenanto',)", 'object_name': 'Pago'},
            'dato': ('alighi.models.NeEstontecaDato', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kreinto': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pagokreinto'", 'null': 'True', 'to': "orm['auth.User']"}),
            'lasta_redaktanto': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pagoredaktanto'", 'null': 'True', 'to': "orm['auth.User']"}),
            'pagmaniero': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Pagmaniero']"}),
            'pagtipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Pagtipo']"}),
            'partoprenanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Partoprenanto']"}),
            'respondeculo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pagorespondeculo'", 'to': "orm['auth.User']"}),
            'rimarko': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sumo': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
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
            'manghomendoj': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alighi.ManghoMendoTipo']", 'symmetrical': 'False'}),
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
        'alighi.senditaoficialajho': {
            'Meta': {'object_name': 'SenditaOficialajho'},
            'alshutinto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'alshutodato': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dosiero': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partoprenanto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alighi.Partoprenanto']", 'null': 'True', 'blank': 'True'}),
            'priskribo': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
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
            'landokategorio': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alighi.LandoKategorio']", 'unique': 'True'}),
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