import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from lithium.conf import settings
from lithium.wiki.utils import title, user_permission_level

PAGE_PERMISSIONS = (
    (0, 'Use global setting'),
    (1, 'Anonymous'),
    (2, 'User'),
    (3, 'Staff'),
    (4, 'Superuser'),
)

class Page(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    title = models.CharField(_('title'), max_length=255, blank=True)
    slug = models.SlugField(_('slug'))
    write_permission = models.IntegerField(_('write permission'), choices=PAGE_PERMISSIONS, help_text=_('Who can edit this page.'), default=0)
    read_permission = models.IntegerField(_('read permission'), choices=PAGE_PERMISSIONS, help_text=_('Who can read this page.'), default=0)

    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('wiki.page_detail', None, {'slug': self.slug})
    
    @models.permalink
    def get_edit_url(self):
        return ('wiki.page_edit', None, {'slug': self.slug})
    
    @models.permalink
    def get_discuss_url(self):
        return ('wiki.page_discuss', None, {'slug': self.slug})
    
    @models.permalink
    def get_history_url(self):
        return ('wiki.page_history', None, {'slug': self.slug})
    
    @models.permalink
    def get_children_url(self):
        return ('wiki.page_children', None, {'slug': self.slug})

    def get_read_permission(self):
        if self.read_permission:
            return self.read_permission

        if self.parent:
            return self.parent.get_read_permission()

        return settings.WIKI_DEFAULT_READ_PERMISSION

    def get_write_permission(self):
        if self.write_permission:
            return self.write_permission

        if self.parent:
            return self.parent.get_write_permission()

        return settings.WIKI_DEFAULT_WRITE_PERMISSION

    def user_can_edit(self, user):
        return user_permission_level(user) >= self.get_write_permission()

    def has_read_permission(self, user):
        return user_permission_level(user) >= self.get_read_permission()
    
    @property
    def revision(self):
        try:
            return self.revision_set.latest('pub_date')
        except ObjectDoesNotExist:
            return None
    
    @property
    def content(self):
        if self.revision:
            return self.revision.content
        else:
            return ''
    
    def has_children(self):
        if not self.pk:
            return 0
        return self.children.count() > 0
    
    def delete(self, *args, **kwargs):
        for child in self.children.all():
            child.delete()

        super(Page, self).delete(*args, **kwargs)

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
    
    @models.permalink
    def get_absolute_url(self):
        return ('wiki.revision_detail', None, {'slug': self.page.slug, 'pk': self.pk})
    
    @models.permalink
    def get_revert_url(self):
        return ('wiki.revision_revert', None, {'slug': self.page.slug, 'pk': self.pk})
    
    @property
    def title(self):
        return self.page.title
    
    @property
    def content(self):
        if self.text:
            return self.text.content
        else:
            return ''

class Text(models.Model):
    content = models.TextField(_('content'), blank=True)
    
    def __unicode__(self):
        return self.content
