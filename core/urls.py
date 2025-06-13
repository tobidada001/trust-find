
from django.urls import path
from . import views

app_name = 'lost_found'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
   
    # Items
    path('post/', views.post_item, name='post_item'),
    path('my-items/', views.my_items, name='my_items'),
    path('search/', views.search_items, name='search'),
    path('item/<uuid:pk>/', views.item_detail, name='item_detail'),
    path('item/<uuid:pk>/edit/', views.edit_item, name='edit_item'),
    path('item/<uuid:pk>/delete/', views.delete_item, name='delete_item'),
    path('item/<uuid:pk>/resolve/', views.mark_item_resolved, name='mark_resolved'),
    path('item/<uuid:pk>/activate/', views.mark_item_active, name='mark_active'),
    
    # Messages
    path('item/<uuid:pk>/message/', views.send_message, name='send_message'),
    
    # AJAX endpoints
    path('api/delete-image/<int:pk>/', views.delete_image, name='delete_image'),
]