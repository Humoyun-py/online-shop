/* ============================================================
   KarmaShop - Asosiy JavaScript
   Savat boshqaruvi va foydalanuvchi interfeysi
   ============================================================ */

$(document).ready(function () {

    // ============================================================
    // SAVAT MIQDORI +/- BOSHQARUVI
    // ============================================================
    $(document).on('click', '.qty-plus', function () {
        var input = $(this).closest('.input-group').find('.qty-input');
        var val = parseInt(input.val()) || 1;
        var max = parseInt(input.attr('max')) || 999;
        if (val < max) {
            input.val(val + 1);
            input.trigger('change');
        }
    });

    $(document).on('click', '.qty-minus', function () {
        var input = $(this).closest('.input-group').find('.qty-input');
        var val = parseInt(input.val()) || 1;
        if (val > 0) {
            input.val(val - 1);
            input.trigger('change');
        }
    });

    // ============================================================
    // SAVATGA QO'SHISH (AJAX) - Kelajak uchun tayyor
    // ============================================================
    $(document).on('click', '.add-to-cart-ajax', function (e) {
        e.preventDefault();
        var url = $(this).data('url');
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: url,
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            success: function (data) {
                if (data.success) {
                    // Savat sonini yangilash
                    $('.cart-badge').text(data.cart_count);
                    showNotification('Mahsulot savatga qo\'shildi!', 'success');
                }
            },
            error: function () {
                showNotification('Xatolik yuz berdi!', 'error');
            }
        });
    });

    // ============================================================
    // MAHSULOTNI YOQTIRISH (AJAX)
    // ============================================================
    $(document).on('click', '#like-btn', function (e) {
        e.preventDefault();
        var btn = $(this);
        var url = btn.attr('href');

        $.ajax({
            url: url,
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function (data) {
                if (data.liked) {
                    btn.removeClass('btn-outline-danger').addClass('btn-danger');
                    showNotification('Yoqtirganlar ro\'yxatiga qo\'shildi!', 'success');
                } else {
                    btn.removeClass('btn-danger').addClass('btn-outline-danger');
                    showNotification('Yoqtirganlar ro\'yxatidan olib tashlandi.', 'info');
                }
                $('#like-count').text(data.count);
            }
        });
    });

    // ============================================================
    // BILDIRISHNOMA KO'RSATISH
    // ============================================================
    function showNotification(message, type) {
        var alertClass = type === 'success' ? 'alert-success' : (type === 'error' ? 'alert-danger' : 'alert-info');

        var notification = $('<div class="alert ' + alertClass + ' alert-dismissible fade show shop-notification" role="alert">' +
            message +
            '<button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>' +
            '</div>');

        // Agar konteyner yo'q bo'lsa yaratamiz
        if ($('#notification-container').length === 0) {
            $('body').append('<div id="notification-container" style="position:fixed;top:80px;right:20px;z-index:9999;width:300px;"></div>');
        }

        $('#notification-container').append(notification);

        // 3 soniyadan keyin o'chirish
        setTimeout(function () {
            notification.alert('close');
        }, 3000);
    }

    // ============================================================
    // O'CHIRISH TASDIQLASH
    // ============================================================
    $(document).on('click', '.delete-confirm', function (e) {
        if (!confirm('Haqiqatan ham o\'chirishni xohlaysizmi?')) {
            e.preventDefault();
        }
    });

    // ============================================================
    // FORMA TEKSHIRISH - CHECKOUT
    // ============================================================
    $('#checkout-form').on('submit', function (e) {
        var phoneRegex = /^[\+]?[0-9\s\-]{9,15}$/;
        var phone = $('#phone_number').val();

        if (!phoneRegex.test(phone)) {
            e.preventDefault();
            alert('Iltimos, to\'g\'ri telefon raqam kiriting!');
            $('#phone_number').focus();
            return false;
        }
    });

    // ============================================================
    // SEARCH - INPUT TOZALASH TUGMASI
    // ============================================================
    $('#close_search').on('click', function () {
        $('#search_input_box').removeClass('open');
    });

    // ============================================================
    // SAVAT JADVAL - NARXNI DINAMIK HISOBLASH
    // ============================================================
    function updateCartRow(row) {
        var price = parseFloat(row.find('.item-price').data('price'));
        var qty = parseInt(row.find('.qty-input').val()) || 1;
        var subtotal = price * qty;
        row.find('.item-subtotal').text(formatPrice(subtotal) + ' so\'m');
        updateCartTotal();
    }

    function updateCartTotal() {
        var total = 0;
        $('.item-subtotal').each(function () {
            var text = $(this).text().replace(/[^0-9.]/g, '');
            total += parseFloat(text) || 0;
        });
        $('.cart-total').text(formatPrice(total) + ' so\'m');
    }

    function formatPrice(price) {
        return Math.round(price).toLocaleString('uz-UZ');
    }

    $(document).on('change', '.qty-input', function () {
        var row = $(this).closest('tr');
        updateCartRow(row);
    });

});
