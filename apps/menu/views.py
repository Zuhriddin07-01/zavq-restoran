from django.shortcuts import render
from rest_framework import viewsets
from .models import MenuItem, Category
from .serializers import CategorySerializer, MenuItemSerializer


def menu_list(request):
    categories = Category.objects.all()
    items = MenuItem.objects.filter(is_available=True)
    return render(request, 'menu/menu_list.html', {'menu': items, 'categories': categories})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'preparation_time']
            


# Create your views here.
