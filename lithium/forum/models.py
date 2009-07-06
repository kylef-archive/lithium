import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from lithium.forum.managers import ForumManager, ThreadManager

class Forum(models.Model):
    """
    # Create some forums
    >>> public = Forum.objects.create(title='Public', slug='public')
    >>> private = Forum.objects.create(title='Private', slug='private')
    
    # Create some sub-forums
    >>> sub1 = Forum.objects.create(title='Sub Public 1', slug='sub-public-1', parent=public)
    >>> sub2 = Forum.objects.create(title='Sub Public 2', slug='sub-public-2', parent=public)
    
    # They're all in order
    >>> Forum.objects.all()
    [<Forum: Public>, <Forum: Sub Public 1>, <Forum: Sub Public 2>, <Forum: Private>]
    
    # Delete a forum
    >>> public.delete()
    
    # All sub-forums we're also deleted.
    >>> Forum.objects.all()
    [<Forum: Private>]
    
    # Check the position is 1
    >>> Forum.objects.all()[0].position
    1
    """
    
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    description = models.TextField(_('description'), blank=True)
    is_category = models.BooleanField(_('is category'), default=False, help_text=_('Categories cannot contain threads/posts'))
    
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    position = models.PositiveIntegerField(_('position'), editable=False, default=0)
    level = models.PositiveIntegerField(_('level'), editable=False, default=0)
    
    objects = ForumManager()
    
    class Meta:
        ordering = ('position',)
    
    def __str__(self):
        return self.title
    
    def siblings(self, include_self=False):
        """
        Every forum on the current 'level'.
        """
        qs = Forum.objects.all()
        
        if not self.parent:
            qs = qs.filter(parent__isnull=True)
        else:
            qs = qs.filter(parent=self.parent)
        
        if not include_self:
            qs = qs.exclude(pk=self.pk)
        
        return qs
    
    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                # Although we dont actually want to include ourselfs, since we are not
                # inserted to the db, we cannot be excluded from the query.
                self.position = self.siblings(include_self=True).only('position').order_by('-position')[0].position + 1
            except IndexError:
                if self.parent:
                    self.position = self.parent.position + 1
                else:
                    try:
                        self.position = Forum.objects.only('position').order_by('-position')[0].position + 1
                    except IndexError:
                        self.position = 1
            
            if self.position != 1:
                Forum.objects.update_position(self.position)
            
            if self.parent:
                self.level = self.parent.level + 1
        super(Forum, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        for child in self.children.all():
            child.delete()
        
        # Our position could have changed due to children
        position = Forum.objects.get(pk=self.pk).position
        super(Forum, self).delete(*args, **kwargs)
        
        Forum.objects.update_position(position, increment=False)

class Thread(models.Model):
    """
    # Looup a forum from earlier
    >>> f = Forum.objects.all()[0]
    
    # Create a thread
    >>> t = Thread.objects.create(forum=f, title='Thread One', slug='thread-one')
    >>> t.save()
    
    # Create a post
    >>> Post.objects.create(thread=t, content='test').save()
    
    # Create another thread
    >>> t2 = Thread.objects.create(forum=f, title='Thread Two', slug='thread-two')
    >>> t2.save()
    
    # Create a post in this new thread
    >>> Post.objects.create(thread=t2, content='test').save()
    
    # There are now two threads in the forum
    >>> Forum.objects.all()[0].thread_count
    2
    
    # The threads are in the correct order
    >>> Thread.objects.all()
    [<Thread: Thread Two>, <Thread: Thread One>]
    
    # Create a new post (moving the old thread infront of the new thread)
    >>> Post.objects.create(thread=t, content='test2').save()
    >>> Thread.objects.all()
    [<Thread: Thread One>, <Thread: Thread Two>]
    """
    forum = models.ForeignKey(Forum)
    
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    
    is_sticky = models.BooleanField(_('is sticky'), default=False)
    is_locked = models.BooleanField(_('is locked'), default=False)
    
    objects = ThreadManager()
    
    def __unicode__(self):
        return self.title

class Post(models.Model):
    content = models.TextField(_('content'))
    
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User, related_name='forum_post_set', null=True, blank=True)
    pub_date = models.DateTimeField(_('published date'), default=datetime.datetime.now)
    
    class Meta:
        ordering = ('pub_date',)
    
    def __unicode__(self):
        return u'%s' % self.content[:20]
