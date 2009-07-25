import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from lithium.conf import settings
from lithium.wiki.utils import title

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
    permission = models.IntegerField(_('permission'), choices=PAGE_PERMISSIONS, help_text=_('Who can edit this page.'), default=0)
    
    def __unicode__(self):
        return self.title
    
    #@models.permalink
    def get_absolute_url(self):
        return ('wiki.page_detail', None, {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
    #@models.permalink
    def get_edit_url(self):
        return ('wiki.page_edit', None, {'slug': self.slug})
    get_edit_url = models.permalink(get_edit_url)
    
    #@models.permalink
    def get_discuss_url(self):
        return ('wiki.page_discuss', None, {'slug': self.slug})
    get_discuss_url = models.permalink(get_discuss_url)
    
    #@models.permalink
    def get_history_url(self):
        return ('wiki.page_history', None, {'slug': self.slug})
    get_history_url = models.permalink(get_history_url)
    
    #@models.permalink
    def get_children_url(self):
        return ('wiki.page_children', None, {'slug': self.slug})
    get_children_url = models.permalink(get_children_url)
    
    def user_can_edit(self, user):
        permission = self.permission or settings.WIKI_DEFAULT_USER_PERMISSION
        user_perm = int(not user.is_anonymous()) + 1
        
        if user.is_staff:
            user_perm = 3
        
        if user.is_superuser:
            user_perm = 4
        
        return user_perm >= permission
    
    #@property
    def revision(self):
        try:
            return self.revision_set.latest('pub_date')
        except ObjectDoesNotExist:
            return None
    revision = property(revision)
    
    #@property
    def content(self):
        if self.revision:
            return self.revision.content
        else:
            return ''
    content = property(content)
    
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
    
    #@models.permalink
    def get_absolute_url(self):
        return ('wiki.revision_detail', None, {'slug': self.page.slug, 'pk': self.pk})
    get_absolute_url = models.permalink(get_absolute_url)
    
    #@models.permalink
    def get_revert_url(self):
        return ('wiki.revision_revert', None, {'slug': self.page.slug, 'pk': self.pk})
    get_revert_url = models.permalink(get_revert_url)
    
    #@property
    def title(self):
        return self.page.title
    title = property(title)
    
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
