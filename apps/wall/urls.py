from django.urls import path
from . import views

urlpatterns = [
    path('wall_app/', views.wall_index, name='wall_index'),
    path('wall_app/<str:name>/', views.hello_name, name='wall_hello_name'),
]