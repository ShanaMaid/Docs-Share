from django.conf.urls import url
from .import views
urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^adminIndex/$',views.adminIndex,name='adminIndex'),
	url(r'^deleteArticle/$',views.deleteArticle,name='deleteArticle'),
	url(r'^addArticle/$',views.addArticle,name='addArticle'),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^approve/$',views.approve,name='approve'),
	url(r'^addUser/$',views.addUser,name='addUser'),
	url(r'^removeUser/$',views.removeUser,name='removeUser'),
	url(r'^addGroup/$',views.addGroup,name='addGroup'),
	url(r'^removeGroup/$',views.removeGroup,name='removeGroup'),
	url(r'^getGroup/$',views.getGroup,name='getGroup'),
	url(r'^checkRole/(^$)$',views.checkRole,name='checkRole'),
	url(r'^clients/$',views.clients,name='clients')
]
