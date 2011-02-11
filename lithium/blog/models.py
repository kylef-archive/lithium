import datetime

try:
    from xmlrpclib import Server as XMPRPCServer
except ImportError:
    XMPRPCServer = None

from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.comments import moderation

from lithium.conf import settings
from lithium.blog.managers import CurrentSitePostManager

class Category(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'))
    favorite = models.BooleanField(_('favorite'), default=False, help_text=_("Whether this category should be included in category lists."))
    
    class Meta:
        verbose_name_plural = _('categories')
        ordering = ('title',)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return ('blog.category_detail', None, {'tag': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

class Post(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    
    content = models.TextField(_('content'), blank=True)
    
    pub_date = models.DateTimeField(_('published date'), default=datetime.datetime.now)
    is_public = models.BooleanField(_('is public'), default=False)
    enable_comments = models.BooleanField(_('enable comments'), default=settings.ENABLE_COMMENTS_BY_DEFAULT)
    sites = models.ManyToManyField(Site)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category, blank=True)
    
    on_site = CurrentSitePostManager('sites')
    objects = models.Manager()
    
    class Meta:
        ordering = ('-pub_date',)
        permissions = (('can_read_private', 'Can read private posts'),)
    
    def __unicode__(self):
        return self.title
    
    #@models.permalink
    def get_absolute_url(self):
        return ('blog.post_detail', None, {
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%b").lower(),
            'day': self.pub_date.strftime("%d"),
            'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_next_post(self):
        return self.get_next_by_pub_date()
    
    def get_previous_post(self):
        return self.get_previous_by_pub_date()

def ping_post(sender, instance, signal, *args, **kwargs):
    if settings.BLOG_PING:
        if instance.is_public == True:
            site = Site.objets.get_current()
            blog = 'http://%s%s' % (site.domain, reverse('lithium.blog.views.post_list'))
            post = 'http://%s%s' % (site.domain, instance.get_absolute_url())
            for server in settings.BLOG_PING_SERVERS:
                if XMPRPCServer:
                    j = XMPRPCServer(server)
                    reply = j.weblogUpdates.ping(site.name, blog, post)

models.signals.post_save.connect(ping_post, sender=Post)

class PostCommentModerator(moderation.CommentModerator):
    enabled_field = 'enable_comments'
moderation.moderator.register(Post, PostCommentModerator)
