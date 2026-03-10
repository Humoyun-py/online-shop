from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import (
    Category, Product, ProductSpecification, ProductLike,
    Comment, CommentLike, Cart, CartItem, Order, OrderItem
)


# ============================================================
# YO'RDAMCHI FUNKSIYA: Savat ma'lumotlarini olish
# ============================================================
def get_cart_data(request):
    """Sessiya yoki foydalanuvchi asosida savat ma'lumotlarini qaytaradi"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    return None


# ============================================================
# BOSH SAHIFA
# ============================================================
def home_page(request):
    """Bosh sahifa - so'nggi mahsulotlar va kategoriyalar"""
    categories = Category.objects.all()
    latest_products = Product.objects.filter(quantity__gt=0).order_by('-created_at')[:8]
    featured_products = Product.objects.filter(quantity__gt=0)[:4]

    cart = get_cart_data(request)
    cart_count = cart.total_items() if cart else 0

    context = {
        'categories': categories,
        'latest_products': latest_products,
        'featured_products': featured_products,
        'cart_count': cart_count,
    }
    return render(request, 'index.html', context)


# ============================================================
# MAHSULOTLAR RO'YXATI (SHOP SAHIFASI)
# ============================================================
def products_list(request):
    """Barcha mahsulotlar ro'yxati, qidiruv va filtr bilan"""
    categories = Category.objects.all()
    products = Product.objects.filter(quantity__gt=0)

    # Qidiruv
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        )

    # Narx filtr
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    cart = get_cart_data(request)
    cart_count = cart.total_items() if cart else 0

    context = {
        'categories': categories,
        'products': products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'cart_count': cart_count,
    }
    return render(request, 'shop.html', context)


# ============================================================
# MAHSULOT TAFSILOTLARI
# ============================================================
def product_detail(request, pk):
    """Mahsulot tafsilotlari sahifasi"""
    product = get_object_or_404(Product, pk=pk)
    specifications = product.specifications.all()
    comments = product.comments.all().order_by('-created_at')
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:4]

    # Yoqtirganmi tekshirish
    is_liked = False
    if request.user.is_authenticated:
        is_liked = ProductLike.objects.filter(user=request.user, product=product).exists()

    categories = Category.objects.all()
    cart = get_cart_data(request)
    cart_count = cart.total_items() if cart else 0

    context = {
        'product': product,
        'specifications': specifications,
        'comments': comments,
        'related_products': related_products,
        'is_liked': is_liked,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'single-product.html', context)


# ============================================================
# KATEGORIYA BO'YICHA MAHSULOTLAR
# ============================================================
def category_products(request, pk):
    """Kategoriya bo'yicha mahsulotlar sahifasi"""
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category, quantity__gt=0)
    categories = Category.objects.all()

    cart = get_cart_data(request)
    cart_count = cart.total_items() if cart else 0

    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'category.html', context)


# ============================================================
# IZOH QO'SHISH
# ============================================================
@login_required
@require_POST
def add_comment(request, pk):
    """Mahsulotga izoh qo'shish"""
    product = get_object_or_404(Product, pk=pk)
    comment_text = request.POST.get('comment', '').strip()

    if comment_text:
        Comment.objects.create(
            user=request.user,
            product=product,
            comment=comment_text
        )
        messages.success(request, "Izohingiz muvaffaqiyatli qo'shildi!")
    else:
        messages.error(request, "Izoh bo'sh bo'lishi mumkin emas!")

    return redirect('product_detail', pk=pk)


# ============================================================
# MAHSULOTNI YOQTIRISH
# ============================================================
@login_required
def like_product(request, pk):
    """Mahsulotni yoqtirish / yoqtirmaslik"""
    product = get_object_or_404(Product, pk=pk)
    like, created = ProductLike.objects.get_or_create(user=request.user, product=product)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = product.likes.count()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': like_count})

    return redirect('product_detail', pk=pk)


# ============================================================
# SAVATGA QO'SHISH
# ============================================================
@login_required
def add_to_cart(request, pk):
    """Mahsulotni savatga qo'shish"""
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        if cart_item.quantity < product.quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"'{product.title}' savatingizda yangilandi!")
        else:
            messages.warning(request, "Mahsulot yetarli miqdorda mavjud emas!")
    else:
        messages.success(request, f"'{product.title}' savatga qo'shildi!")

    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


