from django.urls import path
from django.conf.urls import url
from member import views

app_name = 'member'

urlpatterns = [
    url('main', views.main_field, name='main'),
    url('编委领域审查主界面.html', views.main_field),
    url('编委水平审查主界面.html',views.main_level,name='main_level'),
    path('编委领域审阅界面.html', views.censor, name='censor'),
    path('编委水平审阅界面.html', views.censor_level, name='censor_level'),
    path('logout/', views.user_logout, name='u_logout'),
    path('return/', views.return_main, name='return_main'),
    path('accept/', views.member_accept,name = 'member_accept'),
    path('modify/', views.member_modify,name = 'member_modify'),
    path('accept_level/', views.member_accept_level,name = 'member_accept_level'),
    path('modify_level/', views.member_modify_level,name = 'member_modify_level'),
    path('download/',views.download,name='download'),
    path('reject/',views.level_reject,name='level_reject'),
]