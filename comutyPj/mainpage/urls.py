from django.urls import path
from mainpage import views as my_views

urlpatterns = [
    path('', my_views.home, name='main-home'),
    path('room/<int:pk>', my_views.room, name='room'),

    path('create-room/', my_views.createroom, name='create-room'),
    path('update-room/<int:pk>', my_views.updateroom, name='update-room'),
    path('delete-room/<int:pk>', my_views.deleteroom, name='delete-room'),
]
