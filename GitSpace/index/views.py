from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.contrib import messages
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
    label1 = request.POST['label1']
    label2 = request.POST['label2']
    dic1 = {
    'java':1,
    'c':2,
    'c++':4,
    'python':8
    }
    dic2 = {
    '大数据':16,
    '人工智能':32,
    '游戏开发':64,
    '编程学习':128
    }
    person = Person.objects.get(personID=request.session.get('personID'))
    Idea.objects.create(sender=person,content=ideaContent,createDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),label=(dic1[label1]|dic2[label2]))    
    return HttpResponseRedirect('/indexAfterLogin/')

def indexHotViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
    return render(request,'indexHot.html',locals())

def indexLikeViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
    return render(request,'indexLike.html',locals())

def indexRecommendViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
    return render(request,'indexRecommend.html',locals())

def indexAfterLoginViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        dynamicList = Dynamic.objects.all()[::-1]
        ideaList = Idea.objects.all()[::-1]
        articleLsit = Article.objects.all()[::-1]
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
        if vuser:
            messages.add_message(request,messages.ERROR,'Repeat of user name')
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
                newuser = Person.objects.create(personName=personName,personPassword=finalPassword,personMobile=personMobile,personEmail=personEmail,isActive=True,personInfo='我是古天乐。',personImage='/imgs/head.png')
                request.session['personID'] = newuser.personID
                return HttpResponseRedirect('/indexAfterLogin')

# 修改密码,管理员功能
def changepassword(request):
    uname = "C莫儿"
    upwd = "mgf123456"
    finalPassword = make_password(upwd) 
    Person.objects.filter(personName=uname).update(personPassword=finalPassword)
    return HttpResponse("change successfully")

# 
def protocolViews(request):
    return render(request,'protocol.html')

