from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	url(r'^blogs/$', views.Blog.as_view(), name='posts'),
	url(r'^blog/(?P<pk>\d+)$', views.BlogView.as_view(), name='post-detail'),
	url(r'^courses/$', views.Coursess.as_view(), name='courses'),
	url(r'^course/(?P<pk>\d+)$', views.CourseView.as_view(), name='course-detail'),
	url(r'^success', views.success, name='success'),
	url(r'^subscribe', views.subscribe, name='subscribe'),
	url(r'^about', views.about, name='about'),
	url(r'^contact', views.contact, name='contact'),
	path('confirmation/<str:email>/<str:random>/', views.confirmation, name = 'confirmation'),
]