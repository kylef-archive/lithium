from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

class ContactForm(forms.Form):
    subject = forms.CharField(label=_('Subject'), max_length=100)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)
    sender = forms.EmailField(label=_('Email address'), help_text=_('A valid e-mail address, please.'))
    cc_myself = forms.BooleanField(label=_('Send a copy to yourself?'), required=False)
    
    def save(self, recipients=[]):
        if form.errors:
            raise ValueError("The ContactForm could not be saved because the data didn't validate.")
        
        if self.cleaned_data['cc_myself']:
            recipients.append(self.cleaned_data['sender'])
        
        send_mail(self.cleaned_data['subject'], self.cleaned_data['message'],
            self.cleaned_data['sender'], recipients)
