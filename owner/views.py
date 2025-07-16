from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from vendor.models import Vendor
from .models import AdminActionLog

@login_required
def vendor_approval(request):
    if not request.user.is_staff:  
        return redirect("home")
    
    vendors = Vendor.objects.filter(is_approved=False)  
    
    if request.method == "POST":
        vendor_id = request.POST.get("vendor_id")
        action = request.POST.get("action")  
        vendor = get_object_or_404(Vendor, id=vendor_id)
        
        if action == "approve":
            vendor.is_approved = True
            vendor.save()
            AdminActionLog.objects.create(action="Approved Vendor", target_vendor=vendor)
        elif action == "reject":
            vendor.delete()
            AdminActionLog.objects.create(action="Rejected Vendor", target_vendor=vendor)
        
        return redirect("vendor_approval")
    
    return render(request, "vendor_approval.html", {"vendors": vendors})


from django.contrib.auth.models import User

@login_required
def user_management(request):
    if not request.user.is_staff:
        return redirect("home")
    
    users = User.objects.all()  
    
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")  
        user = get_object_or_404(User, id=user_id)
        
        if action == "deactivate":
            user.is_active = False
            user.save()
            AdminActionLog.objects.create(action="Deactivated User", target_user=user)
        elif action == "activate":
            user.is_active = True
            user.save()
            AdminActionLog.objects.create(action="Activated User", target_user=user)
        
        return redirect("user_management")
    
    return render(request, "user_management.html", {"users": users})

from vendor.models import Order

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from vendor.models import Order
from .models import AdminActionLog
from vendor.models import OrderItem  # Import OrderItem

@login_required
def order_monitoring(request):
    if not request.user.is_staff:  
        return redirect("home")

    order_items = OrderItem.objects.all()
    print(order_items)  # Debugging: Check if OrderItems are retrieved

    return render(request, "order_monitoring.html", {"order_items": order_items})


from vendor.models import Order
from django.contrib.auth.models import User

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:  
        return redirect("admin:login")  # Redirect to admin login instead of home

    total_vendors = Vendor.objects.count()
    pending_vendors = Vendor.objects.filter(is_approved=False).count()
    active_users = User.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    recent_logs = AdminActionLog.objects.all().order_by('-timestamp')[:5]

    context = {
        "total_vendors": total_vendors,
        "pending_vendors": pending_vendors,
        "active_users": active_users,
        "total_orders": total_orders,
        "recent_orders": recent_orders,
        "recent_logs": recent_logs,
    }
    
    return render(request, "admin_dashboard.html", context)
