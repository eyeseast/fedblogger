from django.contrib import admin
from fedblogger.models import *

class BranchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class AgencyAdmin(admin.ModelAdmin):
    prepulated_fields = {'slug': ['name']}

class AuthorTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class BlogFeedAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

    list_display = ('name', 'agency', 'author_type', 'status')
    list_filter = ('author_type', 'agency', 'status')

class BlogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_filter = ('blog',)
    list_display = ('title', 'blog', 'pub_date')

admin.site.register(Branch, BranchAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(AuthorType, AuthorTypeAdmin)
admin.site.register(BlogFeed, BlogFeedAdmin)
admin.site.register(BlogEntry, BlogEntryAdmin)
