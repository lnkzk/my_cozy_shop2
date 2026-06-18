from django.db import models
from django.urls import reverse


# ==============================================================================
# БАЗОВЫЕ МОДЕЛИ КАТАЛОГА ТОВАРОВ
# ==============================================================================

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon_image = models.ImageField(upload_to='categories/icons/', blank=True, null=True)
    icon_position = models.IntegerField(default=50)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_position = models.IntegerField(default=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    purposes = models.ManyToManyField(Purpose, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    related_products = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='related_to',
        verbose_name='Похожие / Сопутствующие товары'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])


# ==============================================================================
# НАСТРОЙКИ КОНСТРУКТОРА ГЛАВНОЙ СТРАНИЦЫ И ШАПКИ
# ==============================================================================

class MainBanner(models.Model):
    banner_size = models.CharField(max_length=20,
                                   choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
                                   default='medium')
    sub_title = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    show_shipping_badge = models.BooleanField(default=True)
    shipping_title = models.CharField(max_length=100, blank=True)
    shipping_subtitle = models.CharField(max_length=100, blank=True)
    show_payment_badge = models.BooleanField(default=True)
    payment_title = models.CharField(max_length=100, blank=True)
    payment_subtitle = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Главный баннер'
        verbose_name_plural = 'Главные баннеры'


class CategoryBlockSettings(models.Model):
    block_title = models.CharField(max_length=200, default="Shop by Category")
    block_size = models.CharField(max_length=20, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
                                  default='medium')
    block_padding = models.CharField(max_length=20,
                                     choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
                                     default='medium')
    browse_all_text = models.CharField(max_length=50, default="Browse all →")
    browse_all_link = models.CharField(max_length=200, default="/catalog/")

    class Meta:
        verbose_name = 'Настройки блока категорий'
        verbose_name_plural = 'Настройки блоков категорий'


class PromoBanner(models.Model):
    banner_size = models.CharField(max_length=20,
                                   choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
                                   default='medium')
    tag_text = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(max_length=200, blank=True)
    badge_up_to_text = models.CharField(max_length=50, blank=True)
    badge_value_text = models.CharField(max_length=50, blank=True)
    badge_bottom_text = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='promo/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Промо-баннер'
        verbose_name_plural = 'Промо-баннеры'


class FeaturedProductsSettings(models.Model):
    block_title = models.CharField(max_length=200, default="Топ продаж")
    view_all_text = models.CharField(max_length=50, default="View all →")
    view_all_link = models.CharField(max_length=200, default="/catalog/")
    cart_button_text = models.CharField(max_length=50, default="+ Add to Cart")
    products = models.ManyToManyField(Product, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Настройки Топа продаж'
        verbose_name_plural = 'Настройки Топа продаж'


class HeaderSettings(models.Model):
    site_name = models.CharField(max_length=100, default="KÓTI")
    logo_icon = models.CharField(max_length=10, default="★")

    class Meta:
        verbose_name = 'Настройки шапки'
        verbose_name_plural = 'Настройки шапки'


class HeaderNavigation(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ссылка меню'
        verbose_name_plural = 'Ссылки меню'


class FooterSettings(models.Model):
    copyright_text = models.CharField(max_length=200, default="© 2026 KÓTI. Все права защищены.")
    instagram_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Настройки подвала'
        verbose_name_plural = 'Настройки подвала'


# ==============================================================================
# КОНСТРУКТОР ДИНАМИЧЕСКИХ ФОРМ, ОПЛАТЫ И АВТОМАТИЧЕСКОГО ГРАФИКА
# ==============================================================================

class WorkingSchedule(models.Model):
    DAY_CHOICES = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]
    day_of_week = models.IntegerField('День недели', choices=DAY_CHOICES, unique=True)
    is_working = models.BooleanField('Рабочий день магазина', default=True)
    work_from = models.TimeField('Работаем с', default="09:00")
    work_to = models.TimeField('Работаем до', default="21:00")

    class Meta:
        verbose_name = 'График работы магазина'
        verbose_name_plural = 'График магазина (Самовывоз)'
        ordering = ['day_of_week']

    def __str__(self):
        status = f"{self.work_from.strftime('%H:%M')}-{self.work_to.strftime('%H:%M')}" if self.is_working else "Выходной"
        return f"{self.get_day_of_week_display()}: {status}"


# --- НОВЫЙ БЛОК: КУРЬЕРЫ И ИХ ЛИЧНЫЕ ГРАФИКИ ---

class Courier(models.Model):
    name = models.CharField('ФИО Курьера / Название службы', max_length=100)
    is_active = models.BooleanField('Активен (выезжает на заказы)', default=True)

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return self.name


class CourierSchedule(models.Model):
    DAY_CHOICES = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='schedules', verbose_name='Курьер')
    day_of_week = models.IntegerField('День недели', choices=DAY_CHOICES)
    is_working = models.BooleanField('Рабочий день курьера', default=True)
    work_from = models.TimeField('Рабочая смена с', default="10:00")
    work_to = models.TimeField('Рабочая смена до', default="20:00")
    courier_cutoff_time = models.TimeField(
        'Время отсечки для доставки день в день',
        default="15:00",
        help_text="Если клиент заказывает позже этого времени, этот курьер сегодня заказ уже не возьмет."
    )

    class Meta:
        verbose_name = 'Рабочий день курьера'
        verbose_name_plural = 'Графики работы курьеров'
        unique_together = ('courier', 'day_of_week')
        ordering = ['courier', 'day_of_week']

    def __str__(self):
        status = f"{self.work_from.strftime('%H:%M')}-{self.work_to.strftime('%H:%M')}" if self.is_working else "Выходной"
        return f"[{self.courier.name}] {self.get_day_of_week_display()}: {status}"


