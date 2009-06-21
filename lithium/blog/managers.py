import datetime
from django.contrib.sites.managers import CurrentSiteManager
from lithium.conf import settings

class CurrentSitePostManager(CurrentSiteManager):
    def all(self, allow_private=False):
        queryset = self.get_query_set()
        
        if allow_private:
            return queryset.all()
        else:
            return queryset.filter(is_public=True)
    
    def disallow_future(self):
        return self.all().filter(pub_date__lte=datetime.datetime.now())
