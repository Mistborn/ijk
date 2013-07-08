# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import hashlib
import shutil
import os.path

DOSIERO_UPLOAD_TO = getattr(settings, 'DOSIERO_UPLOAD_TO', 'dosiero')
DOSIERO_BACKUP_DIR = getattr(settings, 'DOSIERO_BACKUP_DIR', None)


class Dosiero(models.Model):
    priskribo = models.CharField(max_length=250, blank=True,
        verbose_name=_('Description'),
        help_text=_('Will be set to the file name if left blank'))
    dosiero = models.FileField(upload_to=DOSIERO_UPLOAD_TO,
                               verbose_name=_('File'))

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
        if DOSIERO_BACKUP_DIR is not None:
            with open(self.dosiero.path, 'rb') as f:
                filehash = hashlib.sha256(f.read()).hexdigest()
            newpath = os.path.join(
                DOSIERO_BACKUP_DIR, '{}.{}'.format(filehash, self.basename))
            shutil.move(self.dosiero.path, newpath)
        super(Dosiero, self).delete()

    def __unicode__(self):
        return self.priskribo

    class Meta:
        verbose_name = _('Dosiero file')
        verbose_name_plural = _('Dosiero files')