# ============================================================
# SAVATDAN O'CHIRISH
# ============================================================
@login_required
def remove_from_cart(request, item_id):
    """Mahsulotni savatdan o'chirish"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = cart_item.product.title
    cart_item.delete()
    messages.success(request, f"'{product_name}' savatdan o'chirildi!")
    return redirect('cart')


# ============================================================
# SAVAT MIQDORINI YANGILASH
# ============================================================
@login_required
@require_POST
def update_cart(request, item_id):
    """Savat mahsulot miqdorini yangilash"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0 and quantity <= cart_item.product.quantity:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Savat yangilandi!")
    elif quantity <= 0:
        cart_item.delete()
        messages.success(request, "Mahsulot savatdan o'chirildi!")
    else:
        messages.warning(request, "Yetarli miqdor mavjud emas!")

    return redirect('cart')


# ============================================================
# SAVAT KO'RISH
# ============================================================
@login_required
def cart_view(request):
    """Savat sahifasi"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    categories = Category.objects.all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'categories': categories,
        'cart_count': cart.total_items(),
    }
    return render(request, 'cart.html', context)


# ============================================================
# BUYURTMA BERISH (CHECKOUT)
# ============================================================
@login_required
def checkout(request):
    """Buyurtma berish sahifasi"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    categories = Category.objects.all()

    if not cart_items:
        messages.warning(request, "Savatingiz bo'sh! Avval mahsulot qo'shing.")
        return redirect('cart')

    if request.method == 'POST':
        # Forma ma'lumotlarini olish
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        country = request.POST.get('country', "O'zbekiston").strip()
        city = request.POST.get('city', '').strip()
        district = request.POST.get('district', '').strip()
        address_line1 = request.POST.get('address_line1', '').strip()
        address_line2 = request.POST.get('address_line2', '').strip()
        postcode = request.POST.get('postcode', '').strip()

        # Majburiy maydonlarni tekshirish
        if not all([first_name, last_name, phone_number, city, address_line1]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
        else:
            # Buyurtma yaratish
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                country=country,
                city=city,
                district=district,
                address_line1=address_line1,
                address_line2=address_line2,
                postcode=postcode,
            )

            # Buyurtma mahsulotlarini yaratish
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                # Mahsulot miqdorini kamaytirish
                item.product.quantity -= item.quantity
                item.product.save()

            # Savatni tozalash
            cart.items.all().delete()

            messages.success(request, f"Buyurtmangiz #{order.pk} muvaffaqiyatli qabul qilindi!")
            return redirect('confirmation', order_id=order.pk)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'categories': categories,
        'cart_count': cart.total_items(),
    }
    return render(request, 'checkout.html', context)


# ============================================================
# BUYURTMA TASDIQLASH
# ============================================================
@login_required
def confirmation(request, order_id):
    """Buyurtma tasdiqlash sahifasi"""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order_items = order.order_items.select_related('product').all()
    categories = Category.objects.all()

    cart = get_cart_data(request)
    cart_count = cart.total_items() if cart else 0

    context = {
        'order': order,
        'order_items': order_items,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'confirmation.html', context)


# ============================================================
# LOGIN SAHIFASI
# ============================================================
def login_page(request):
    """Login sahifasi"""
    from django.contrib.auth import authenticate, login, logout

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name or user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri!")

    categories = Category.objects.all()
    return render(request, 'login.html', {'categories': categories, 'cart_count': 0})


# ============================================================
# LOGOUT
# ============================================================
def logout_view(request):
    """Tizimdan chiqish"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect('home')


# ============================================================
# RO'YXATDAN O'TISH
# ============================================================
def register_page(request):
    """Ro'yxatdan o'tish sahifasi"""
    from django.contrib.auth import login
    from django.contrib.auth.models import User

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 != password2:
            messages.error(request, "Parollar mos kelmadi!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud!")
        elif len(password1) < 6:
            messages.error(request, "Parol kamida 6 ta belgidan iborat bo'lishi kerak!")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {first_name or username}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('home')

    categories = Category.objects.all()
    return render(request, 'register.html', {'categories': categories, 'cart_count': 0})
