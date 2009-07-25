from django.conf.urls.defaults import *
from lithium.wiki.models import Page

urlpatterns = patterns('lithium.wiki.views',
    url(r'^$', 'page_detail', dict(slug='Start'), 'wiki.start_page'),
    url(r'^(?P<slug>[-\w]+)/$', 'page_detail', name='wiki.page_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'page_edit', name='wiki.page_edit'),
    url(r'^(?P<slug>[-\w]+)/history/$', 'page_history', name='wiki.page_history'),
    url(r'^(?P<slug>[-\w]+)/discuss/$', 'page_discuss', name='wiki.page_discuss'),
    url(r'^(?P<slug>[-\w]+)/children/$', 'page_children', name='wiki.page_children'),
    url(r'^(?P<slug>[-\w]+)/(?P<pk>[\d]+)/$', 'revision_detail', name='wiki.revision_detail'),
    url(r'^(?P<slug>[-\w]+)/revert/(?P<pk>[\d]+)/$', 'revision_revert', name='wiki.revision_revert'),
    url(r'^(?P<slug>[-\w]+)/diff$', 'revision_diff', name='wiki.revision_diff'),
)
