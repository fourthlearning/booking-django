from django.urls import path
from . import views

urlpatterns = [
    #path('', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('index/', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('add/', views.room_add, name='room_add'),
    path('update/<int:room_id>/', views.room_update, name='room_update'),
    path('delete/<int:room_id>/', views.room_delete, name='room_delete'),
    path('requestlist/', views.requestlist, name='requestlist'),
    path('requestlist/edit/<int:request_id>', views.requestlist_edit, name='requestlist_edit')
]