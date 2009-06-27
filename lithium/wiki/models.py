import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

PAGE_PERMISSIONS = (
    (0, 'Use global setting'),
    (1, 'Anonymous'),
    (2, 'User'),
    (3, 'Superuser'),
)

class Page(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    permission = models.IntegerField(_('permission'), choices=PAGE_PERMISSIONS, help_text=_('Who can edit this page.'), default=0)
    
    def __unicode__(self):
        return self.title
    
    #@property
    def revision(self):
        return self.revision_set.latest('pub_date')
    revision = property(revision)
    
    #@property
    def content(self):
        return self.revision.content
    content = property(content)

class Revision(models.Model):
    page = models.ForeignKey(Page)
    text = models.ForeignKey('Text', blank=True, null=True)
    comment = models.CharField(_('comment'), max_length=255, blank=True, help_text=_('A short description of the changes you have made.'))
    pub_date = models.DateTimeField(_('published'), default=datetime.datetime.now, blank=True)
    
    author = models.ForeignKey(User, blank=True, null=True)
    author_ip = models.IPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ('-pub_date',)
    
    def __unicode__(self):
        return u'%s' % self.pk
    
    #@property
    def content(self):
        if self.text:
            return self.text.content
        else:
            return ''
    content = property(content)

class Text(models.Model):
    content = models.TextField(_('content'), blank=True)
    
    def __unicode__(self):
        return self.content
