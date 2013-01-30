# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe

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

    def save(self):
        self.set_priskribo()
        super(Dosiero, self).save()
        
    def __unicode__(self):
        return self.priskribo
        
    class Meta:
        verbose_name_plural = u'Dosieroj'