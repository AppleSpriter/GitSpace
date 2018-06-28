# -*- coding:utf-8 -*-
from django.conf.urls import url
from .views import *

#文章点赞收藏推荐三大功能
urlpatterns = [
    url(r'^Article',Article_views),
]


urlpatterns += [
    url(r'^01_ArticleThumbUp',ArticleThumbUp_views),
    url(r'^02_DynamicThumbUp',DynamicThumbUp_views),
    url(r'^03_IdeaThumbUp',IdeaThumbUp_views),
    url(r'^04_ArticleRecommend',ArticleRecommend_views),
    url(r'^05_IdeaRecommend',IdeaRecommend_views),
    url(r'^06_IdeaCollection',IdeaCollection_views),
    url(r'^07_ArticleCollection',ArticleCollection_views),
]

# 富文本编辑器wangeditor 
# 只是测试用
urlpatterns += [
    url(r'^wangeditor',wangeditor_views),
]