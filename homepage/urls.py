from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('forget/', views.forget, name='forget'),
    path('signup/', views.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('error/',views.error,name='error'),
    path('changepwd/',views.changepwd,name='changepwd'),
    path('send_email/',views.send_email,name='send_email'),
]