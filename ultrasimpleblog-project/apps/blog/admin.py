from django.contrib import admin

from apps.blog.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'published', 'created', 'modified']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ['published']
    list_filter = ['published']

admin.site.register(Article, ArticleAdmin)
