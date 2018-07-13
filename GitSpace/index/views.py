from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.contrib import messages
from collections import Counter
import os
# 用来和js传递数值
import json
# Create your views here.

def publishDynamicViews(request): 
    dynamicContent = request.POST['dynamicContent']
    person = Person.objects.get(personID=request.session.get('personID'))
    Dynamic.objects.create(sender=person,content=dynamicContent,createDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return HttpResponseRedirect('/indexAfterLogin/')

def publishIdeaViews(request):
    ideaContent = request.POST['ideaContent']
    value = request.POST.getlist('label')
    print(value)
    label = 0
    if  value == None:
        label = 0  
    for v in value:
        label |= 1<<int(v)
    person = Person.objects.get(personID=request.session.get('personID'))
    Idea.objects.create(sender=person,content=ideaContent,createDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),label=label)    
    return HttpResponseRedirect('/indexAfterLogin/')

def indexLikeViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        followList  = PersonFollow.objects.filter(follower =person)
        dynamicList = []
        for f in followList:
            for d in Dynamic.objects.filter(sender=f.followee):
                dynamicList.append(d)
        # print(dynamicList)
        dynamicList.sort(key =lambda Dynamic:Dynamic.createDate,reverse = True)

        ideaList = []
        for f in followList:
            for d in Idea.objects.filter(sender=f.followee):
                ideaList.append(d)
        # print(dynamicList)
        ideaList.sort(key =lambda Idea:Idea.createDate,reverse = True)

        articleList = []
        for f in followList:
            for d in Article.objects.filter(sender=f.followee):
                articleList.append(d)
        # print(dynamicList)
        articleList.sort(key =lambda Article:Article.createDate,reverse = True)
        return render(request,'indexLike.html',locals())
    else:
        return HttpResponseRedirect('/indeHot/')

def indexHotViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
    # 推送,获取比较新的数条数据,或者随机获取一定数据
    # pushlist所得到的是个字典的value,存的一个新列表
    pushlist = []
    for one in IdeaThumbUp.objects.values('likeIdea_id').all():
        pushlist.append(one['likeIdea_id'])
    # 测试pushlist
    # print(pushlist)
    #　统计热度最高的十条想法
    ideaList = []
    for i in Counter(pushlist).most_common(10):
         ideaList.append(Idea.objects.get(ideaID = i[0]))
    # print(ideaList)

    pushlist = []
    for one in ArticleThumbUp.objects.values('likeArticle_id').all():
        pushlist.append(one['likeArticle_id'])
    # 测试pushlist
    # print(pushlist)
    #　统计热度最高的十条文章
    articleList = []
    for i in Counter(pushlist).most_common(10):
         articleList.append(Article.objects.get(articleID = i[0]))
    return render(request,'indexHot.html',locals())


def indexRecommendViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
    return render(request,'indexRecommend.html',locals())

def indexAfterLoginViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        dynamicList = Dynamic.objects.all()[::-1]
        ideaList = Idea.objects.all()[::-1]
        articleList = Article.objects.all()[::-1]
        return render(request,'indexAfterLogin.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

# 登录
def loginViews(request):
    if request.method == 'GET':
        return render(request,'login.html')

    else:
        personName = request.POST.get('uname')
        personPassword = request.POST.get('upwd') 

        vuser = Person.objects.filter(personName=personName)

        if vuser:
            if check_password(personPassword, vuser[0].personPassword):
                request.session['personID']=vuser[0].personID
                # print(request.session.get('personID'))
                if request.POST.get('isSave'):
                    request.COOKIES['uname'] = personName
                    request.COOKIES['upwd'] = personPassword
                return HttpResponseRedirect('/indexAfterLogin')
        messages.add_message(request,messages.ERROR,'用户名或密码不正确')
        return HttpResponseRedirect('/login')

# 注册
def registerViews(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        personName = request.POST.get('uname')
        personPassword = request.POST.get('upwd')
        checkPassword = request.POST.get('upwd2')
        finalPassword = make_password(personPassword)
        personMobile = request.POST.get('umobile')
        personEmail = request.POST.get('uemail')
        
        vuser = Person.objects.filter(personName=personName)
        vphone = Person.objects.filter(personMobile=personMobile)
        if vuser:
            messages.add_message(request,messages.ERROR,'名称重复')
            return HttpResponseRedirect('/register/')
        if vphone:
            messages.add_message(request,messages.ERROR,'手机号重复')
            return HttpResponseRedirect('/register/')
        if personPassword == "":
            messages.add_message(request,messages.ERROR,'Valid PassPword!')
            return HttpResponseRedirect('/register/')
        if len(personPassword) < 6:
            messages.add_message(request,messages.ERROR,'Password is less than 6 characters!')
            return HttpResponseRedirect('/register/')
        else:
            if personPassword != checkPassword:
                messages.add_message(request,messages.ERROR,'Wrong Check Password!')
                return HttpResponseRedirect('/register/')
            else:
                newuser = Person.objects.create(personName=personName,personPassword=finalPassword,personMobile=personMobile,personEmail=personEmail,isActive=True,personInfo='我在GitSpace。',personImage='/static/imgs/userhead/default.png')
                request.session['personID'] = newuser.personID
                return HttpResponseRedirect('/indexAfterLogin')

# 
def protocolViews(request):
    return render(request,'protocol.html')


# 检查是否在关注列表
def checkFollow(followeeID,followerID):
    # 获取关注人
    follower = Person.objects.get(personID=followerID)
    # 获取被关注人
    followee = Person.objects.get(personID=followeeID)
    # 检查该关注是否在数据库中
    check = PersonFollow.objects.filter(follower=follower,followee=followee)
    # 在数据库中返回True
    if check:
        return True
    else:
        return False

# 获最新前8条文字
def newArticle():
    articleNew = list(Article.objects.all())
    articleNew.sort(key=lambda Article:Article.createDate,reverse = True)
    return articleNew[0:8]

# 获取最热3条想法
def hotIdea():
    pushlist = []
    for one in IdeaThumbUp.objects.values('likeIdea_id').all():
        pushlist.append(one['likeIdea_id'])
        #　统计热度最高的十条想法
    ideaList = []
    for i in Counter(pushlist).most_common(3):
        ideaList.append(Idea.objects.get(ideaID = i[0]))
    return ideaList

# 获取最热3条文字
def hotArticle():
    pushlist = []
    for one in ArticleThumbUp.objects.values('likeArticle_id').all():
        pushlist.append(one['likeArticle_id'])
        #　统计热度最高的十条想法
    articleList = []
    for i in Counter(pushlist).most_common(3):
        articleList.append(Article.objects.get(articleID = i[0]))
    return articleList

# 查询自己的动态
def indexPersonTrendsViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        dynamicList = Dynamic.objects.filter(sender=person)[::-1]
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        return render(request,'person/indexPersonTrends.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

# 其他人的动态页面
def indexOtherPersonTrendsViews(request,ID):
    # 获取当前session的ID
    currentpersonID = request.session.get('personID')
    # 判断点击的是否为自己的页面
    if int(ID) == int(currentpersonID):
        return HttpResponseRedirect('/person/personTrends')
    # 跳转到其他人界面
    else:
        person = Person.objects.get(personID=ID)        
        dynamicList = Dynamic.objects.filter(sender=person)[::-1]
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        followMes = json.dumps(1)
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonTrends.html',locals())
        else:
            followMes = json.dumps(0)
            return render(request,'otherperson/indexOtherPersonTrends.html',locals())

#　查询自己的想法
def indexPersonIdeaViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        ideaList = Idea.objects.filter(sender=person)[::-1]
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        return render(request,'person/indexPersonIdea.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

# 其他人的想法页面
def indexOtherPersonIdeaViews(request,ID):
    # 获取当前session的ID
    currentpersonID = request.session.get('personID')
    # 判断点击的是否为自己的页面
    if int(ID) == int(currentpersonID):
        return HttpResponseRedirect('/person/personIdea')
    else:
        person = Person.objects.get(personID=ID)
        ideaList = Idea.objects.filter(sender=person)[::-1]
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        followMes = json.dumps(1)
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonIdea.html',locals())
        else:
            followMes = json.dumps(0)
            return render(request,'otherperson/indexOtherPersonIdea.html',locals())

# 自己的想法收藏显示
def indexPersonCollectionIdeaViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        ideaCollectionList = IdeaCollection.objects.filter(collectionUser=person)
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        return render(request,'person/indexPersonCollectionIdea.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

# 自己的文章收藏显示
def indexPersonCollectionArtiViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        artiCollectionList = ArticleCollection.objects.filter(collectionUser=person)
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        return render(request,'person/indexPersonCollectionArticle.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

# 其他人的想法收藏显示
def indexOtherPersonCollectionIdeaViews(request,ID):
    # 获取当前session的ID
    currentpersonID = request.session.get('personID')
    # 判断点击的是否为自己的页面
    if int(ID) == int(currentpersonID):
        return HttpResponseRedirect('/person/personCollectionIdea')
    else:
        person = Person.objects.get(personID=ID)
        ideaCollectionList = IdeaCollection.objects.filter(collectionUser=person)
        check = checkFollow(ID,currentpersonID)
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        followMes = json.dumps(1)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonCollectionIdea.html',locals())
        else:
            followMes = json.dumps(0)
            return render(request,'otherperson/indexOtherPersonCollectionIdea.html',locals())

# 其他人的文章收藏显示
def indexOtherPersonCollectionArtiViews(request,ID):
    # 获取当前session的ID
    currentpersonID = request.session.get('personID')
    # 判断点击的是否为自己的页面
    if int(ID) == int(currentpersonID):
        return HttpResponseRedirect('/person/personCollectionArti')
    else:
        person = Person.objects.get(personID=ID)
        artiCollectionList = ArticleCollection.objects.filter(collectionUser=person)
        check = checkFollow(ID,currentpersonID)
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        followMes = json.dumps(1)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonCollectionArti.html',locals())
        else:
            followMes = json.dumps(0)
            return render(request,'otherperson/indexOtherPersonCollectionArti.html',locals())

# 删除想法收藏
def cancelCollectionIdeaViews(request,ideaID):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        idea = Idea.objects.get(ideaID=ideaID)
        IdeaCollection.objects.get(collectionUser=person,collectionIdea=idea).delete()
        return HttpResponseRedirect('/person/personCollectionIdea/')
    else:
        return HttpResponseRedirect('/indexHot')

# 删除文章收藏
def cancelCollectionArtiViews(request,articleID):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        article = Article.objects.get(articleID=articleID)
        ArticleCollection.objects.get(collectionUser=person,collectionArticle=article).delete()
        return HttpResponseRedirect('/person/personCollectionArti/')
    else:
        return HttpResponseRedirect('/indexHot')


# 自己的文章显示
def indexPersonArticleViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        articleList = Article.objects.filter(sender=person)[::-1]
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        return render(request,'person/indexPersonArticle.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

# 其他人的文章显示
def indexOtherPersonArticleViews(request,ID):
    # 获取当前session的ID
    currentpersonID = request.session.get('personID')
    # 判断点击的是否为自己的页面
    if int(ID) == int(currentpersonID):
        return HttpResponseRedirect('/person/personCollectionArti')
    else:
        person = Person.objects.get(personID=ID)
        articleList = Article.objects.filter(sender=person)[::-1]
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        followMes = json.dumps(1)
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonArticle.html',locals())
        else:
            followMes = json.dumps(0)
            return render(request,'otherperson/indexOtherPersonArticle.html',locals())


# 自己的关注列表
def indexPersonFollowViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        presonFollowList = PersonFollow.objects.filter(follower=person)
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        return render(request,'person/indexPersonFollow.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

#　其他人的关注列表
def indexOtherPersonFollowViews(request,ID):
    # 获取当前session的ID
    currentpersonID = request.session.get('personID')
    # 判断点击的是否为自己的页面
    if int(ID) == int(currentpersonID):
        return HttpResponseRedirect('/person/personFollow')
    else:
        person = Person.objects.get(personID=ID)
        presonFollowList = PersonFollow.objects.filter(follower=person)
        articlenew = newArticle()
        hotidea = hotIdea()
        hotarticle = hotArticle()
        followMes = json.dumps(1)
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonFollow.html',locals())
        else:
            followMes = json.dumps(0)
            return render(request,'otherperson/indexOtherPersonFollow.html',locals())


def logOutViews(request):
    del request.session['personID']
    return HttpResponseRedirect('/indexHot')

#　修改个人信息
def editPersonViews(request):
    if 'personID' in request.session:
    # print(request.session.get('personID'))
        person = Person.objects.get(personID=request.session.get('personID'))
        if request.method == 'GET':
            return render(request,'person/editPerson.html',locals())
        else:
            person.personSex = request.POST.get('userSex')
            person.personMobile = request.POST.get('userMobile')
            person.personEmail = request.POST.get('userEmail')
            if request.FILES.get("userImage",None):
                # print('23333')
                obj = request.FILES['userImage']
                f = open(os.getcwd()+'/index/static/imgs/userhead/'+ str(person.personID) + "-" +obj.name,'wb+')
                for chunk in obj.chunks():
                    f.write(chunk)
                f.close()
                person.personImage = '/static/imgs/userhead/'+ str(person.personID) + "-" +obj.name
            person.personInfo = request.POST.get('userInfo')
            person.save()
            return HttpResponseRedirect('/person/indexPerson/')
    else:
        return HttpResponseRedirect('/indexHot')

# 修改个人密码
def changepassword(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        if request.method == 'GET':
            return render(request,'person/editPerson.html',locals())
        else:
            origin = request.POST.get('originpassword')
            newpass = request.POST.get('newpassword')
            if check_password(origin,person.personPassword):
                if newpass == "":
                    return render(request,'person/editPerson.html',{'person':person,'mes': '密码为空!'})
                if len(newpass) < 6:
                    return render(request,'person/editPerson.html',{'person':person,'mes': '密码小于６位!'})
                else:
                    finalPassword = make_password(newpass)
                    Person.objects.filter(personName=person.personName).update(personPassword=finalPassword)
                    return render(request,'person/editPerson.html',{'person':person,'mes': '密码修改成功'})
            else:
                return render(request,'person/editPerson.html',{'person':person,'mes': '密码匹配错误!'})


def indexPerson(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        return render(request,'person/indexPerson.html',{'person':person})
    else:
        return render(request,'person/indexPerson.html')

def likePerson(request):
    return render(request,'person/likePerson.html')

# 加入关注列表
def addFollowViews(request, followeeID):
    # 获取关注人
    follower = Person.objects.get(personID = request.session.get('personID'))
    # 获取被关注人
    followee = Person.objects.get(personID = followeeID)
    PersonFollow.objects.create(follower=follower,followee=followee)
    return HttpResponseRedirect('/person/personFollow/')

# 取消关注
def cancelFollowViews(request,followeeID):
    follower = Person.objects.get(personID=request.session.get('personID'))
    followee = Person.objects.get(personID=followeeID)
    PersonFollow.objects.get(follower=follower,followee=followee).delete()
    return HttpResponseRedirect('/person/personFollow/')

def ideaCollectionViews(request,ideaID):
    if 'personID' in request.session:
        user = Person.objects.get(personID=request.session.get('personID'))
        idea = Idea.objects.get(ideaID = ideaID)
        # print('23333')
        if user.personID != idea.sender.personID:
            IdeaCollection.objects.create(collectionUser=user,collectionIdea=idea)
        return HttpResponseRedirect('/indexAfterLogin')
    else:
        return HttpResponseRedirect('/indexAfterLogin')

def articleCollectionViews(request,articleID):
    if 'personID' in request.session:
        user = Person.objects.get(personID=request.session.get('personID'))
        article = Article.objects.get(articleID = articleID)
        if user.personID != article.sender.personID:
            IdeaCollection.objects.create(collectionUser=user,collectionArticle=article)
        return render(request,'/indexAfterLogin')
    else:
        return HttpResponseRedirect('/login/')       


def discussViews(request,ideaID):
    if 'personID' not in request.session:
        return HttpResponseRedirect('/indexHot')
    if request.method == 'GET':
        idea = Idea.objects.get(ideaID=ideaID)
        person = Person.objects.get(personID=request.session.get('personID'))
        ideaMessageList = IdeaMessage.objects.filter(idea = Idea.objects.get(ideaID=ideaID))
        ideaMemberList = IdeaMember.objects.filter(idea = idea)
        print(ideaMemberList)
        return render(request,'discuss.html',locals())
    else:
        person = Person.objects.get(personID=request.session.get('personID'))
        idea = Idea.objects.get(ideaID=ideaID)
        content = request.POST.get('message')
        IdeaMessage.objects.create(sender=person,idea=idea,content = content,publishDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if not IdeaMember.objects.filter(idea = idea,member=person):
            # print(person)
            IdeaMember.objects.create(idea=idea,member = person)
        # print(ideaMemberList)
        ideaMemberList = IdeaMember.objects.filter(idea = idea)
        ideaMessageList = IdeaMessage.objects.filter(idea = idea)
        return render(request,'discuss.html',locals())

def dropIdeaViews(request,ideaID):
    if 'personID' in request.session:
        idea = Idea.objects.get(ideaID = ideaID)
        IdeaMessage.objects.filter(idea = idea).delete()
        IdeaMember.objects.filter(idea = idea).delete()
        idea.delete()
        return HttpResponseRedirect('/indexAfterLogin')
    else:
        return HttpResponseRedirect('/indexHot/')

def deleteIdeaMemberViews(request,ideaID):
    if 'personID' in request.session:
        deleteIdeaMember = request.POST.getlist('deleteIdeaMember')
        idea = Idea.objects.get(ideaID=ideaID)
        for p in deleteIdeaMember:
            IdeaMember.objects.filter(idea = idea,member=Person.objects.get(personID=int(p))).delete()
        # print(type(deleteIdeaMember[0]))
        return HttpResponseRedirect('/discuss/'+str(ideaID))
    else:
        return HttpResponseRedirect('/indexHot/');



def pushDynamicViews(request):
    # 推送,获取比较新的数条数据,或者随机获取一定数据
    # pushlist 获取的是一个字典的列表{"lieDynamic_id",3}
    pushlist = DynamicThumbUp.objects.values("likeDynamic_id").all()
    pushlist2 = []
    # pushlist2 所得到的是pushlist每个字典的value,存的一个新列表
    for one in pushlist:
        pushlist2.append(one['likeDynamic_id'])
    # 测试,pushlist2中id为3的动态总数
    cc = pushlist2.count(3)
    reallist = pushlist.count()
    return HttpResponse(cc)



# 任荣福－－文章编辑
def get_article_list(request, person_id):
    person=Person.objects.get(personID=person_id)
    articleList=person.Article_set().all
    return render_to_response('article-list.html', {'articleList': articleList})

def get_article(request, article_id):
    try:
        article=Article.objects.get(articleID=article_id)
    except Article.DoesNotExist:
        return render(request, 'indexAfterLogin.html', locals())
    comments = ArticleComment.objects.filter(commentArticle=article)
    person = Person.objects.get(personID = request.session.get('personID'))
    return render(request, 'show-article.html', locals())

def post_article(request):
    if request.method == 'GET':
       return render(request,'post-article.html')

#编辑文章
def edit_article(request,article_id):
    if request.method == 'GET':
        try:
            article=Article.objects.get(articleID=article_id)
        except Article.DoesNotExist:
            return render(request,'indexAfterLogin.html',locals())

        return render(request,'edit-article.html',locals())

# #二次编辑，待测试
# def edit_article(request,article_id):
#     if request.method == 'GET' :
#         try:
#             article=Article.objects.get(articleUD=article_id)
#         except Article.DoesNotExist:
#             return render(request,'indexAfterLogin.html',locals())
#     else request.is_ajax():
#         person = Person.objects.get(personID=request.session.get('personID'))
#         date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         content=request.POST.get('cont')
#         title=request.POST.get('titl')
#         label = request.POST.get('labl')
#         description=request.POST.get('des')
#         isPub=request.POST.get('isPub') 
#         Article.objects.create(title=title,content=content,description=description,label=label,sender=person,createDate=date,\
#           isPub=isPub)

#         if isPub == 0 :
#             print("responsed!")
#             ctx={
#                 'artl-id':0,
#                 'result':1
#             }
#             return HttpResponse(json.dumps(ctx))
#         else :
#             ctx={
#                 'artl-id':1,
#                 'result': 1
#             }
#             return HttpResponse(json.dumps(ctx))


def save_article(request): 
    if request.is_ajax():
        print("1")
        person = Person.objects.get(personID=request.session.get('personID'))
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content=request.POST.get('cont')
        title=request.POST.get('titl')
        label = request.POST.get('labl')
        description=request.POST.get('des')
        isPub=request.POST.get('isPub') 
        print(description)
        Article.objects.create(title=title,content=content,description=description,label=label,sender=person,createDate=date,\
          isPub=isPub)

        if isPub == 0 :
            print("responsed!")
            ctx={
                'artl-id':0,
                'result':1
            }
            return HttpResponse(json.dumps(ctx))
        else :
            ctx={
                'artl-id':1,
                'result': 1
            }
            return HttpResponse(json.dumps(ctx))
        print("responsed!")


# ---------------------------------------------------------------------------------
def indexComment_views(request):
    switch = request.POST.get('switch')

    if switch=='articleComment':
        # 文章评论
        articleID = request.POST.get('articleID')
        article = Article.objects.get(articleID=articleID)
        articleTitle = article.title;
        person = Person.objects.get(personID=request.session.get('personID')) 
        upcomment = request.POST.get('ucomment')
        ucommentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ArticleComment.objects.create(
            commentContent = upcomment,
            commentUser = person,
            commentArticle = article,
            commentTime = ucommentTime
            )

        result = 1
        articleCommentList = ArticleComment.objects.filter(commentArticle=article)[::-1]
        num = len(articleCommentList)
        
        if num>0:
            articleComment = []
            for tem in range(num):
                dic = {}
                dic['commentUser'] = articleCommentList[tem].commentUser.personName
                dic['commentContent'] = articleCommentList[tem].commentContent 
                dic['commentTime'] = articleCommentList[tem].commentTime.strftime('%Y-%m-%d %H:%M:%S')
                articleComment.append(dic)
        else:
            articleComment = []
        return HttpResponse(json.dumps({
                "result": result,
                "articleComment":articleComment,
                "articleTitle":articleTitle,
                "num":num
            }))
    elif switch=='dynamicComment':
        # 动态评论
        dynamicID = request.POST.get('dynamicID')
        dynamic = Dynamic.objects.get(dynamicID=dynamicID)
        person = Person.objects.get(personID=request.session.get('personID')) 
        upcomment = request.POST.get('ucomment')
        ucommentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        DynamicComment.objects.create(
            commentContent = upcomment,
            commentUser = person,
            commentDynamic = dynamic,
            commentTime = ucommentTime
            )

        result = 1
        dynamicCommentList = DynamicComment.objects.filter(commentDynamic=dynamic)[::-1]
        num = len(dynamicCommentList)
        
        if num>0:
            dynamicComment = []
            for tem in range(num):
                dic = {}
                dic['commentUser'] = dynamicCommentList[tem].commentUser.personName
                dic['commentContent'] = dynamicCommentList[tem].commentContent 
                dic['commentTime'] = dynamicCommentList[tem].commentTime.strftime('%Y-%m-%d %H:%M:%S')
                dynamicComment.append(dic)
        else:
            dynamicComment = []
        return HttpResponse(json.dumps({
                "result": result,
                "dynamicComment":dynamicComment,
                "num":num
            }))
    else:
        pass

def switch_views(request):
    
    switch = request.POST.get('switch')


    # ----------------------------动态点赞------------------------------------
    if switch == 'dynamicThumUp':

        # 判断动态是否已点赞
        result = 0
        dynamicID = request.POST.get('dynamicID')
        person = Person.objects.get(personID=request.session.get('personID')) 
        dynamic = Dynamic.objects.get(dynamicID = dynamicID)
        sender = dynamic.sender.personName

        try :
            dynamicThumbUp = DynamicThumbUp.objects.filter(likeDynamic=dynamic)
            for user in dynamicThumbUp:
                if user.likeUser == person : 
                    result = 1
        except: 
            result = 0

        if result == 0:
            # 没有点赞过就完成点赞
            DynamicThumbUp.objects.create(
                    likeUser = person,
                    likeDynamic = dynamic
                    )
        
        # result 0:点赞成功;1：已点赞
        return HttpResponse(json.dumps({
                "result": result
            }))
        
    # ----------------------------文章点赞------------------------------------
    elif switch == 'articleThumbUp':
       # 判断文章是否已点赞
        result = 0
        articleID = request.POST.get('articleID')
        person = Person.objects.get(personID=request.session.get('personID')) 
        article = Article.objects.get(articleID = articleID)
        sender = article.sender.personName

        try :
            articleThumbUp = ArticleThumbUp.objects.filter(likeArticle=article)
            for user in articleThumbUp:
                if user.likeUser == person : 
                    result = 1
        except: 
            result = 0

        if result == 0:
            # 没有点赞过就完成点赞
            ArticleThumbUp.objects.create(
                    likeUser = person,
                    likeArticle = article
                    )
        # result 0:点赞成功;1：已点赞
        return HttpResponse(json.dumps({
                "result": result
            }))
        

    # ----------------------------想法点赞------------------------------------
    elif switch == 'ideaThumbUp':
        # 判断想法是否已点赞
        result = 0
        ideaID = request.POST.get('ideaID')
        person = Person.objects.get(personID=request.session.get('personID')) 
        print(ideaID)
        idea = Idea.objects.get(ideaID = ideaID)
        sender = idea.sender.personName

        try :
            ideaThumbUp = IdeaThumbUp.objects.filter(likeIdea=idea)
            for user in ideaThumbUp:
                if user.likeUser == person : 
                    result = 1
        except: 
            result = 0

        if result == 0:
            # 没有点赞过就完成点赞
            IdeaThumbUp.objects.create(
                    likeUser = person,
                    likeIdea = idea
                    )
        # result 0:点赞成功;1：已点赞
        return HttpResponse(json.dumps({
                "result": result
            }))

    # ----------------------------文章收藏------------------------------------
    elif switch == 'articleCollection':
        # 判断文章是否已收藏
        result = 0
        articleID = request.POST.get('articleID')
        person = Person.objects.get(personID=request.session.get('personID')) 
        article = Article.objects.get(articleID = articleID)
        sender = article.sender.personName

        try :
            articleCollection = ArticleCollection.objects.filter(collectionArticle=article)
            for user in articleCollection:
                if user.collectionUser == person : 
                    result = 1
        except: 
            result = 0

        if result == 0:
            # 没有收藏过就完成收藏
            ArticleCollection.objects.create(
                    collectionUser = person,
                    collectionArticle = article
                    )
        # result 0:收藏成功;1：已收藏
        return HttpResponse(json.dumps({
                "result": result
            }))

    # ----------------------------想法收藏------------------------------------
    elif switch == 'ideaCollection':
        # 判断想法是否已收藏
        result = 0
        ideaID = request.POST.get('ideaID')
        person = Person.objects.get(personID=request.session.get('personID')) 
        idea = Idea.objects.get(ideaID = ideaID)
        sender = idea.sender.personName

        try :
            ideaCollection = IdeaCollection.objects.filter(collectionIdea=idea)
            for user in ideaCollection:
                if user.collectionUser == person : 
                    result = 1
        except: 
            result = 0

        if result == 0:
            # 没有收藏过就完成收藏
            IdeaCollection.objects.create(
                    collectionUser = person,
                    collectionIdea = idea
                    )
        # result 0:收藏成功;1：已收藏
        return HttpResponse(json.dumps({
                "result": result
            }))

    # ----------------------------动态评论------------------------------------
    elif switch == 'dynamicComment':
        # 动态评论
        dynamicID = request.POST.get('dynamicID')
        dynamic = Dynamic.objects.get(dynamicID=dynamicID)
        dynamicCommentList = DynamicComment.objects.filter(commentDynamic=dynamic)[::-1]
        num = len(dynamicCommentList)


        if num>0:

            dynamicComment = []
            for tem in range(num):
                dic = {}
                dic['commentUser'] = dynamicCommentList[tem].commentUser.personName
                dic['commentContent'] = dynamicCommentList[tem].commentContent 
                dic['commentTime'] = dynamicCommentList[tem].commentTime.strftime('%Y-%m-%d %H:%M:%S')

                dynamicComment.append(dic)
            
        else:
            dynamicComment = []
            num = 0



        return HttpResponse(json.dumps({
                "dynamicComment":dynamicComment,
                "num":num
            }))

    # ----------------------------文章评论------------------------------------
    elif switch == 'articleComment':
        # 文章评论
        articleID = request.POST.get('articleID')
        article = Article.objects.get(articleID=articleID)
        articleTitle = article.title;
        articleCommentList = ArticleComment.objects.filter(commentArticle=article)[::-1]
        num = len(articleCommentList)


        if num>0:

            articleComment = []
            for tem in range(num):
                dic = {}
                dic['commentUser'] = articleCommentList[tem].commentUser.personName
                dic['commentContent'] = articleCommentList[tem].commentContent 
                dic['commentTime'] = articleCommentList[tem].commentTime.strftime('%Y-%m-%d %H:%M:%S')

                articleComment.append(dic)
            
        else:
            articleComment = []
            num = 0

        return HttpResponse(json.dumps({
                "articleComment":articleComment,
                "articleTitle":articleTitle,
                "num":num
            }))
    
    # ----------------------------动态删除------------------------------------
    elif switch == 'dynamicDelete':
        # 动态删除
        dynamicID = request.POST.get('dynamicID')
        dynamic = Dynamic.objects.get(dynamicID=dynamicID)
        DynamicThumbUp.objects.filter(likeDynamic=dynamic).delete()
        DynamicComment.objects.filter(commentDynamic=dynamic).delete()
        dynamic.delete()
        return HttpResponse(json.dumps({"result": 1}))

    # ----------------------------想法删除------------------------------------
    elif switch == 'ideaDelete':
        # 想法删除
        ideaID = request.POST.get('ideaID')
        idea = Idea.objects.get(ideaID=ideaID)
        IdeaThumbUp.objects.filter(likeIdea=idea).delete()
        
        idea.delete()
        return HttpResponse(json.dumps({"result": 1}))

    # ----------------------------文章删除------------------------------------
    elif switch == 'articleDelete':
        # 文章删除
        articleID = request.POST.get('articleID')
        article = Article.objects.get(articleID=articleID)
        ArticleThumbUp.objects.filter(likeArticle=article).delete()
        ArticleComment.objects.filter(commentArticle=article).delete()
        ArticleCollection.objects.filter(collectionArticle=article).delete()
        article.delete()
        return HttpResponse(json.dumps({"result": 1}))
    else:
        return HttpResponse('出现错误，请联系网站管理员解决')

# 搜索
def searchViews(request):
    searchContent = request.POST.get('searchContent')
    if searchContent==None:
        searchContent = ""
    ideaList = Idea.objects.filter(content__icontains=searchContent)
    personList = Person.objects.filter(personName__contains=searchContent)
    articleList = Article.objects.filter(title__contains=searchContent)
    return render(request,'search.html',locals())