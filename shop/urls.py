from django.urls import path
from . import views

# URL yo'naltirishlari
urlpatterns = [
    # Bosh sahifa
    path('', views.home_page, name='home'),

    # Mahsulotlar sahifasi
    path('mahsulotlar/', views.products_list, name='products'),

    # Mahsulot tafsilotlari
    path('mahsulot/<int:pk>/', views.product_detail, name='product_detail'),

    # Kategoriya mahsulotlari
    path('kategoriya/<int:pk>/', views.category_products, name='category_products'),

    # Mahsulotga izoh qo'shish
    path('mahsulot/<int:pk>/izoh/', views.add_comment, name='add_comment'),

    # Mahsulotni yoqtirish
    path('mahsulot/<int:pk>/yoqtirish/', views.like_product, name='like_product'),

    # Savatga qo'shish
    path('savat/qoshish/<int:pk>/', views.add_to_cart, name='add_to_cart'),

    # Savatdan o'chirish
    path('savat/ochirish/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Savat miqdorini yangilash
    path('savat/yangilash/<int:item_id>/', views.update_cart, name='update_cart'),

    # Savat ko'rish
    path('savat/', views.cart_view, name='cart'),

    # Buyurtma berish
    path('buyurtma/', views.checkout, name='checkout'),

    # Buyurtma tasdiqlash
    path('tasdiqlash/<int:order_id>/', views.confirmation, name='confirmation'),

    # Login
    path('kirish/', views.login_page, name='login'),

    # Logout
    path('chiqish/', views.logout_view, name='logout'),

    # Ro'yxatdan o'tish
    path('royxat/', views.register_page, name='register'),
]
