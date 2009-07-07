from django.views.generic.list_detail import *
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.http import urlquote
from django.core.paginator import Paginator, InvalidPage

from lithium.conf import settings
from lithium.forum.models import Forum, Thread, Post
from lithium.forum.forms import ThreadCreateForm, ThreadReplyForm
from lithium.forum.utils import user_permission_level

def forum_index(request):
    user_permission = user_permission_level(request.user)
    return object_list(request, queryset=Forum.objects.filter(read__lte=user_permission))

def forum_detail(request, forum):
    user_permission = user_permission_level(request.user)
    
    try:
        forum = Forum.objects.filter(slug=forum, read__lte=user_permission).get()
    except ObjectDoesNotExist:
        raise Http404
    
    return object_list(request,
        queryset=Thread.objects.filter(forum=forum),
        extra_context={'forum': forum, 'can_create': forum.write < user_permission},
        paginate_by=settings.FORUM_THREAD_PAGINATE_BY,
        template_object_name='thread'
    )

def thread_create(request, forum):
    user_permission = user_permission_level(request.user)
    
    try:
        forum = Forum.objects.filter(slug=forum, write__lte=user_permission).get()
    except ObjectDoesNotExist:
        raise Http404
    
    if forum.is_category:
        raise Http404
    
    if request.method == 'POST':
        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            if request.user and request.user.is_authenticated():
                form.post.author = request.user
            
            form.thread.forum = forum
            form.save()
            
            return HttpResponseRedirect(form.thread.get_absolute_url())
    else:
        form = ThreadCreateForm()
    
    template_context = {
        'forum': forum,
        'form': form,
    }
    
    return render_to_response('forum/thread_create.html', template_context, RequestContext(request))

def thread_detail(request, forum, slug, page=None, display_posts=True, paginate_by=settings.FORUM_POST_PAGINATE_BY, template_name='forum/thread_detail.html'):
    user_permission = user_permission_level(request.user)
    
    try:
        forum = Forum.objects.filter(slug=forum, read__lte=user_permission).get()
        thread = Thread.objects.filter(forum=forum, slug=slug).get()
    except ObjectDoesNotExist:
        raise Http404
    
    template_context = dict(thread=thread)
    
    if display_posts:
        queryset = Post.objects.filter(thread=thread)
        paginator = Paginator(queryset, paginate_by)
        
        if page == None:
            page = request.GET.get('page', 1)
        
        try:
            page = int(page)
        except ValueError:
            raise Http404
        
        page_obj = paginator.page(page)
        
        template_context['posts'] = page_obj.object_list
        template_context['paginator'] = paginator
        template_context['page_obj'] = page_obj
        template_context['is_paginated'] = page_obj.has_other_pages()
    else:
        template_context['posts'] = None
        template_context['paginator'] = None
        template_context['page_obj'] = None
        template_context['is_paginated'] = False
    
    if thread.is_locked:
        form = None
    elif forum.write > user_permission:
        form = None
    else:
        if request.method == 'POST':
            form = ThreadReplyForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                
                if request.user and request.user.is_authenticated():
                    instance.author = request.user
                
                instance.thread = thread
                instance.save()
                
                return HttpResponseRedirect(form.instance.get_absolute_url())
        else:
            form = ThreadReplyForm()
    
    template_context['form'] = form
    template_context['can_reply'] = form != None
    
    return render_to_response(template_name, template_context, RequestContext(request))
