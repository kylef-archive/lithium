import datetime
from django.contrib.sites.managers import CurrentSiteManager
from lithium.conf import settings

class CurrentSitePostManager(CurrentSiteManager):
    def get_query_set(self):
        queryset = super(CurrentSitePostManager, self).get_query_set()
        return queryset.filter(is_public=True, pub_date__lte=datetime.datetime.now())
