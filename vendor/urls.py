from django.urls import path
from . import views

urlpatterns = [
    
    path("vendor/", views.vendor_index, name="vendor_index"),  
    path("register/", views.vendor_register, name="vendor_register"),
    path("orders/", views.manage_orders, name="manage_orders"),
    path("not-approved/", views.not_approved, name="not_approved"),  
    path("vendor_dashboard/", views.vendor_dashboard, name="vendor_dashboard"),  
    path("loginn/", views.vendor_login, name="vendor_login"),
    path("profile/", views.vendor_profile, name="vendor_profile"),
    path("add-food-item/", views.add_food_item, name="add_food_item"),
    path("update-food-item/<int:food_item_id>/", views.update_food_item, name="update_food_item"),
    path("delete-food-item/<int:food_item_id>/", views.delete_food_item, name="delete_food_item"),
    path("view-food-items/", views.view_food_items, name="view_food_items"),
    path('cart/add/<int:food_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views. checkout, name='checkout'),
    path('payment/<int:order_id>/',views.payment, name='payment'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('pending/', views.pending_orders_view, name='pending')

    
]


