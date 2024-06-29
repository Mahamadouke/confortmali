from django.contrib import admin
from .models import Categorie, Shop, Contact, Cart, CartItem, Order

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'categorie', 'price', 'quantity_stock')
    search_fields = ('name', 'description')
    list_filter = ('categorie',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'message')
    search_fields = ('first_name', 'last_name', 'email', 'message')

admin.site.register(Categorie, CategorieAdmin)  
admin.site.register(Shop, ShopAdmin)
admin.site.register(Contact, ContactAdmin)     

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'quantity', 'total_price', 'customer_name', 'payment_status')
    search_fields = ('customer_name', 'customer_phone', 'user__username')
    list_filter = ('payment_status', 'shop')
    readonly_fields = ('total_price',)

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)