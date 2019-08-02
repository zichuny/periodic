from django.urls import path
from . import views

app_name = 'author'

urlpatterns = [
    path('author_contribute/',views.author_contribute,name='author_contribute'),
    path('contribute/',views.contribute,name='contribute'),
    path('modify/',views.modify,name='modify'),
    path('savefile/',views.savefile,name='savefile'),
    path('data_fresh/',views.data_fresh,name='data_fresh'),
    path('reupload/',views.reupload,name='reupload'),
    path('logout/', views.user_logout, name='logout'),

]