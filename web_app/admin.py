from django.contrib import admin
from .models import Article, Commentary
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'theme', 'text', 'author', 'date')
    list_display_links = ('id', 'name', 'theme')
    search_fields = ('id', 'name', 'theme')
    list_filter = ('theme',)


class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'date')
    list_display_links = ('id', 'text')
    search_fields = ('text', 'author')
    list_filter = ('article',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Commentary, CommentaryAdmin)
