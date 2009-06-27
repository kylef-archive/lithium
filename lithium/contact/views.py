from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings

from lithium.contact.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            recipients = []
            
            if settings.MANAGERS:
                for manager in settings.MANAGERS:
                    recipients.append(manager[1])
            
            form.save(recipients)
            
            return HttpResponseRedirect(reverse('contact_confirmation'))
    else:
        form = ContactForm()
    
    return render_to_response('contact/contact_form.html', {'form':form,})
