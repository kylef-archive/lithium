from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from lithium.forum.models import Forum, Post
from lithium.forum.utils import user_permission_level

class LatestPostFeed(Feed):
    def get_object(self, request, slug=None):
        self.request = request
        if slug:
            user_permission = user_permission_level(request.user)
            return get_object_or_404(Forum, slug=slug, read__lte=user_permission)

    def link(self, obj):
        if obj:
            return obj.get_absolute_url()
        return reverse('forum.forum_index')

    def title(self, obj):
        if obj:
            return obj.title
        return 'All posts'

    def description(self, obj):
        if obj:
            return obj.description
        return 'All posts'

    def items(self, obj):
        user_permission = user_permission_level(self.request.user)
        return Post.objects.prefetch_related('thread__forum').filter(thread__forum__read__lte=user_permission)[:20]

    def item_title(self, item):
        return item.thread.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_categories(self, item):
        return [item.thread.title]

