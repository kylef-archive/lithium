from django import forms
from django.utils.translation import ugettext_lazy as _

from lithium.forum.models import Thread, Post

class ThreadCreateForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=255)
    content = forms.CharField(label=_('Content'), widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(ThreadCreateForm, self).__init__(*args, **kwargs)
        self.thread = Thread()
        self.post = Post()
    
    def save(self):
        self.thread.title = self.cleaned_data['title']
        self.thread.save()
        
        self.post.thread = self.thread
        self.post.content = self.cleaned_data['content']
        self.post.save()

class ThreadReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
