import datetime
from django.contrib.sites.managers import CurrentSiteManager
from lithium.conf import settings

class CurrentSitePostManager(CurrentSiteManager):
    def get_query_set(self):
        queryset = super(CurrentSitePostManager, self).get_query_set()
        return queryset.filter(is_public=True)
    
    def disallow_future(self):
        return self.get_query_set().filter(pub_date__lte=datetime.datetime.now())
