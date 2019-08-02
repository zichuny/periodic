from django.urls import path
from django.conf.urls import url
from editor import views

app_name = 'editor'

urlpatterns = [
    url('main', views.main, name='main'),
    url('编辑主界面.html', views.main),
    path('编辑审阅界面.html', views.censor, name='censor'),
    path('logout/', views.user_logout, name='u_logout'),
    path('return/', views.return_main, name='return_main'),
    path('accept/', views.editor_accept,name = 'editor_accept'),
    path('modify/', views.editor_modify,name = 'editor_modify'),
    path('download/',views.download,name='download'),
]