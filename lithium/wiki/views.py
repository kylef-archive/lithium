import difflib

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    
    def pygments_diff(data):
        return highlight(data, get_lexer_by_name('diff'), HtmlFormatter())
    
except ImportError:
    def pygments_diff(data):
        return data

from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.utils.http import urlquote
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic.list_detail import object_list
from django.utils.translation import ugettext_lazy as _

from lithium.conf import settings
from lithium.wiki.models import Page, Revision
from lithium.wiki.forms import EditForm
from lithium.wiki.utils import title

def page_detail(request, slug, template_name='wiki/page_detail.html'):
    try:
        page = Page.objects.filter(slug=slug).get()
    except ObjectDoesNotExist:
        page = Page(title=title(slug), slug=slug)
    
    return render_to_response(template_name,
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

def page_discuss(request, *args, **kwargs):
    return page_detail(request, template_name='wiki/page_discuss.html', *args, **kwargs)

def page_children(request, *args, **kwargs):
    return page_detail(request, template_name='wiki/page_children.html', *args, **kwargs)

def page_history(request, slug, **kwargs):
    try:
        page = Page.objects.filter(slug=slug).get()
    except ObjectDoesNotExist:
        raise Http404, "No page found matching the query"
    
    kwargs['queryset'] = Revision.objects.filter(page=page)
    kwargs['extra_context'] = {'page': page}
    kwargs['template_name'] = 'wiki/page_history.html'
    kwargs['template_object_name'] = 'revision'
    kwargs['paginate_by'] = settings.WIKI_HISTORY_PAGINATE_BY
    
    return object_list(request, **kwargs)

def revision_detail(request, slug, pk):
    try:
        revision = Revision.objects.filter(page__slug=slug, pk=pk).get()
    except ObjectDoesNotExist:
        raise Http404, "No revision found matching the query"
    
    return render_to_response('wiki/revision_detail.html', {'revision': revision,}, RequestContext(request))

def revision_revert(request, slug, pk):
    try:
        revision = Revision.objects.filter(page__slug=slug, pk=pk).get()
    except ObjectDoesNotExist:
        raise Http404, "No revision found matching the query"
    
    if not revision.page.user_can_edit(request.user):
        if request.user.is_anonymous():
            return HttpResponseRedirect('%s?%s=%s' % (settings.LOGIN_URL, REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
        else:
            return render_to_response('wiki/permission_denied.html', context_instance=RequestContext(request))
    
    r = Revision(text=revision.text, page=revision.page)
    r.comment = _(u'Reverted to revision %(revision)s by %(author)s') % {'revision':revision.pk, 'author':revision.author or revision.author_ip}
    
    if request.user.is_anonymous():
        r.author_ip = request.META['REMOTE_ADDR']
    else:
        r.author = request.user
    
    r.save()
    
    return HttpResponseRedirect(r.get_absolute_url())

def revision_diff(request, slug):
    if request.GET.get('a').isdigit() and request.GET.get('b').isdigit():
        a = int(request.GET.get('a'))
        b = int(request.GET.get('b'))
    else:
        return HttpResponseBadRequest(u'You must select two revisions.')
    
    try:
        page = Page.objects.filter(slug=slug).get()
        revisionA = Revision.objects.filter(page=page, pk=a).get()
        revisionB = Revision.objects.filter(page=page, pk=b).get()
    except ObjectDoesNotExist:
        raise Http404, "No revision found matching the query"
    
    if revisionA.content != revisionB.content:
        d = difflib.unified_diff(
            revisionA.content.splitlines(),
            revisionB.content.splitlines(),
            'Revision %s' % revisionA.pk,
            'Revision %s' % revisionB.pk,
            lineterm=''
        )
    
        difftext = '\n'.join(d)
        difftext = pygments_diff(difftext)
    else:
        difftext = _('No changes were made between this two revisions.')
    
    template_context = {
        'page': page,
        'revisionA': revisionA,
        'revisionB': revisionB,
        'difftext': difftext,
    }
    
    return render_to_response('wiki/revision_diff.html', template_context, RequestContext(request))
