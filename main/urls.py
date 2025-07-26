from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('chat/', views.public_chat, name='public_chat'),
    path('send/', views.send_message, name='send_message'),
    path('chat/private/<str:username>/', views.private_chat_view, name='private_chat'),
    path('messages/', views.private_chat_list, name='private_chat_list'),
]