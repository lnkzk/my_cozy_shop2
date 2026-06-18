import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Min, Max
from django.contrib import messages
from .models import (Category, Product, MainBanner, CategoryBlockSettings, PromoBanner,
                     FeaturedProductsSettings, HeaderSettings, HeaderNavigation, FooterSettings,
                     Purpose, Color, WorkingSchedule, Courier, CourierSchedule, DeliveryMethod, PaymentMethod,
                     OrderFormField, Order)
from .cart import Cart


def get_common_context(request):
    return {
        'header_settings': HeaderSettings.objects.first(),
        'header_menu': HeaderNavigation.objects.all(),
        'footer_settings': FooterSettings.objects.first(),
        'cart': Cart(request),
    }


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    main_banner = MainBanner.objects.filter(is_active=True).first()
    category_block_settings = CategoryBlockSettings.objects.first()
    featured_categories = Category.objects.filter(is_featured=True)
    promo_banner = PromoBanner.objects.filter(is_active=True).first()
    featured_section = FeaturedProductsSettings.objects.first()
    featured_products = featured_section.products.filter(available=True) if featured_section else []
    context = get_common_context(request)
    context.update({'category': category, 'categories': categories, 'products': products, 'main_banner': main_banner,
                    'category_block_settings': category_block_settings, 'featured_categories': featured_categories,
                    'promo_banner': promo_banner, 'featured_section': featured_section,
                    'featured_products': featured_products})
    return render(request, 'shop/product/list.html', context)


def catalog_view(request):
    products = Product.objects.filter(available=True)
    price_bounds = products.aggregate(min_p=Min('price'), max_p=Max('price'))
    min_price_bound = int(price_bounds['min_p'] or 0)
    max_price_bound = int(price_bounds['max_p'] or 5000)
    selected_purposes = request.GET.getlist('purpose')
    selected_colors = request.GET.getlist('color')
    req_min_price = request.GET.get('min_price')
    req_max_price = request.GET.get('max_price')
    if selected_purposes: products = products.filter(purposes__id__in=selected_purposes).distinct()
    if selected_colors: products = products.filter(colors__id__in=selected_colors).distinct()
    current_min = int(req_min_price) if req_min_price else min_price_bound
    current_max = int(req_max_price) if req_max_price else max_price_bound
    products = products.filter(price__gte=current_min, price__lte=current_max)
    context = get_common_context(request)
    context.update({'products': products, 'purposes': Purpose.objects.all(), 'colors': Color.objects.all(),
                    'selected_purposes': [int(x) for x in selected_purposes],
                    'selected_colors': [int(x) for x in selected_colors], 'min_price_bound': min_price_bound,
                    'max_price_bound': max_price_bound, 'current_min': current_min, 'current_max': current_max})
    return render(request, 'shop/product/catalog.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = product.related_products.filter(available=True)[:5]
    context = get_common_context(request)
    context.update({'product': product, 'related_products': related_products})
    return render(request, 'shop/product/detail.html', context)


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    override_quantity = request.POST.get('override_quantity') == 'true'
    is_ajax_form = request.POST.get('is_ajax') == 'true' or request.headers.get(
        'x-requested-with') == 'XMLHttpRequest' or 'HTTP_X_CSRFTOKEN' in request.META
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
    cart.add(product=product, quantity=quantity, override_quantity=override_quantity)
    if is_ajax_form:
        return JsonResponse(
            {'status': 'success', 'cart_total_price': str(cart.get_total_price()), 'cart_len': len(cart)})
    messages.success(request, 'Товар добавлен в корзину')
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(
            {'status': 'success', 'cart_total_price': str(cart.get_total_price()), 'cart_len': len(cart)})
    return redirect('shop:cart_detail')


def cart_detail(request):
    context = get_common_context(request)
    return render(request, 'shop/product/cart_detail.html', context)


# --- УМНЫЙ АВТОМАТИЧЕСКИЙ МУЛЬТИ-КУРЬЕРСКИЙ РАСЧЕТ ДАТ ---
def calculate_delivery_dates():
    now = datetime.datetime.now()
    current_time = now.time()

    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
              "декабря"]
    days_ru = ["в понедельник", "во вторник", "в среду", "в четверг", "в пятницу", "в субботу", "в воскресенье"]

    def format_date_string(dt, is_today, is_tomorrow):
        if is_today:
            return f"Сегодня, {dt.day} {months[dt.month - 1]}"
        elif is_tomorrow:
            return f"Завтра, {dt.day} {months[dt.month - 1]}"
        else:
            return f"{days_ru[dt.weekday()].capitalize()}, {dt.day} {months[dt.month - 1]}"

    # 1. Считаем Самовывоз (по графику магазина WorkingSchedule)
    shop_sched_map = {s.day_of_week: s for s in WorkingSchedule.objects.all()}
    pickup_date_str = "В рабочий день магазина"
    for i in range(7):
        check_date = now + datetime.timedelta(days=i)
        day_sched = shop_sched_map.get(check_date.weekday())
        if day_sched and day_sched.is_working:
            if i == 0 and current_time >= day_sched.work_to: continue
            pickup_date_str = format_date_string(check_date, is_today=(i == 0), is_tomorrow=(i == 1))
            break

    # 2. Считаем Курьерскую доставку (по сменам всех активных курьеров CourierSchedule)
    courier_date_str = "В ближайший день доставки"

    # Ищем по дням вперед
    for i in range(7):
        check_date = now + datetime.timedelta(days=i)
        day_num = check_date.weekday()

        # Получаем все смены курьеров на этот день недели
        active_schedules = CourierSchedule.objects.filter(
            courier__is_active=True,
            day_of_week=day_num,
            is_working=True
        )

        day_has_available_courier = False
        for sched in active_schedules:
            if i == 0:
                # Если проверяем «сегодня», курьер должен работать и время заказа должно быть ДО отсечки
                if current_time < sched.courier_cutoff_time and current_time < sched.work_to:
                    day_has_available_courier = True
                    break
            else:
                # На будущие дни достаточно факта, что курьер работает в этот день
                day_has_available_courier = True
                break

        if day_has_available_courier:
            courier_date_str = format_date_string(check_date, is_today=(i == 0), is_tomorrow=(i == 1))
            break

    return {'pickup_date': pickup_date_str, 'courier_date': courier_date_str}


