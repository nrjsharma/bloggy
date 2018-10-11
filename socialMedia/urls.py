"""socialMedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list,name='post_list'),
    url(r'^blog/(?P<id>\d+)/(?P<slug>[\w-]+)/$',views.post_details,name="post_detail"),
    url(r'^post_create/$',views.post_create,name='post_create'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.registration, name='register'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^like/$', views.post_like, name='like_post'),
    url(r'^(?P<id>\d+)/post_edit/$', views.post_edit, name='post_edit'),
    url(r'^(?P<id>\d+)/post_delete/$', views.post_delete, name='post_delete'),


    #password reset url
    # url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^password-reset/confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #        OR
    url('^', include('django.contrib.auth.urls')),

 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

