
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Vendor, Order , Cart,CartItem,FoodItem,TrainRoute



@login_required
def vendor_dashboard(request):
    vendor = Vendor.objects.get(user=request.user)

    if not vendor.is_approved:
        return redirect("not_approved") 

    return render(request, "dashboard.html") 

def vendor_register(request):
    return render(request, "register.html")  

def not_approved(request):
    return render(request, "not_approved.html")  





from django.http import JsonResponse

@login_required
def manage_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendor=vendor, status='pending')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')  
        order = Order.objects.get(id=order_id)

        if action == 'accept':
            order.status = 'accepted'
        elif action == 'reject':
            order.status = 'rejected'
        order.save()

        return JsonResponse({'success': True})

    return render(request, 'orders.html', {'orders': orders})

 
from django.contrib.auth.models import User
from django.contrib.auth import login


def vendor_register(request):
    if request.method == "POST":
        business_name = request.POST.get("business_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            return render(request, "vendor_register.html", {"error": "Email already registered."})

        user = User.objects.create_user(username=email, email=email, password=password)
        vendor = Vendor.objects.create(user=user, business_name=business_name, is_approved=False)

        login(request, user)  
        return redirect("/pending/") 

    return render(request, "vendor_register.html")
def pending_orders_view(request):
    return render(request, 'pending_orders.html')  

def vendor_index(request):
    return render(request, "vendor_index.html")







from django.contrib.auth import authenticate, login
from django.contrib import messages


def vendor_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            try:
                
                vendor = Vendor.objects.get(user=user)
                if vendor.is_approved:
                    login(request, user)  
                    return redirect("vendor_dashboard")  
                else:
                    messages.error(request, "Your account has not been approved yet.")
            except Vendor.DoesNotExist:
                messages.error(request, "You are not registered as a vendor.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "vendor_login.html")
from django.contrib.auth.decorators import login_required

@login_required
def vendor_dashboard(request):
    
    vendor = Vendor.objects.get(user=request.user)
    return render(request, "dashboard.html", {"vendor": vendor})

from django.shortcuts import render, get_object_or_404

@login_required
def vendor_profile(request):
    
    vendor = get_object_or_404(Vendor, user=request.user)
    return render(request, "profile.html", {"vendor": vendor})


from .forms import FoodItemForm

@login_required
def add_food_item(request):
    vendor = Vendor.objects.get(user=request.user)
    if not vendor.is_approved:
        return redirect("not_approved")  

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.vendor = vendor
            food_item.save()
            return redirect("vendor_dashboard")
        else:
            print(form.errors)  

    else:
        form = FoodItemForm()

    return render(request, "add_food_item.html", {"form": form})


@login_required
def update_food_item(request, food_item_id):
    vendor = Vendor.objects.get(user=request.user)
    food_item = FoodItem.objects.get(id=food_item_id, vendor=vendor)

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = FoodItemForm(instance=food_item)

    return render(request, "update_food_item.html", {"form": form})

@login_required
def delete_food_item(request, food_item_id):
    vendor = Vendor.objects.get(user=request.user)
    food_item = FoodItem.objects.get(id=food_item_id, vendor=vendor)
    food_item.delete()
    return redirect("vendor_dashboard")


@login_required
def vendor_dashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    
    if not vendor.is_approved:
        return redirect("not_approved")  

    
    food_items = vendor.food_items.all()  

    context = {
        "vendor": vendor,
        "food_items": food_items,  
    }
    return render(request, "dashboard.html", context)


from django.db.models import Q

from django.contrib import messages


from users.models import user_tbl

def view_food_items(request):
    query = request.GET.get("q", "")  
    pnr_or_train = request.GET.get("pnr_or_train", "")  
    selected_station = request.GET.get("station", "")  
    stations = []

    
    if pnr_or_train:
        try:
            
            train_route = TrainRoute.objects.get(train_number=pnr_or_train)
            stations = train_route.stations  # List of stations
        except TrainRoute.DoesNotExist:
            pass  # Handle invalid PNR/train number gracefully


    food_items = FoodItem.objects.filter(vendor__is_approved=True)

    if query:
        food_items = food_items.filter(name__icontains=query)
    if selected_station:
        food_items = food_items.filter(railway_station=selected_station)

    context = {
        "food_items": food_items,
        "query": query,
        "pnr_or_train": pnr_or_train,
        "stations": stations,
        "selected_station": selected_station,
    }
    return render(request, "view_food_items.html", context)
def add_to_cart(request, food_item_id):
    if 'idl' not in request.session:
        return redirect('login')  # Redirect to login if user is not logged in
    
    user_id = request.session['idl']
    print(f"Logged-in User ID: {user_id}")  # Debugging
    
    user = get_object_or_404(user_tbl, id=user_id)
    food_item = get_object_or_404(FoodItem, id=food_item_id)
    
    # Ensure cart is unique for each user
    cart, created = Cart.objects.get_or_create(user=user)
    
    # Check if the item already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

def view_cart(request):
    if 'idl' not in request.session:
        return redirect('login')

    user_id = request.session['idl']
    print(f"Fetching Cart for User ID: {user_id}")  # Debugging

    user = get_object_or_404(user_tbl, id=user_id)
    
    # Fetch only the logged-in user's cart
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cart_items.all()
    
    total_price = sum(item.food_item.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'view_cart.html', context)

def remove_from_cart(request, cart_item_id):
    if 'idl' not in request.session:
        return redirect('login')
    
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    
    return redirect('view_cart')

from . models import Ordering, OrderItem
def checkout(request):
    if 'idl' not in request.session:
        return redirect('login')
    
    user_id = request.session['idl']
    user = get_object_or_404(user_tbl, id=user_id)
    cart = get_object_or_404(Cart, user=user)
    cart_items = cart.cart_items.all()
    
    if not cart_items:
        return redirect('view_cart')
    
    total_price = sum(item.food_item.price * item.quantity for item in cart_items)
    
    # Create Order
    order = Ordering.objects.create(user=user, total_price=total_price, status="Pending")
    for item in cart_items:
        OrderItem.objects.create(order=order, food_item=item.food_item, quantity=item.quantity)
    
    cart.cart_items.all().delete()  # Clear the cart after checkout
    return redirect('payment', order_id=order.id)

# Dummy Payment
def payment(request, order_id):
    order = get_object_or_404(Ordering, id=order_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order.payment_method = payment_method
        
        if payment_method in ["Credit Card", "Debit Card"]:
            order.card_number = request.POST.get('card_number')
            order.expiry_date = request.POST.get('expiry_date')
            order.cvv = request.POST.get('cvv')
        
        order.status = "Completed"
        order.save()
        return redirect('order_success', order_id=order.id)
    return render(request, 'payment.html', {'order': order})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ordering, Feedback
from django.contrib import messages

def order_success(request, order_id):
    order = get_object_or_404(Ordering, id=order_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating:  # Ensure rating is provided
            Feedback.objects.create(user=order.user, order=order, rating=int(rating), comment=comment)
            messages.success(request, "Thank you for your feedback!")
            return redirect("view_cart")  # Redirect to another page after submission
    
    
    return render(request, "order_success.html", {"order": order})
