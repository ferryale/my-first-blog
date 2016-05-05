from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.information, name = 'information'),
	url(r'^posts$', views.post_list, name = 'post_list'),
	url(r'^drafts/$', views.post_draft_list, name = 'post_draft_list'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name = 'post_detail'),
	url(r'^authorization_error/$', views.authorization_error, name = 'authorization_error'),
	url(r'^post/new/$', views.post_new, name = 'post_new'),
	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name = 'post_edit'),
	url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name = 'post_publish'),
	url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name = 'post_remove'),
	url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name = 'add_comment_to_post'),
	url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name = 'comment_approve'),
	url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name = 'comment_remove'),
        url(r'^documents/list/$', views.document_list, name = 'document_list'),
        url(r'^documents/upload/$', views.document_upload, name = 'document_upload'),
        url(r'^documents/(?P<pk>\d+)/remove/$', views.document_remove, name = 'document_remove'),
]
