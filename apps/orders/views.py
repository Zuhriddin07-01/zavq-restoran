from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.menu.models import MenuItem
from .models import Order, OrderItem
from rest_framework import viewsets
from .serializers import OrderSerializer, OrderItemSerializer
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity'))
        menu_item = get_object_or_404(MenuItem, id=item_id)

        order, created = Order.objects.get_or_create(
            user=request.user,
            status='pending',
        )

        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={'quantity': quantity, 'price_at_order': menu_item.price}
        )

        if not item_created:
            order_item.quantity += quantity
            order_item.save()

        return redirect('cart')

    return redirect('menu')


@login_required
def cart_view(request):
    cart = Order.objects.filter(user=request.user, status='pending').first()
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
def checkout(request):
    cart = get_object_or_404(Order, user=request.user, status='pending')

    if request.method == 'POST':
        cart.status = 'confirmed'
        cart.save()
        return redirect('cart')

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).exclude(status='pending')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def update_cart_item(request, item_id, action):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)

    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

    return redirect('cart')



def is_staff_user(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff_user)
def staff_orders(request):
    orders = Order.objects.exclude(status__in=['pending', 'delivered', 'cancelled'])
    return render(request, 'orders/staff_orders.html', {'orders': orders})


@login_required
@user_passes_test(is_staff_user)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    order.status = new_status
    order.save()
    return redirect('staff_orders')



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['status']
    search_fields = ['delivery_address', 'phone_number']
    ordering_fields = ['created_at']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer





# Create your views here.
