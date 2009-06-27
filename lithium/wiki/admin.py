from django.contrib import admin
from lithium.wiki.models import Page, Revision, Text

class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ['title']}

class RevisionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'comment',)
    list_filter = ('pub_date',)
    ordering = ('-pub_date',)
    date_hierarchy = 'pub_date'

admin.site.register(Page, PageAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(Text)
