from django.contrib import admin
from .models import (
    Category, Product, ProductSpecification, ProductLike,
    Comment, CommentLike, Cart, CartItem, Order, OrderItem
)


# Mahsulot xususiyatlari inline
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


# Buyurtma mahsulotlari inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')


# Savat mahsulotlari inline
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# Kategoriya admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    ordering = ('-created_at',)


# Mahsulot admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'quantity', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    list_editable = ('price', 'quantity')
    inlines = [ProductSpecificationInline]
    ordering = ('-created_at',)


# Izoh admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')
    list_filter = ('product',)
    search_fields = ('comment', 'user__username')
    ordering = ('-created_at',)


# Savat admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]


# Buyurtma admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'city', 'status', 'created_at')
    list_display_links = ('id', 'first_name')
    list_filter = ('status', 'city')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    ordering = ('-created_at',)


# Mahsulot yoqtirish admin
@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')
    list_filter = ('product',)
