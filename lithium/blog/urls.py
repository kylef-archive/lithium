from django.conf.urls.defaults import *
from django.core.urlresolvers import get_callable
from django.core.urlresolvers import RegexURLPattern

from lithium.conf import settings
from lithium.blog.models import Post
from lithium.blog.feeds import LatestPosts, LatestPostsByTag, LatestPostsByAuthor

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

def patterns_decorator(decorator, prefix, *args):
    """
    This method applies a decorator to each url.
    """
    pattern_list = []
    for t in args:
        if isinstance(t, (list, tuple)):
            t = url(prefix=prefix, *t)
        elif isinstance(t, RegexURLPattern):
            t.add_prefix(prefix)
        
        # Add the real view to the dict
        if t._callback:
            t.default_args['view'] = t._callback
        else:
            t.default_args['view'] = get_callable(t._callback_str)
        
        # Give the RegexURLPattern the decorator
        if callable(decorator):
            t._callback = decorator
        else:
            t._callback = None
            t._callback_str = decorator
        
        pattern_list.append(t)
    return pattern_list

urlpatterns = patterns_decorator('lithium.blog.views.decorator', 'lithium.views.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', detail_dict, 'blog.post_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', list_dict, 'blog.archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', list_dict, 'blog.archive_month'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', list_dict, 'blog.archive_year'),
    url(r'^$', 'archive_index', list_dict, 'blog.post_list'),
    url(r'^author/(?P<author>[-\w]+)/?$', 'archive_index', list_dict, 'blog.author_detail'),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'archive_index', list_dict, 'blog.category_detail'),
)

feeds = {
    'latest': LatestPosts,
    'tag': LatestPostsByTag,
    'author': LatestPostsByAuthor,
}

urlpatterns += patterns('django.contrib.syndication.views',
    url(r'^feed/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}, name='blog.feeds'),
)
