# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
import hashlib, shutil, os.path

class Dosiero(models.Model):
    priskribo = models.CharField(max_length=250, blank=True,
        help_text=u'Ricevos la nomon de la dosiero se vi lasos ĝin malplena.')
    dosiero = models.FileField(upload_to=u'dosiero')
    
    def set_priskribo(self):
        if self.priskribo:
            return
        self.priskribo = self.dosiero.name

    @property
    def url(self):
        return self.dosiero.url

    @property
    def basename(self):
        return os.path.basename(self.dosiero.name)

    def save(self):
        self.set_priskribo()
        super(Dosiero, self).save()

    def delete(self):
        with open(self.dosiero.path, 'rb') as f:
            hash = hashlib.sha256(f.read()).hexdigest()
        newpath = os.path.join(
            settings.BACKUP_DIR,
            u'dosiero',
            u'{}.{}'.format(hash, self.basename))
        shutil.move(self.dosiero.path, newpath)
        super(Dosiero, self).delete()
        
    def __unicode__(self):
        return self.priskribo
        
    class Meta:
        verbose_name_plural = u'Dosieroj'