from django.db import models
from django.contrib.auth.models import User

# Kategoriya modeli
class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nomi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.title


# Mahsulot modeli
class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name="Nomi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Kategoriya")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    image = models.ImageField(upload_to='products/', verbose_name="Rasm", blank=True, null=True)
    description = models.TextField(verbose_name="Tavsif", blank=True)
    short_description = models.CharField(max_length=500, verbose_name="Qisqa tavsif", blank=True)
    quantity = models.PositiveIntegerField(default=0, verbose_name="Miqdori")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# Mahsulot xususiyatlari modeli
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications', verbose_name="Mahsulot")
    specification = models.CharField(max_length=500, verbose_name="Xususiyat")

    class Meta:
        verbose_name = "Mahsulot xususiyati"
        verbose_name_plural = "Mahsulot xususiyatlari"

    def __str__(self):
        return f"{self.product.title} - {self.specification}"


# Mahsulot yoqtirish modeli
class ProductLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_likes', verbose_name="Foydalanuvchi")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes', verbose_name="Mahsulot")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Mahsulot yoqtirish"
        verbose_name_plural = "Mahsulot yoqtirishlar"
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


# Izoh modeli
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Foydalanuvchi")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="Mahsulot")
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


# Izoh yoqtirish modeli
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes', verbose_name="Foydalanuvchi")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Izoh yoqtirish"
        verbose_name_plural = "Izoh yoqtirishlar"
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} - izoh yoqtirdi"


# Savat modeli
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Foydalanuvchi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Savat"
        verbose_name_plural = "Savatlar"

    def __str__(self):
        return f"{self.user.username} savati"

    def total_price(self):
        """Savat umumiy narxi"""
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        """Savat umumiy mahsulot soni"""
        return sum(item.quantity for item in self.items.all())


# Savat mahsuloti modeli
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Savat")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdori")

    class Meta:
        verbose_name = "Savat mahsuloti"
        verbose_name_plural = "Savat mahsulotlari"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def subtotal(self):
        """Mahsulot subtotali"""
        return self.product.price * self.quantity


# Buyurtma modeli
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('shipped', 'Yuborildi'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Foydalanuvchi", null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    country = models.CharField(max_length=100, verbose_name="Mamlakat", default="O'zbekiston")
    city = models.CharField(max_length=100, verbose_name="Shahar")
    district = models.CharField(max_length=100, verbose_name="Tuman", blank=True)
    address_line1 = models.CharField(max_length=200, verbose_name="Manzil (1-qator)")
    address_line2 = models.CharField(max_length=200, verbose_name="Manzil (2-qator)", blank=True)
    postcode = models.CharField(max_length=20, verbose_name="Pochta indeksi", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.pk} - {self.first_name} {self.last_name}"

    def total_price(self):
        """Buyurtma umumiy narxi"""
        return sum(item.subtotal() for item in self.order_items.all())


# Buyurtma mahsuloti modeli
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Buyurtma")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    quantity = models.PositiveIntegerField(verbose_name="Miqdori")

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def subtotal(self):
        """Mahsulot subtotali"""
        return self.price * self.quantity
