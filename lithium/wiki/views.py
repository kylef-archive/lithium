from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.utils.http import urlquote
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

from lithium.wiki.models import Page, Revision
from lithium.wiki.forms import EditForm
from lithium.wiki.utils import title

def page_detail(request, slug):
    try:
        page = Page.objects.filter(slug=slug).get()
    except ObjectDoesNotExist:
        page = Page(title=title(slug), slug=slug)
    
    return render_to_response('wiki/page_detail.html',
        {'page':page, 'page_exists': bool(page.pk)}, RequestContext(request))

def page_edit(request, slug):
    try:
        page = Page.objects.filter(slug=slug).get()
    except ObjectDoesNotExist:
        page = Page(title=title(slug), slug=slug)
    
    if not page.user_can_edit(request.user):
        if request.user.is_anonymous():
            return HttpResponseRedirect('%s?%s=%s' % (settings.LOGIN_URL, REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
        else:
            return render_to_response('wiki/permission_denied.html', context_instance=RequestContext(request))
    
    if request.method == 'POST':
        form = EditForm(request, page, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        if page.content:
            form = EditForm(request, page, {'text': page.content})
        else:
            form = EditForm(request, page)
    
    template_context = {
        'page': page,
        'form': form,
    }
    
    return render_to_response('wiki/page_edit.html', template_context, RequestContext(request))

def revision_detail(request, slug, pk):
    try:
        revision = Revision.objects.filter(page__slug=slug, pk=pk).get()
    except ObjectDoesNotExist:
        raise Http404, "No revision found matching the query"
    
    return render_to_response('wiki/revision_detail.html', {'revision': revision,}, RequestContext(request))