def discussViews(request,ideaID):
    if request.method == 'GET':
        person = Person.objects.get(personID=request.session.get('personID'))
        idea = Idea.objects.get(ideaID=ideaID)
        ideaMessageList = IdeaMessage.objects.filter(idea = idea)
        ideaMemberList = []
        for i in ideaMessageList:
            if i.sender  not in ideaMemberList:
                ideaMemberList.append(i.sender)
        #print(ideaMemberList)
        return render(request,'discuss.html',locals())
    else:
        person = Person.objects.get(personID=request.session.get('personID'))
        idea = Idea.objects.get(ideaID=ideaID)
        content = request.POST.get('message')
        IdeaMessage.objects.create(sender=person,idea=idea,content = content,publishDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return HttpResponseRedirect('/discuss/'+str(idea.ideaID))


# 以下是更新的内容

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

# 查询自己的动态
def indexPersonTrendsViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        dynamicList = Dynamic.objects.filter(sender=person)[::-1]
        return render(request,'person/indexPersonTrends.html',{'dynamicList':dynamicList, 'person':person})
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
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonTrends.html',\
                {'dynamicList':dynamicList, 'person':person, 'followMes': json.dumps(1)})
        else:
            return render(request,'otherperson/indexOtherPersonTrends.html',\
                {'dynamicList':dynamicList, 'person':person, 'followMes': json.dumps(0)})

#　查询自己的想法
def indexPersonIdeaViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        ideaList = Idea.objects.filter(sender=person)[::-1]
        return render(request,'person/indexPersonIdea.html',{'ideaList':ideaList,'person':person})
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
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonIdea.html',\
                {'ideaList':ideaList, 'person':person, 'followMes': json.dumps(1)})
        else:
            return render(request,'otherperson/indexOtherPersonIdea.html',\
                {'ideaList':ideaList, 'person':person, 'followMes': json.dumps(0)})

# 自己的想法收藏显示
def indexPersonCollectionIdeaViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        ideaCollectionList = IdeaCollection.objects.filter(collectionUser=person)
        return render(request,'person/indexPersonCollectionIdea.html',locals())
    else:
        return HttpResponseRedirect('/indexHot')

# 自己的文章收藏显示
def indexPersonCollectionArtiViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        artiCollectionList = ArticleCollection.objects.filter(collectionUser=person)
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
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonCollectionIdea.html',\
                {'ideaCollectionList':ideaCollectionList, 'person':person, 'followMes': json.dumps(1)})
        else:
            return render(request,'otherperson/indexOtherPersonCollectionIdea.html',\
                {'ideaCollectionList':ideaCollectionList, 'person':person, 'followMes': json.dumps(0)})

# 自己的文章显示
def indexPersonArticleViews(request):
    if 'personID' in request.session:
        person = Person.objects.get(personID=request.session.get('personID'))
        return render(request,'person/indexPersonArticle.html',{'person':person})
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
        artiCollectionList = ArticleCollection.objects.filter(collectionUser=person)
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonArticle.html',\
                {'artiCollectionList':artiCollectionList, 'person':person, 'followMes': json.dumps(1)})
        else:
            return render(request,'otherperson/indexOtherPersonArticle.html',\
                {'artiCollectionList':artiCollectionList, 'person':person, 'followMes': json.dumps(0)})


# 自己的关注列表
def indexPersonFollowViews(request):
    if 'personID' in request.session:
        follower = Person.objects.get(personID=request.session.get('personID'))
        presonFollowList = PersonFollow.objects.filter(follower=follower)
        return render(request,'person/indexPersonFollow.html',\
            {'presonFollowList':presonFollowList,'person':follower})
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
        follower = Person.objects.get(personID=ID)
        presonFollowList = PersonFollow.objects.filter(follower=follower)
        check = checkFollow(ID,currentpersonID)
        if check:
            # 传值动态列表，person，是否在关注表
            return render(request,'otherperson/indexOtherPersonFollow.html',\
                {'presonFollowList':presonFollowList, 'person':person, 'followMes': json.dumps(1)})
        else:
            return render(request,'otherperson/indexOtherPersonFollow.html',\
                {'presonFollowList':presonFollowList, 'person':person, 'followMes': json.dumps(0)})


def logOutViews(request):
    del request.session['personID']
    return HttpResponseRedirect('/indexHot')

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
            if request.POST.get('userImage'):
                obj = request.FILES['userImage']
                f = open(os.getcwd()+'/index/static/imgs/userhead/'+ person.personID + "-" +obj.name,'wb+')
                for chunk in obj.chunks():
                    f.write(chunk)
                f.close()
                person.personImage = '/static/imgs/userhead/'+ person.personID + "-" +obj.name
            person.personInfo = request.POST.get('userInfo')
            person.save()
            return HttpResponseRedirect('/person/indexPerson/')
    else:
        return HttpResponseRedirect('/indexHot')

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
    if request.method == 'GET':
        person = Person.objects.get(personID=request.session.get('personID'))
        idea = Idea.objects.get(ideaID=ideaID)
        ideaMessageList = IdeaMessage.objects.filter(idea = idea)
        ideaMemberList = []
        for i in ideaMessageList:
            if i.sender  not in ideaMemberList:
                ideaMemberList.append(i.sender)
        #print(ideaMemberList)
        return render(request,'discuss.html',locals())
    else:
        person = Person.objects.get(personID=request.session.get('personID'))
        idea = Idea.objects.get(ideaID=ideaID)
        content = request.POST.get('message')
        IdeaMessage.objects.create(sender=person,idea=idea,content = content,publishDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return HttpResponseRedirect('/discuss/'+str(idea.ideaID))

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

def deleteIdeaMemberViews(request,ideaID):
    if 'personID' in request.session:
        deleteIdeaMember = request.POST.getlist('deleteIdeaMember')
        idea = Idea.objects.get(ideaID=ideaID)
        for p in deleteIdeaMember:
            IdeaMessage.objects.filter(idea = idea,sender=Person.objects.get(personID=int(p))).delete()
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
def get_artilce_list(request, person_id):
    person=Person.objects.get(personID=person_id)
    articleList=person.Article_set().all
    return render_to_response('article-list.html', {'articleList': articleList})

def get_artilce(request, article_id):
    try:
        article=Article.objects.get(articleID=article_id)
    except Article.DoesNotExist:
        raise Http404
    comments=article.ArticleComment_set().all
    ctx={
        'article': article,
        'comments': comments
    }
    return render(request, 'show-article.html', ctx)

def post_article(request):
    if request.method == 'GET':
       return render(request,'post-article.html')

def save_article(request): 
    if request.is_ajax():
        person = Person.objects.get(personID=request.session.get('personID'))
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content=request.POST.get('cont')
        title=request.POST.get('titl')
        # ____________________________________待修改___________________________________________________________
        label = 1
        description=request.POST.get('des')
        isPub=request.POST.get('isPub')
        Article.objects.create(title=title,content=content,description=description,label=label,sender=person,createDate=date,\
          isPub=isPub)
        print("inserted!")

        if ispub == 0 :
            ctx={
                'artl-id':0,
                'result':1
            }
            return HttpResponse(json.dumps(ctx))
        else :
            ctx={
                'artl-id':1,
                'result': 0
            }
            return HttpResponse(json.dumps(ctx))


# ---------------------------------------------------------------------------------
def indexComment_views(request):
    switch = request.POST.get('switch')

    if switch=='articleComment':
        pass
        # 文章评论
        # articleCommentList = ArticleComment.objects.all()[::-1]
        # num = len(articleCommentList)

        # person = Person.objects.get(personID=request.session.get('personID'))
        # ucommentArticle = Article.objects.get(articleID=ID)
        # upcomment = request.POST.get('ucomment')
        # ucommentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # ArticleComment.objects.create(
        #         commentUser=person,
        #         commentArticle=ucommentArticle,
        #         commentContent=upcomment,
        #         commentTime=ucommentTime)
        # return HttpResponseRedirect('/indexHot/')
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
        print (dynamicID)
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
    else:
        return HttpResponse('error')

# 搜索
def searchViews(request):
    searchContent = request.POST.get('searchContent')
    if searchContent==None:
        searchContent = ""
    ideaList = Idea.objects.filter(content__icontains=searchContent)
    personList = Person.objects.filter(personName__icontains=searchContent)
    # article = Article.objects.filter(articleTitle__icontains=searchContent)
    return render(request,'search.html',locals())