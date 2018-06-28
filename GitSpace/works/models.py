# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ArticleThumbUp(models.Model) :
    likeUser=models.ForeignKey(Person)
    likeArticle=models.ForeignKey(Article)
    def __str__(self):
        return self.likeUser.personName

    class Meta:
        verbose_name_plural='文章点赞表'

class DynamicThumbUp(models.Model) :
    likeUser=models.ForeignKey(Person)
    likeDynamic=models.ForeignKey(Dynamic)
    
    def __str__(self):
        return self.likeUser.personName

    class Meta:
        verbose_name_plural='动态点赞表'

class IdeaThumbUp(models.Model) :
    likeUser=models.ForeignKey(Person)
    likeIdea=models.ForeignKey(Idea)
   
    def __str__(self):
        return self.likeUser.personName

    class Meta:
        verbose_name_plural='想法点赞表'

class ArticleRecommend(models.Model) :
    recommendtUser=models.ForeignKey(Person)
    recommendArticle=models.ForeignKey(Article)
    def __str__(self):
        return self.recommendtUser.personName
    class Meta:
        verbose_name_plural='文章推荐表'

class IdeaRecommend(models.Model) :
    recommendrecommendUser=models.ForeignKey(Person)
    recommendIdea=models.ForeignKey(Idea)

    def __str__(self):
        return self.recommendrecommendUser.personName

    class Meta:
        verbose_name_plural='想法推荐表'

class IdeaCollection(models.Model) :
    collectionUser=models.ForeignKey(Person)
    collectionIdea=models.ForeignKey(Idea)
    
    def __str__(self):
        return self.collectionUser.personName
        
    class Meta:
        verbose_name_plural='想法收藏表'

class ArticleCollection(models.Model) :
    collectionUser=models.ForeignKey(Person)
    collectionArticle=models.ForeignKey(Article)
    def __str__(self):
        return self.collectionUser.personName
    class Meta:
        verbose_name_plural='文章收藏表'
        
