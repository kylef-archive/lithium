from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from lithium.blog.models import Category, Post

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'category', 'is_public',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'pub_date', 'enable_comments', 'author', 'sites',)
        })
    )
    list_display = ('title', 'pub_date', 'is_public',)
    list_filter = ('enable_comments', 'is_public', 'pub_date', 'author')
    search_fields = ('title', 'content')
    ordering = ('-pub_date',)
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'pub_date'
    
    def save_model(self, request, obj, form, change):
        """
        Only superuser's may save a post under another user.
        """
        if not request.user.is_superuser:
            obj.author = request.user
        obj.save()
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Select the current site in the list of sites a post is viewable from.
        """
        if db_field.name == 'sites':
            kwargs['initial'] = [Site.objects.get_current()]
            return db_field.formfield(**kwargs)
        return super(PostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Select the user who is currently logged in.
        """
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def queryset(self, request):
        """
        If the user is a superuser, then display all posts. Otherwise only show their own posts.
        """
        if request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(author=request.user)
    
    def has_change_permission(self, request, obj=None):
        """
        Check that the user may edit this post.
        """
        has_class_permission = super(PostAdmin, self).has_change_permission(request, obj)
        
        if not has_class_permission:
            return False
        
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        
        return True

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
