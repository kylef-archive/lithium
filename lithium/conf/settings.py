from django.conf import settings

MEDIA_URL = getattr(settings, 'MEDIA_URL', None)
DEBUG = getattr(settings, 'DEBUG', False)
SITE_ID = getattr(settings, 'SITE_ID', 1)

# lithium
ENABLE_COMMENTS_BY_DEFAULT = getattr(settings, 'ENABLE_COMMENTS_BY_DEFAULT', True)

# lithium.blog
BLOG_PAGINATE_BY = getattr(settings, 'BLOG_PAGINATE_BY', 10)
BLOG_PING = getattr(settings, 'BLOG_PING', False)
BLOG_PING_SERVERS = getattr(settings, 'BLOG_PING_SERVERS', (
    'http://blogsearch.google.com/ping/RPC2',
    'http://rpc.technorati.com/rpc/ping',
    'http://api.my.yahoo.com/rss/ping',
    'http://ping.feedburner.com',
))
BLOG_FEED_ITEMS = getattr(settings, 'BLOG_FEED_ITEMS', 20)

# lithium.wiki
WIKI_DEFAULT_USER_PERMISSION = getattr(settings, 'WIKI_DEFAULT_USER_PERMISSION', 1)
WIKI_HISTORY_PAGINATE_BY = getattr(settings, 'WIKI_HISTORY_PAGINATE_BY', 50)

# lithium.forum
FORUM_THREAD_PAGINATE_BY = getattr(settings, 'FORUM_THREAD_PAGINATE_BY', 40)
FORUM_POST_PAGINATE_BY = getattr(settings, 'FORUM_POST_PAGINATE_BY', 20)
FORUM_DEFAULT_READ_PERMISSION = getattr(settings, 'FORUM_DEFAULT_READ_PERMISSION', 1)
FORUM_DEFAULT_WRITE_PERMISSION = getattr(settings, 'FORUM_DEFAULT_WRITE_PERMISSION', 2)
