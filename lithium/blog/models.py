import datetime

try:
    from xmlrpclib import Server as XMPRPCServer
except ImportError:
    XMPRPCServer = None

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from lithium.conf import settings
from lithium.blog.managers import PostManager, CurrentSitePostManager

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    favorite = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('title',)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return ('blog.category_detail', None, {'tag': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    content = models.TextField(blank=True)
    
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    is_public = models.BooleanField(default=False)
    enable_comments = models.BooleanField(default=settings.ENABLE_COMMENTS_BY_DEFAULT)
    sites = models.ManyToManyField(Site)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category, blank=True)
    
    objects = PostManager()
    on_site = CurrentSitePostManager('sites')
    
    class Meta:
        ordering = ('-pub_date',)
    
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
        return self.get_next_by_pub_date(is_public=True, sites=settings.SITE_ID)
    
    def get_previous_post(self):
        return self.get_next_by_previous(is_public=True, sites=settings.SITE_ID)

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
