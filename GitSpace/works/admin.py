# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
# class ArticleThumbUpContact(admin.ModelAdmin):
#     list_display=('LikeUser','LikeArticle')
#     search_fields=['LikeUser']
label = models.BinaryField(max_length=64)
class ArticleContact(admin.ModelAdmin):
    list_display=('LikeUser','LikeArticle')
    search_fields=['LikeUser']
admin.site.register(Person)
admin.site.register(Article)
admin.site.register(Dynamic)
admin.site.register(Idea)
# admin.site.register(ArticleThumbUp,ArticleThumbUpContact)
admin.site.register(ArticleThumbUp)
admin.site.register(DynamicThumbUp)
admin.site.register(IdeaThumbUp)
admin.site.register(ArticleRecommend)
admin.site.register(IdeaRecommend)
admin.site.register(IdeaCollection)
admin.site.register(ArticleCollection)