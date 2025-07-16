# owner/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("vendor-approval/", views.vendor_approval, name="vendor_approval"),
    path("user-management/", views.user_management, name="user_management"),
    path("order-monitoring/", views.order_monitoring, name="order_monitoring"),
    
]