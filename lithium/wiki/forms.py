from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from lithium.wiki.models import Revision, Text

class EditForm(forms.Form):
    text = forms.CharField(label=_('Text'), widget=forms.Textarea)
    comment = forms.CharField(label=_('Comment'), max_length=255, required=False,
        help_text=_('A short description of the changes you have made.'))
    
    def __init__(self, request, page, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.request = request
        self.page = page
        self.instance = Revision()
    
    def save(self, *args, **kwargs):
        if self.request.user.is_anonymous():
            self.instance.author_ip = self.request.META['REMOTE_ADDR']
        else:
            self.instance.author = self.request.user
        
        if not self.page.pk:
            self.page.save()
        self.instance.page = self.page
        
        text, created = Text.objects.get_or_create(content=self.cleaned_data['text'])
        self.instance.text = text
        
        self.instance.comment = self.cleaned_data['comment']
        
        if not created:
            try:
                revision = text.revision_set.latest('pub_date')
                self.instance.comment = _(u'Reverted to revision %(revision)s by %(author)s') % {'revision':revision.pk, 'author':revision.author or revision.author_ip}
            except ObjectDoesNotExist:
                pass
        
        self.instance.save()
