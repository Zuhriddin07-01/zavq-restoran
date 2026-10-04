from django.contrib import admin
from .models import Order, OrderItem

class OrderIteamInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'delivery_address', 'phone_number')
    inlines = [OrderIteamInline]


# Register your models here.
