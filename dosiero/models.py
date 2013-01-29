from django.db import models

class Dosiero(models.Model):
    priskribo = models.CharField(max_length=250)
    dosiero = models.FileField(upload_to=u'dosiero')
    
    def set_priskribo(self):
        if self.priskribo:
            return
        self.priskribo = self.dosiero.name
        
    def __unicode__(self):
        return self.priskribo
        
    class Meta:
        verbose_name_plural = u'Dosieroj'