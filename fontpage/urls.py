from django.conf.urls import url
from .import views
urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^adminIndex/$',views.adminIndex,name='adminIndex'),
	url(r'^deleteArticle/$',views.deleteArticle,name='deleteArticle'),
	url(r'^addArticle/$',views.addArticle,name='addArticle'),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^approve/$',views.approve,name='logout'),
	url(r'^addUser/$',views.addUser,name='logout'),
	url(r'^removeUser/$',views.removeUser,name='logout'),
	url(r'^addGroup/$',views.addGroup,name='logout'),
	url(r'^removeGroup/$',views.removeGroup,name='logout'),
	url(r'^getGroup/$',views.getGroup,name='logout'),
	url(r'^checkRole/$',views.checkRole,name='logout'),
	url(r'^pCenter/$',views.pCenter,name='pCenter'),
]
