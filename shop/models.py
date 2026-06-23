import openpyxl
from decimal import Decimal
from django.db import models
from django.urls import reverse


# ==============================================================================
# БАЗОВЫЕ МОДЕЛИ КАТАЛОГА ТОВАРОВ
# ==============================================================================

class Category(models.Model):
    name = models.CharField('Название категории', max_length=200, db_index=True)
    slug = models.SlugField('URL-адрес (ссылка)', max_length=200, unique=True)
    image = models.ImageField('Фото категории', upload_to='categories/', blank=True, null=True)
    icon_image = models.ImageField('Иконка категории', upload_to='categories/icons/', blank=True, null=True)
    icon_position = models.IntegerField('Центровка иконки (%)', default=50)
    is_featured = models.BooleanField('Выводить на главную?', default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField('Назначение', max_length=100)

    class Meta: verbose_name = 'Назначение'; verbose_name_plural = 'Справочник: Назначения'

    def __str__(self): return self.name


class Color(models.Model):
    name = models.CharField('Название цвета', max_length=100)

    class Meta: verbose_name = 'Цвет'; verbose_name_plural = 'Справочник: Цвета'

    def __str__(self): return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField('Название товара', max_length=200, db_index=True)
    sku = models.CharField('Артикул', max_length=50, blank=True, null=True, unique=True, db_index=True)
    slug = models.SlugField('URL-адрес', max_length=200, db_index=True)
    image = models.ImageField('Главное фото', upload_to='products/%Y/%m/%d', blank=True)
    image_position = models.IntegerField('Центровка фото (%)', default=50)
    description = models.TextField('Описание', blank=True)

    price = models.DecimalField('Цена продажи (руб.)', max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField('Закупочная цена (руб.)', max_digits=10, decimal_places=2, default=0.00)
    supplier_shipping_cost = models.DecimalField('Доставка от поставщика (руб.)', max_digits=10, decimal_places=2,
                                                 default=0.00)

    stock = models.PositiveIntegerField('Остаток на складе', default=0)
    available = models.BooleanField('В наличии (Активен)', default=True)
    purposes = models.ManyToManyField(Purpose, blank=True, verbose_name="Назначения")
    colors = models.ManyToManyField(Color, blank=True, verbose_name="Цвета")
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to',
                                              verbose_name='Похожие товары')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"[{self.sku}] {self.name}" if self.sku else self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images', verbose_name="Товар")
    image = models.ImageField('Дополнительное фото', upload_to='products/gallery/%Y/%m/%d')
    image_position = models.IntegerField('Центровка фото (%)', default=50)
    is_active = models.BooleanField('Отображать', default=True)

    class Meta: verbose_name = 'Дополнительное фото'; verbose_name_plural = 'Галерея товара'

    def __str__(self): return f"Фото для {self.product.name}"


# ==============================================================================
# НАСТРОЙКИ САЙТА (БАННЕРЫ И БЛОКИ)
# ==============================================================================
class MainBanner(models.Model):
    banner_size = models.CharField('Размер', max_length=20,
                                   choices=[('small', 'Узкий'), ('medium', 'Средний'), ('large', 'Широкий')],
                                   default='medium')
    sub_title = models.CharField('Надзаголовок', max_length=100, blank=True)
    title = models.CharField('Главный заголовок', max_length=200)
    description = models.TextField('Описание', blank=True)
    button_text = models.CharField('Текст на кнопке', max_length=50, blank=True)
    button_link = models.CharField('Ссылка с кнопки', max_length=200, blank=True)
    image = models.ImageField('Фон', upload_to='banners/', blank=True, null=True)
    show_shipping_badge = models.BooleanField('Показывать плашку доставки?', default=True)
    shipping_title = models.CharField('Заголовок доставки', max_length=100, blank=True)
    shipping_subtitle = models.CharField('Подтекст доставки', max_length=100, blank=True)
    show_payment_badge = models.BooleanField('Показывать плашку оплаты?', default=True)
    payment_title = models.CharField('Заголовок оплаты', max_length=100, blank=True)
    payment_subtitle = models.CharField('Подтекст оплаты', max_length=100, blank=True)
    is_active = models.BooleanField('Включить баннер', default=True)

    class Meta: verbose_name = 'Главный баннер'; verbose_name_plural = 'Главные баннеры'


class CategoryBlockSettings(models.Model):
    block_title = models.CharField('Заголовок блока', max_length=200, default="Категории")
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Выберите категории для показа на Главной")
    block_size = models.CharField('Размер кружков', max_length=20,
                                  choices=[('small', 'Мелкие'), ('medium', 'Средние'), ('large', 'Крупные')],
                                  default='medium')
    block_padding = models.CharField('Отступы блока', max_length=20,
                                     choices=[('small', 'Маленькие'), ('medium', 'Средние'), ('large', 'Большие')],
                                     default='medium')
    browse_all_text = models.CharField('Текст ссылки', max_length=50, default="Все категории →")
    browse_all_link = models.CharField('Ссылка', max_length=200, default="/catalog/")

    class Meta: verbose_name = 'Блок категорий'; verbose_name_plural = 'Настройки блока категорий'


class PromoBanner(models.Model):
    banner_size = models.CharField('Размер', max_length=20,
                                   choices=[('small', 'Узкий'), ('medium', 'Средний'), ('large', 'Крупный')],
                                   default='medium')
    tag_text = models.CharField('Тег', max_length=100, blank=True)
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание', blank=True)
    button_text = models.CharField('Текст кнопки', max_length=50, blank=True)
    button_link = models.CharField('Ссылка кнопки', max_length=200, blank=True)
    badge_up_to_text = models.CharField('Верхний текст кружка', max_length=50, blank=True)
    badge_value_text = models.CharField('Цифра кружка', max_length=50, blank=True)
    badge_bottom_text = models.CharField('Нижний текст кружка', max_length=50, blank=True)
    image = models.ImageField('Фото баннера', upload_to='promo/', blank=True, null=True)
    is_active = models.BooleanField('Включен', default=True)

    class Meta: verbose_name = 'Промо-баннер (Акция)'; verbose_name_plural = 'Промо-баннеры (Акции)'


class FeaturedProductsSettings(models.Model):
    block_title = models.CharField('Заголовок блока', max_length=200, default="Топ продаж")
    view_all_text = models.CharField('Текст ссылки', max_length=50, default="Все товары →")
    view_all_link = models.CharField('Ссылка', max_length=200, default="/catalog/")
    cart_button_text = models.CharField('Текст кнопки корзины', max_length=50, default="Добавить в корзину")
    products = models.ManyToManyField(Product, blank=True, verbose_name="Товары")
    is_active = models.BooleanField('Показывать блок?', default=True)

    class Meta: verbose_name = 'Топ продаж'; verbose_name_plural = 'Настройки Топа продаж'


class HeaderSettings(models.Model):
    site_name = models.CharField('Название сайта', max_length=100, default="KÓTI")
    logo_icon = models.CharField('Символ логотипа', max_length=10, default="♥")
    admin_email = models.EmailField('Email для уведомлений', blank=True, null=True)

    class Meta: verbose_name = 'Настройки шапки (Лого и Email)'; verbose_name_plural = 'Настройки шапки (Лого и Email)'


class HeaderNavigation(models.Model):
    title = models.CharField('Пункт меню', max_length=100)
    link = models.CharField('Ссылка', max_length=200)

    class Meta: verbose_name = 'Ссылка главного меню'; verbose_name_plural = 'Ссылки главного меню'


class FooterSettings(models.Model):
    copyright_text = models.CharField('Копирайт', max_length=200, default="© 2026 KÓTI.")
    instagram_url = models.URLField('Instagram', blank=True, null=True)
    telegram_url = models.URLField('Telegram', blank=True, null=True)

    class Meta: verbose_name = 'Настройки подвала'; verbose_name_plural = 'Настройки подвала (соцсети)'


# ==============================================================================
# ЛОГИСТИКА И ЗАКАЗЫ
# ==============================================================================
class WorkingSchedule(models.Model):
    DAY_CHOICES = [(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'),
                   (6, 'Воскресенье')]
    day_of_week = models.IntegerField('День недели', choices=DAY_CHOICES, unique=True)
    is_working = models.BooleanField('Рабочий день?', default=True)
    work_from = models.TimeField('Открыто с', default="09:00")
    work_to = models.TimeField('Открыто до', default="21:00")

    class Meta: verbose_name = 'График шоурума'; verbose_name_plural = 'Логистика: График работы шоурума'; ordering = [
        'day_of_week']


class Courier(models.Model):
    name = models.CharField('Имя курьера / Служба', max_length=100)
    is_active = models.BooleanField('Активен', default=True)

    class Meta: verbose_name = 'Курьер'; verbose_name_plural = 'Логистика: Курьеры'

    def __str__(self): return self.name


class CourierSchedule(models.Model):
    DAY_CHOICES = [(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'),
                   (6, 'Воскресенье')]
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='schedules', verbose_name='Курьер')
    day_of_week = models.IntegerField('День недели', choices=DAY_CHOICES)
    is_working = models.BooleanField('Рабочий день', default=True)
    work_from = models.TimeField('Начало смены', default="10:00")
    work_to = models.TimeField('Конец смены', default="20:00")
    courier_cutoff_time = models.TimeField('Время отсечки', default="15:00")

    class Meta: verbose_name = 'Смена курьера'; verbose_name_plural = 'Смены курьеров'; unique_together = ('courier',
                                                                                                           'day_of_week'); ordering = [
        'courier', 'day_of_week']


class DeliveryMethod(models.Model):
    TYPE_CHOICES = [('pickup', 'Самовывоз'), ('courier', 'Доставка')]
    method_type = models.CharField('Тип расчета дат', max_length=10, choices=TYPE_CHOICES, unique=True)
    title = models.CharField('Название способа', max_length=100)
    price = models.DecimalField('Стоимость (руб.)', max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField('Активен', default=True)

    class Meta: verbose_name = 'Способ получения'; verbose_name_plural = 'Логистика: Способы получения'

    def __str__(self): return self.title


class PaymentMethod(models.Model):
    slug = models.SlugField('Системный код', max_length=50, unique=True)
    title = models.CharField('Название', max_length=100)
    is_active = models.BooleanField('Активен', default=True)

    class Meta: verbose_name = 'Способ оплаты'; verbose_name_plural = 'Логистика: Способы оплаты'

    def __str__(self): return self.title


class OrderFormField(models.Model):
    FIELD_TYPES = [('text', 'Текстовая строка'), ('tel', 'Телефон'), ('email', 'Email'),
                   ('textarea', 'Многострочный текст')]
    SECTION_CHOICES = [('address', 'Блок «Адрес»'), ('recipient', 'Блок «Данные получателя»')]
    label = models.CharField('Название поля (подсказка)', max_length=100)
    field_name = models.CharField('Системное имя', max_length=50, unique=True)
    field_type = models.CharField('Тип поля', max_length=15, choices=FIELD_TYPES, default='text')
    section = models.CharField('Блок', max_length=15, choices=SECTION_CHOICES, default='recipient')
    is_required = models.BooleanField('Обязательное?', default=True)
    sort_order = models.IntegerField('Порядок', default=0)

    class Meta: verbose_name = 'Поле формы заказа'; verbose_name_plural = 'Справочник: Поля формы заказа'; ordering = [
        'sort_order']

    def __str__(self): return self.label


class Order(models.Model):
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    order_source = models.CharField('Откуда заказ (Источник)', max_length=100, blank=True, null=True,
                                    help_text="Для ручных заказов впишите: Instagram, Шоурум и т.д. Если заказ с сайта, заполнится само.")
    delivery_method = models.CharField('Способ получения', max_length=150, default='Не указан', blank=True)
    payment_method = models.CharField('Способ оплаты', max_length=100, default='Не указан', blank=True)
    items_summary = models.TextField('Состав заказа (Список товаров)', help_text="Например: Свеча 'Ваниль' х 2 шт.")

    # ФИНАНСЫ (Разрешен пустой ввод)
    items_retail_price = models.DecimalField('Розничная цена товаров (Выручка)', max_digits=10, decimal_places=2,
                                             default=0.00, blank=True, null=True)
    items_purchase_price = models.DecimalField('Закупочная цена товаров', max_digits=10, decimal_places=2, default=0.00,
                                               blank=True, null=True)
    supplier_shipping_price = models.DecimalField('Доставка от поставщика', max_digits=10, decimal_places=2,
                                                  default=0.00, blank=True, null=True)
    delivery_price = models.DecimalField('Стоимость нашей доставки клиенту', max_digits=10, decimal_places=2,
                                         default=0.00, blank=True, null=True)

    # ИТОГИ
    cost_price = models.DecimalField('Общая себестоимость', max_digits=10, decimal_places=2, default=0.00, blank=True,
                                     null=True)
    total_price = models.DecimalField('Итоговая сумма (Чек)', max_digits=10, decimal_places=2, default=0.00, blank=True,
                                      null=True)
    gross_profit = models.DecimalField('Валовая прибыль (Чистыми)', max_digits=10, decimal_places=2, default=0.00,
                                       blank=True, null=True)

    form_data = models.JSONField('Заполненные данные клиента', default=dict, blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы клиентов'

    def __str__(self): return f"Заказ №{self.pk} от {self.created.strftime('%d.%m.%Y')}"


class OrderReport(Order):
    class Meta:
        proxy = True
        verbose_name = 'Финансовый отчет'
        verbose_name_plural = 'Отчет: Выручка и Прибыль'


# ==============================================================================
# АВТООБНОВЛЕНИЕ ИЗ EXCEL
# ==============================================================================
class PriceUpdate(models.Model):
    excel_file = models.FileField('Файл прайс-листа (.xlsx)', upload_to='price_updates/')
    created_at = models.DateTimeField('Дата загрузки', auto_now_add=True)
    log = models.TextField('Отчет системы', blank=True)

    class Meta:
        verbose_name = 'Обновление прайса (Excel)'; verbose_name_plural = 'Обновления из Excel'; ordering = [
            '-created_at']

    def __str__(self):
        return f"Обновление от {self.created_at.strftime('%d.%m.%Y %H:%M')}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.excel_file:
            log_messages = []
            updated_count = 0
            try:
                wb = openpyxl.load_workbook(self.excel_file)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row or row[0] is None: continue
                    sku = str(row[0]).strip()
                    price_val = row[1]
                    stock_val = row[2] if len(row) > 2 else None
                    purchase_val = row[3] if len(row) > 3 else None
                    shipping_val = row[4] if len(row) > 4 else None

                    if sku.lower() == 'артикул' or sku == '': continue

                    try:
                        product = Product.objects.filter(sku=sku).first()
                        if product:
                            if price_val is not None: product.price = Decimal(
                                str(price_val).replace(',', '.')) if isinstance(price_val, str) else Decimal(
                                str(price_val))
                            if stock_val is not None:
                                try:
                                    product.stock = int(float(str(stock_val).replace(',', '.')))
                                except ValueError:
                                    pass
                            if purchase_val is not None: product.purchase_price = Decimal(
                                str(purchase_val).replace(',', '.')) if isinstance(purchase_val, str) else Decimal(
                                str(purchase_val))
                            if shipping_val is not None: product.supplier_shipping_cost = Decimal(
                                str(shipping_val).replace(',', '.')) if isinstance(shipping_val, str) else Decimal(
                                str(shipping_val))
                            product.save(update_fields=['price', 'stock', 'purchase_price', 'supplier_shipping_cost'])
                            updated_count += 1
                            log_messages.append(f"✅ {sku} обновлен.")
                        else:
                            log_messages.append(f"❌ Не найден: Артикул {sku}.")
                    except Exception:
                        log_messages.append(f"⚠️ Ошибка ({sku}).")

                self.log = f"Итого обновлено: {updated_count}\n" + "=" * 40 + "\n\n" + "\n".join(log_messages)
            except Exception as e:
                self.log = f"Ошибка: {e}"
            super().save(update_fields=['log'])