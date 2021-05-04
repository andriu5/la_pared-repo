from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall_index, name='wall_index'),
    path('post_message/', views.post_messages, name='post_messages'),
    path('post_comment/<int:id>/', views.post_comments, name='post_comments'),
    path('delete_message/<int:id>/', views.delete_message, name='delete_message'),
    path('logout/', views.logout, name='wall_logout'),
]