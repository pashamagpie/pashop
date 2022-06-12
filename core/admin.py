from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext

from core import models


class CustomUserAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (gettext('Personal Info'), {'fields': ('name',)}),
        (
            gettext('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (gettext('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'is_available')
    prepopulated_fields = {'slug': ('name',)}


class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'is_active')
    list_editable = ('is_active',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart)
admin.site.register(models.CartItem, CartItemAdmin)
admin.site.register(models.ProductVariation, ProductVariationAdmin)
