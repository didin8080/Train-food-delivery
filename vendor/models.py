from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from users.models import user_tbl

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.JSONField()  # Storing order items
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by_admin = models.BooleanField(default=False)


class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="food_items")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    railway_station = models.CharField(max_length=255)  # Name of the railway station
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.vendor.business_name}"

    


class TrainRoute(models.Model):
    train_number = models.CharField(max_length=10, unique=True)
    stations = models.JSONField()  # List of station names in order

    def __str__(self):
        return f"Train {self.train_number}"
    

class Cart(models.Model):
    user = models.OneToOneField(user_tbl, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.fname}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)



class Ordering(models.Model):
    user = models.ForeignKey(user_tbl, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Cancelled", "Cancelled")], default="Pending")
    payment_method = models.CharField(max_length=50, choices=[("Credit Card", "Credit Card"), ("Debit Card", "Debit Card"), ("Cash on Delivery", "Cash on Delivery")], default="Cash on Delivery")
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)
    cvv = models.CharField(max_length=3, blank=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Ordering, on_delete=models.CASCADE, related_name="order_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



class Feedback(models.Model):
    user = models.ForeignKey(user_tbl, on_delete=models.CASCADE)
    order = models.ForeignKey(Ordering, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user} - {self.rating} Stars"


