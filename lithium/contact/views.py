from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext

from lithium.contact.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save([manager[1] for manager in settings.MANAGERS])
            return HttpResponseRedirect(reverse('contact_confirmation'))
    else:
        form = ContactForm()
    
    return render_to_response('contact/contact_form.html', {'form':form,}, context_instance=RequestContext(request))
