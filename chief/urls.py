from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'chief'

urlpatterns = [
    path('main', views.main, name = 'main'),
    path('main/主编审阅界面.html', views.censor, name='censor'),
    path('manage', views.manage, name='manage'),
    path('manage/主编人事信息添加界面.html', views.add, name='add'),
    path('主编人事信息添加界面.html', views.add, name='add'),
    path('用户登录界面.html', views.main),
    path('manage/用户登录界面.html', views.main),
    path('logout/', views.user_logout, name='u_logout'),
    path('delete/', views.delete_faculty, name='delete_faculty'),
    url(r'^manage/主编人事信息更改界面.html', views.modify, name='modify'),
    path('censor', views.censor, name='censor'),
    path('censor/主编审阅界面.html', views.censor_detail, name='censor_detail'),
    path('accept/',views.chief_accept,name='accept'),
    path('reject/',views.chief_reject,name='reject'),
    path('download/',views.download,name='download'),
    path('modify/', views.chief_modify, name='chief_modify'),

]