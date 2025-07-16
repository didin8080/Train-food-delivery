from django.contrib import admin
from . models import Order, Vendor,TrainRoute,Cart,CartItem,OrderItem,Ordering,Feedback,FoodItem
# Register your models here.
admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(TrainRoute)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Ordering)
admin.site.register(FoodItem)
admin.site.register(Feedback)