# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
# Create your views here.

def Article_views(request):
    return render(request,'Article.html')

def ArticleThumbUp_views(request):
    # 点赞数查询
    # 点赞数: sum
    # list = ArticleThumbUp.objects.filter(likeUser.personName = '已登录用户').sum()
    # sum = 0
    # for obj in list:
    #     sum += 1

    if request.method == 'GET':
        articleThumbUplist = ArticleThumbUp.objects.all()
        return render(request,'ArticleThumbUp.html',locals())
    else:
       # 
       # 
       # 
        return HttpResponse('ArticleThumbUp_views')

def ArticleRecommend_views(request):
    if request.method == 'GET':
        articleRecommendlist = ArticleRecommend.objects.all()
        return render(request,'ArticleRecommend.html',locals())
    else:
        return HttpResponse('ArticleRecommend_views')

def ArticleCollection_views(request):
    if request.method == 'GET':
        articleCollectionlist = ArticleCollection.objects.all()
        return render(request,'ArticleCollection.html',locals())
    else:
        
        return HttpResponse('ArticleCollection_views')
    



def DynamicThumbUp_views(request):
    articleThumbUplist = ArticleThumbUp.objects.all()
    return render(request,'DynamicThumbUp.html',locals())


def IdeaThumbUp_views(request):
    return HttpResponse('IdeaThumbUp_views')



def IdeaRecommend_views(request):
    return HttpResponse('IdeaRecommend_views')
    
def IdeaCollection_views(request):
    return HttpResponse('IdeaCollection_views')

def wangeditor_views(request):
    if request.method == 'GET':
        return render(request,'wangeditor.html')
    else:
        title = request.POST.get('title2')
        return HttpResponse(title)




    # IdeaThumbUp_views),
    # ArticleRecommend_views),
    # IdeaRecommend_views),
    # IdeaCollection_views),
    # ArticleCollection_views),