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
    # 关注
    url(r'^follow/(\d+)/$',addFollowViews,name='addFollowPerson'),

    # 以下新添加
    url(r'^person/personTrends/$',indexPersonTrendsViews),
    url(r'^person/personIdea/$',indexPersonIdeaViews),
    url(r'^person/personCollectionIdea/$',indexPersonCollectionIdeaViews),
    url(r'^person/personCollectionArti/$',indexPersonCollectionArtiViews),
    url(r'^person/personArticle/$',indexPersonArticleViews),
    url(r'^person/personFollow/$',indexPersonFollowViews),
    url(r'^person/editPerson/$',editPersonViews),
    url(r'^person/indexPerson/$',indexPerson),
    url(r'^person/likePerson/$',likePerson),

    #推送
    url(r'^pushtest/$', pushDynamicViews),

    # 其他人的视图
    url(r'^person/personTrends/(\d+)/$',indexOtherPersonTrendsViews,name='othersTrends'),
    url(r'^person/personIdea/(\d+)/$',indexOtherPersonIdeaViews),
    url(r'^person/personCollectionIdea/(\d+)/$',indexOtherPersonCollectionIdeaViews),
    url(r'^person/personArticle/(\d+)$',indexOtherPersonArticleViews),
    url(r'^person/personFollow/(\d+)$',indexOtherPersonFollowViews),
    # url(r'^person/editPerson/$',editPersonViews),
    # url(r'^person/indexPerson/$',indexPerson),
    # url(r'^person/likePerson/$',likePerson),

    # 文章编辑
    url(r'^postnew/$',post_article),
    url(r'^postnew/save/$',save_article),
    url(r'^admin/uploads/(?P<dir_name>[^/]+)/$', upload_image, name='upload_image'),

    # 搜索
    url(r'^search/$',searchViews),

    #　管理员
    url(r'^administror_changepassword/$',changepassword),
]

# 动态　想法　文章　的　点赞　评论　收藏
urlpatterns +=[
    # 显示动态
    url(r'^indexComment/$',indexComment_views),
    # 开关
    url(r'^switch/$',switch_views),
]
