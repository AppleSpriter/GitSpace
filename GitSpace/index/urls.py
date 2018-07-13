from django.conf.urls import url
from .views import *
from .upload import *

urlpatterns = [
    url(r'^$',indexAfterLoginViews),
    # 发布动态
    url(r'^publishDynamic/$',publishDynamicViews),
    url(r'^publishIdea/$',publishIdeaViews),
    
    # 初始的主页
    url(r'^indexHot/$',indexHotViews),
    url(r'^indexLike/$',indexLikeViews),
    url(r'^indexRecommend/$',indexRecommendViews),
    # 登录后的主页
    url(r'^indexAfterLogin/$',indexAfterLoginViews),
    # 登录
    url(r'^login/$',loginViews),
    # 注册
    url(r'^register/$',registerViews),
    url(r'^protocol/$', protocolViews),
    url(r'^discuss/(\d+)/$',discussViews),
    url(r'^dropIdea/(\d+)/$',dropIdeaViews,name='dropIdea'),
    url(r'^deleteIdeaMember/(\d+)/$',deleteIdeaMemberViews),
    # 退出
    url(r'^logOut/$',logOutViews),
    # 取消关注
    url(r'^cancelFollow/(\d+)/$',cancelFollowViews,name='cancelFollowPerson'),
    # 取消想法收藏 取消文章收藏
    url(r'^cancelCollectionIdea/(\d+)/$',cancelCollectionIdeaViews,name='cancelCollectionIdea'),
    url(r'^cancelCollectionArti/(\d+)/$',cancelCollectionArtiViews,name='cancelCollectionArti'),
    # 关注
    url(r'^follow/(\d+)/$',addFollowViews,name='addFollowPerson'),

    # 以下个人页面显示,分别是动态　想法　想法收藏　文章收藏　文章　关注列表　修改个人信息页面
    url(r'^person/personTrends/$',indexPersonTrendsViews),
    url(r'^person/personIdea/$',indexPersonIdeaViews),
    url(r'^person/personCollectionIdea/$',indexPersonCollectionIdeaViews),
    url(r'^person/personCollectionArti/$',indexPersonCollectionArtiViews),
    url(r'^person/personArticle/$',indexPersonArticleViews),
    url(r'^person/personFollow/$',indexPersonFollowViews),
    url(r'^person/editPerson/$',editPersonViews),
    url(r'^person/indexPerson/$',indexPersonTrendsViews),

    #推送
    url(r'^pushtest/$', pushDynamicViews),

    # 其他人的视图
    url(r'^person/personTrends/(\d+)/$',indexOtherPersonTrendsViews,name='othersTrends'),
    url(r'^person/personIdea/(\d+)/$',indexOtherPersonIdeaViews),
    url(r'^person/personCollectionIdea/(\d+)/$',indexOtherPersonCollectionIdeaViews),
    url(r'^person/personCollectionArti/(\d+)/$',indexOtherPersonCollectionArtiViews),
    url(r'^person/personArticle/(\d+)/$',indexOtherPersonArticleViews),
    url(r'^person/personFollow/(\d+)/$',indexOtherPersonFollowViews),

    # 文章编辑
    url(r'^postnew/$',post_article),
    url(r'^postnew/save/$',save_article),
    url(r'^admin/uploads/(?P<dir_name>[^/]+)/$', upload_image, name='upload_image'),
    url(r'^article/edit/(\d+)/$',edit_article),

    # 文章显示
    url(r'^article/(\d+)/$', get_article),

    # 搜索
    url(r'^search/$',searchViews),

    #　密码修改
    url(r'^changepassword/$',changepassword),
]

# 动态　想法　文章　的　点赞　评论　收藏
urlpatterns +=[
    # 显示动态
    url(r'^indexComment/$',indexComment_views),
    # 开关
    url(r'^switch/$',switch_views),
]
