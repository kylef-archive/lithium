from django.contrib import admin
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound

from lithium.forum.models import Forum, Thread, Post

class ForumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ('title_link', 'expand', 'add_child', 'position_link')
    
    def queryset(self, request):
        qs = super(ForumAdmin, self).queryset(request)
        
        if not request.GET.get('parent'):
            return qs.filter(parent=None)
        
        return qs
    
    def get_urls(self):
        urls = super(ForumAdmin, self).get_urls()
        
        new_urls = patterns('',
            url(r'^move/', self.admin_site.admin_view(self.move), name='admin.forum_move'),
        )
    
        return new_urls + urls
    
    def move(self, request):
        """
        Move a forum up or down in position.
        """
        pk = request.GET.get('f', None)
        direction = request.GET.get('d', None)
        
        if pk:
            forum = get_object_or_404(Forum, pk=pk)
            print forum.move(direction)
            
            if forum.parent:
                return HttpResponseRedirect('/admin/forum/forum/?parent=%d' % forum.parent.pk)
            return HttpResponseRedirect('/admin/forum/forum/')
        
        return HttpResponseNotFound()
    
    def title_link(self, obj):
        """
        With the normal title link, no parent is supplied.
        When there is no parent, the queryset is limited.
        """
        return '<a href="%d/?parent=0">%s</a>' % (obj.id, obj.title)
    title_link.allow_tags = True
    title_link.short_description = 'Title'
    
    def expand(self, obj):
        if not obj.children.all():
            return ''
        return '<a href="?parent=%d">+</a>' % (obj.id)
    expand.allow_tags = True
    expand.short_description = 'Expand'
    
    def add_child(self, obj):
        return '<a href="add/?parent=%d">+</a>' % obj.id
    add_child.allow_tags = True
    add_child.short_description = 'Add sub-forum'
    
    def position_link(self, obj):
        url = reverse('admin.forum_move')
        up = url + '?f=%s&d=%s' % (obj.pk, 'up')
        down = url + '?f=%s&d=%s' % (obj.pk, 'down')
        
        return '<a href="%s" class="up">+</a> <a href="%s" class="down">-</a>' % (up, down)
    position_link.admin_order_field = 'position'
    position_link.allow_tags = True
    position_link.short_description = 'Move'

class PostAdmin(admin.StackedInline):
    model = Post
    
    def queryset(self, request):
        return super(PostAdmin, self).queryset(request).order_by('pub_date')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Select the user who is currently logged in.
        """
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ThreadAdmin(admin.ModelAdmin):
    inlines = [PostAdmin,]
    prepopulated_fields = {'slug': ['title']}
    list_display = ('title', 'post_count',)
    
    def post_count(self, obj):
        return u'%s' % obj.post_count

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
