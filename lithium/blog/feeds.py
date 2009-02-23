from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from lithium.conf import settings
from lithium.blog.models import Post

class LatestPosts(Feed):
    site = Site.objects.get_current()
    title = '%s feed' % site.name
    link = '/posts/'
    description = 'Latest posts at %s' % site.name
    description_template = 'blog/feed_description.html'
    
    def item_pubdate(self, item):
        return item.pub_date
    
    def item_author_name(self, item):
        return '%s %s' % (item.author.first_name, item.author.last_name)
    
    def item_author_email(self, item):
        return item.author.email
    
    def items(self):
        return Post.on_site.all()[:settings.BLOG_FEED_ITEMS]

class LatestPostsByTag(LatestPosts):
    def get_object(self, tags):
        if len(tags) != 1:
            raise ObjectDoesNotExist
        self.tag = tags[0]
    
    def items(self):
        return Post.on_site.filter(category__slug=self.tag)[:settings.BLOG_FEED_ITEMS]

class LatestPostsByAuthor(LatestPosts):
    def get_object(self, authors):
        if len(authors) != 1:
            raise ObjectDoesNotExist
        self.author = authors[0]
    
    def items(self):
        return Post.on_site.filter(author__username=self.author)[:settings.BLOG_FEED_ITEMS]