class DeliveryMethod(models.Model):
    TYPE_CHOICES = [('pickup', 'pickup'), ('courier', 'courier')]
    method_type = models.CharField('Тип доставки', max_length=10, choices=TYPE_CHOICES, unique=True)
    title = models.CharField('Название способа', max_length=100)
    price = models.DecimalField('Стоимость доставки', max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Способ получения'
        verbose_name_plural = 'Способы получения'

    def __str__(self):
        return f"{self.title} ({self.price} руб.)"


class PaymentMethod(models.Model):
    slug = models.SlugField('Идентификатор (латиница)', max_length=50, unique=True)
    title = models.CharField('Название метода оплаты', max_length=100)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

    def __str__(self):
        return self.title


class OrderFormField(models.Model):
    FIELD_TYPES = [
        ('text', 'Текстовая строка (ФИО, Адрес)'),
        ('tel', 'Телефон'),
        ('email', 'Email'),
        ('textarea', 'Многострочное текстовое поле')
    ]
    SECTION_CHOICES = [
        ('address', 'Блок «Адрес»'),
        ('recipient', 'Блок «Данные получателя»')
    ]

    label = models.CharField('Подпись поля / Плейсхолдер', max_length=100)
    field_name = models.CharField('Имя поля в БД (английскими буквами, например: floor)', max_length=50, unique=True)
    field_type = models.CharField('Тип поля ввода', max_length=15, choices=FIELD_TYPES, default='text')
    section = models.CharField('Раздел формы', max_length=15, choices=SECTION_CHOICES, default='recipient')
    is_required = models.BooleanField('Обязательное поле', default=True)
    sort_order = models.IntegerField('Порядок сортировки', default=0)

    class Meta:
        verbose_name = 'Поле формы заказа'
        verbose_name_plural = 'Поля формы заказа'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.label} ({self.get_section_display()})"


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField('Способ получения', max_length=50, default='Не указан')
    payment_method = models.CharField('Способ оплаты', max_length=100, default='Не указан')
    delivery_price = models.DecimalField('Стоимость доставки', max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField('Итоговая сумма', max_digits=10, decimal_places=2)
    items_summary = models.TextField('Состав заказа')
    form_data = models.JSONField('Заполненные поля формы', default=dict, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ №{self.id} от {self.created.strftime('%d.%m.%Y')}"