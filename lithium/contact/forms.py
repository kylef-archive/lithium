from django import forms
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
    subject = forms.CharField(label=_('Subject'), max_length=100)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)
    sender = forms.EmailField(label=_('Email address'), help_text=_('A valid e-mail address, please.'))
    cc_myself = forms.BooleanField(label=_('Send a copy to yourself?'), required=False)