def order_create(request):
    cart = Cart(request)
    fields = OrderFormField.objects.all().order_by('sort_order')
    delivery_methods = DeliveryMethod.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    calculated_dates = calculate_delivery_dates()

    if request.method == 'POST':
        chosen_delivery_id = request.POST.get('delivery_method')
        chosen_payment_slug = request.POST.get('payment_method')

        delivery = get_object_or_404(DeliveryMethod, id=chosen_delivery_id)
        payment = get_object_or_404(PaymentMethod, slug=chosen_payment_slug)

        extracted_form_data = {}
        errors = []
        for field in fields:
            val = request.POST.get(field.field_name, '').strip()
            if field.is_required and not val:
                errors.append(f"Поле «{field.label}» обязательно к заполнению.")
            extracted_form_data[field.field_name] = val

        if not errors:
            items_text = ""
            for item in cart:
                items_text += f"{item['product'].name} x {item['quantity']}; "

            final_total = cart.get_total_price() + delivery.price
            saved_delivery_title = f"{delivery.title} ("
            if delivery.method_type == 'pickup':
                saved_delivery_title += calculated_dates['pickup_date']
            else:
                saved_delivery_title += calculated_dates['courier_date']
            saved_delivery_title += ")"

            order = Order.objects.create(
                delivery_method=saved_delivery_title,
                payment_method=payment.title,
                delivery_price=delivery.price,
                total_price=final_total,
                items_summary=items_text,
                form_data=extracted_form_data
            )
            cart.clear()
            context = get_common_context(request)
            context.update({'order': order})
            return render(request, 'shop/product/created.html', context)
        else:
            for err in errors: messages.error(request, err)

    context = get_common_context(request)
    context.update({
        'fields_address': fields.filter(section='address'),
        'fields_recipient': fields.filter(section='recipient'),
        'delivery_methods': delivery_methods,
        'payment_methods': payment_methods,
        'calculated_dates': calculated_dates,
    })
    return render(request, 'shop/product/order_form.html', context)