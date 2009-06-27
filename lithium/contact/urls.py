from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'lithium.contact.views.contact', name="contact_form"),
    url(r'^sent/$', 'django.views.generic.simple.direct_to_template', 
        { 'template': 'contact/contact_confirmation.html' }, "contact_confirmation"),
)
