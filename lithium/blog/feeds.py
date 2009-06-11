from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from lithium.conf import settings
from lithium.blog.models import Post

class LatestPosts(Feed):
    site = Site.objects.get_current()
    description_template = 'blog/feed_description.html' 
    
    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return u"%s feed" % self._site.name
    
    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % (self._site.domain)
    
    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return u"Latest posts at %s" % self._site.name
    
    def item_pubdate(self, item):
        return item.pub_date
    
    def item_author_name(self, item):
        return '%s %s' % (item.author.first_name, item.author.last_name)
    
    def item_author_email(self, item):
        return item.author.email
    
    def get_query_set(self):
        return Post.on_site.disallow_future()
    
    def items(self):
        return self.get_query_set()[:settings.BLOG_FEED_ITEMS]

class LatestPostsByTag(LatestPosts):
    def get_object(self, tags):
        if len(tags) != 1:
            raise ObjectDoesNotExist
        self.tag = tags[0]
    
    def items(self):
        return self.get_query_set().filter(category__slug=self.tag)[:settings.BLOG_FEED_ITEMS]

class LatestPostsByAuthor(LatestPosts):
    def get_object(self, authors):
        if len(authors) != 1:
            raise ObjectDoesNotExist
        self.author = authors[0]
    
    def items(self):
        return self.get_query_set().filter(author__username=self.author)[:settings.BLOG_FEED_ITEMS]
