from django.db import models

# Create your models here.
class Person(models.Model):
    personID = models.AutoField(primary_key=True)
    personName = models.CharField(max_length=30)
    personPassword = models.CharField(max_length=128)
    personMobile = models.CharField(max_length=20)
    personEmail = models.EmailField(max_length=50)
    personImage = models.CharField(max_length=100)
    personInfo = models.CharField(max_length=100,null=True)
    personSex = models.CharField(max_length = 5,null=True)
    isActive = models.BooleanField(default=True)
    enrollDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.personName

    # @property
    # def get_articles(self):
    #     return articles.all()

    class Meta:
        verbose_name_plural='用户列表'

class PersonFollow(models.Model):
    follower = models.ForeignKey(Person,related_name='follower_person')
    followee = models.ForeignKey(Person,related_name='followee_person')

    class Meta:
        verbose_name_plural='关注列表'

class Dynamic(models.Model):
    dynamicID = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Person)
    content = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.dynamicID)
    class Meta:
        verbose_name_plural='动态列表'

class Article(models.Model):
    articleID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    description = models.TextField(null=True)
    label = models.BigIntegerField()
    sender = models.ForeignKey(Person,related_name='articles')
    createDate = models.DateTimeField(auto_now_add=True)
    isPub = models.BooleanField(1)
    
    def __str__(self):
        return str(self.title)

    # @property
    # def get_comments(self):
    #     return comments.all()

    class Meta:
        verbose_name_plural='文章列表'


class Idea(models.Model):
    ideaID = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Person)
    content = models.TextField()
    createDate = models.DateTimeField()
    label = models.BigIntegerField() 

    def __str__(self):
        return self.content
        # return self.sender.personName

    class Meta:
        verbose_name_plural='想法列表'


# 系统推荐，推荐推送稍后作为补充功能，首先做基本的关注推送
class ArticleComment(models.Model):
    articleCommentID = models.AutoField(primary_key=True)
    commentContent = models.CharField(max_length=466)
    commentUser = models.ForeignKey(Person)
    commentArticle = models.ForeignKey(Article,related_name='comments')
    commentTime = models.DateTimeField()

    def __str__(self):
        return str(self.articleCommentID)

    class Meta:
        verbose_name_plural='文章评论表'



class DynamicComment(models.Model):
    dynamicCommentID = models.AutoField(primary_key=True)
    commentContent = models.CharField(max_length=466)
    commentUser = models.ForeignKey(Person)
    commentDynamic = models.ForeignKey(Dynamic)
    commentTime = models.DateTimeField()

    def __str__(self):
        return str(self.dynamicCommentID)

    class Meta:
        verbose_name_plural='动态评论表'

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


# －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

class IdeaMessage(models.Model):
    sender = models.ForeignKey(Person)
    idea = models.ForeignKey(Idea)
    content = models.CharField(max_length=466)
    publishDate = models.DateTimeField()

class IdeaMember(models.Model):
    idea = models.ForeignKey(Idea)
    member = models.ForeignKey(Person)
    
# class Push(models.Model):
#     pushID = models.AutoField(primary_key=True)
#     userID = models.ForeignKey(Person)

    
#     def __str__(self):
#         return self.pushID;

#     class Meta:
#         verbose_name_plural='推送表'

# class PushMessage(models.Model):
#     pushMessageId = models.AutoField(primary_key=True)
#     pushMessageType = models.CharField(max_length=20)
#     pushMessageDate = models.DateField()
#     pushMessageUserID = models.ForeignKey(Person)

    
#     def __str__(self):
#         return self.pushMessageId;

#     class Meta:
#         verbose_name_plural='推送消息表'
# class PushArticle(models.Model):
#     pushMessageId 
#     articleID
#     personID
#     pushData
