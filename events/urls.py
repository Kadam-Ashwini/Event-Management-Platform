from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/update/', views.event_update, name='event_update'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
    # Food Item URLs
    path('food-items/create/', views.food_item_create, name='food_item_create'),
    path('food-items/<int:item_id>/update/', views.food_item_update, name='food_item_update'),
    path('food-items/<int:item_id>/delete/', views.food_item_delete, name='food_item_delete'),
]
