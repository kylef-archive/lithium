from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label='Email address', help_text='A valid e-mail address, please.')
    cc_myself = forms.BooleanField(required=False, label='Send a copy to yourself?')
