from django.conf.urls.defaults import *
from django.core.urlresolvers import get_callable
from django.core.urlresolvers import RegexURLPattern

from lithium.conf import settings
from lithium.views.date_based import *
from lithium.blog.models import Post
from lithium.blog.feeds import LatestPosts, LatestPostsByTag, LatestPostsByAuthor
from lithium.blog.decorators import private_post_decorator

list_dict = {
    'queryset': Post.on_site.all(),
    'date_field': 'pub_date',
    'paginate_by': settings.BLOG_PAGINATE_BY,
    'template_object_name': 'post',
}

detail_dict = {
    'queryset': Post.on_site.all(),
    'date_field': 'pub_date',
    'template_object_name': 'post',
}

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', private_post_decorator(object_detail), detail_dict, 'blog.post_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', private_post_decorator(archive_day), list_dict, 'blog.archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',  private_post_decorator(archive_month), list_dict, 'blog.archive_month'),
    url(r'^(?P<year>\d{4})/$',  private_post_decorator(archive_year), list_dict, 'blog.archive_year'),
    url(r'^$',  private_post_decorator(archive_index), list_dict, 'blog.post_list'),
    url(r'^author/(?P<author>[-\w]+)/?$',  private_post_decorator(archive_index), list_dict, 'blog.author_detail'),
    url(r'^tag/(?P<tag>[-\w]+)/$',  private_post_decorator(archive_index), list_dict, 'blog.category_detail'),
)

feeds = {
    'latest': LatestPosts,
    'tag': LatestPostsByTag,
    'author': LatestPostsByAuthor,
}

urlpatterns += patterns('django.contrib.syndication.views',
    url(r'^feed/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}, name='blog.feeds'),
)
