import datetime
from django.db.models import Manager
from django.contrib.sites.managers import CurrentSiteManager
from lithium.conf import settings

class PostManager(Manager):
    def get_query_set(self):
        queryset = super(PostManager, self).get_query_set()
        return queryset.filter(is_public=True, pub_date__lte=datetime.datetime.now())

class CurrentSitePostManager(CurrentSiteManager):
    def get_query_set(self):
        queryset = super(CurrentSitePostManager, self).get_query_set()
        return queryset.filter(is_public=True, pub_date__lte=datetime.datetime.now())
