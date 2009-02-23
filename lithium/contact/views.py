from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings

from lithium.contact.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = []
            
            if settings.MANAGERS:
                for manager in settings.MANAGERS:
                    recipients.append(manager[1])
            
            if cc_myself:
                recipients.append(sender)
            
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect(reverse('contact_confirmation'))
    else:
        form = ContactForm()
    
    return render_to_response('contact/contact_form.html', {'form':form,})
