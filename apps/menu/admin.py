from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)   # <-- "seach_fields" emas, "search_fields"


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'is_available')  # <-- image_preview qo'shildi
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

    # ✅ RASMNI ADMIN PANELDA KO'RSATISH
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="border-radius:6px; object-fit:cover;" />',
                obj.image.url
            )
        return "❌ Rasm yo'q"
    image_preview.short_description = 'Rasm'









# Register your models here.
