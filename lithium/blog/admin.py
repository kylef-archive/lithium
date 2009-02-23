from django.contrib import admin
from django.contrib.sites.models import Site

from lithium.blog.models import Category, Post

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

class PostAdmin(admin.ModelAdmin):
    exclude = ('author',)
    fieldsets = (
        (None, {'fields': ('title', 'content', 'category', 'is_public', 'sites')}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('enable_comments', 'pub_date', 'slug')})
    )
    list_display = ('title', 'pub_date', 'is_public')
    list_filter = ('enable_comments', 'is_public', 'pub_date', 'author')
    search_fields = ('title', 'content')
    ordering = ('-pub_date',)
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'pub_date'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(author=request.user)
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PostAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)