import csv
import json
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from .models import (Category, Product, ProductImage, MainBanner, CategoryBlockSettings, PromoBanner,
                     FeaturedProductsSettings, HeaderSettings, HeaderNavigation, FooterSettings,
                     Purpose, Color, WorkingSchedule, Courier, CourierSchedule, DeliveryMethod, PaymentMethod,
                     OrderFormField, Order,
                     PriceUpdate, OrderReport)


class CourierScheduleInline(admin.TabularInline):
    model = CourierSchedule
    extra = 7
    max_num = 7


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    inlines = [CourierScheduleInline]


@admin.register(WorkingSchedule)
class WorkingScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'is_working', 'work_from', 'work_to')
    list_editable = ('is_working', 'work_from', 'work_to')


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 3
    fields = (('image', 'image_preview', 'image_position', 'is_active'),)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        script = """<script>
            if (!window.livePreviewLoaded) { window.livePreviewLoaded = true; document.addEventListener('input', function(e) { if (e.target.name && e.target.name.includes('image_position')) { let container = e.target.closest('.inline-related'); let imgClass = '.preview-img-inline'; if (!container) { container = e.target.closest('form'); imgClass = '.preview-img-main'; } if (container) { let img = container.querySelector(imgClass); if (img) { img.style.objectPosition = 'center ' + e.target.value + '%'; } } } }); }
        </script>"""
        if obj.image: return mark_safe(
            f'<div style="width: 100px; height: 100px; border-radius: 8px; border: 2px solid #1E3F35; overflow: hidden; display: inline-block; margin-right: 20px;"><img src="{obj.image.url}" class="preview-img-inline" style="width: 100%; height: 100%; object-fit: cover; object-position: center {obj.image_position}%; transition: object-position 0.1s ease-out;" /></div>' + script)
        return mark_safe(
            '<div style="width: 100px; height: 100px; border-radius: 8px; background: #EFEBE4; display:flex; align-items:center; justify-content:center; color:#8A847B; font-size:12px; margin-right: 20px;">Нет фото</div>' + script)

    image_preview.short_description = "Превью фокуса"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'purchase_price', 'supplier_shipping_cost', 'stock',
                    'available')
    list_editable = ('price', 'purchase_price', 'supplier_shipping_cost', 'stock', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('purposes', 'colors', 'related_products')
    readonly_fields = ('main_image_preview',)

    fields = (
        'category', 'name', 'slug', 'sku', 'description',
        'price', 'purchase_price', 'supplier_shipping_cost', 'stock', 'available',
        'image', 'main_image_preview', 'image_position',
        'purposes', 'colors', 'related_products'
    )
    inlines = [ProductImageInline]

    def main_image_preview(self, obj):
        if obj.image: return mark_safe(
            f'<div style="width: 150px; height: 150px; border-radius: 12px; border: 2px solid #1E3F35; overflow: hidden; display: inline-block;"><img src="{obj.image.url}" class="preview-img-main" style="width: 100%; height: 100%; object-fit: cover; object-position: center {obj.image_position}%; transition: object-position 0.1s ease-out;" /></div>')
        return mark_safe(
            '<div style="width: 150px; height: 150px; border-radius: 12px; background: #EFEBE4; display:flex; align-items:center; justify-content:center; color:#8A847B;">Нет фото</div>')

    main_image_preview.short_description = "Превью главного фото"


# Окно управления категориями Главной страницы (filter_horizontal делает два списка)
@admin.register(CategoryBlockSettings)
class CategoryBlockSettingsAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'order_source', 'items_summary_short', 'total_price', 'gross_profit')
    readonly_fields = ('created', 'live_calc_script')

    fieldsets = (
        ('Информация о заказе', {
            'fields': ('created', 'order_source', 'items_summary', 'delivery_method', 'payment_method', 'form_data')
        }),
        ('Ввод данных (Пишем сюда)', {
            'fields': (
                'items_retail_price',
                'items_purchase_price',
                'supplier_shipping_price',
                'delivery_price'
            )
        }),
        ('Итоги (Считаются автоматически в реальном времени)', {
            'fields': ('cost_price', 'total_price', 'gross_profit', 'live_calc_script'),
        }),
    )

    def live_calc_script(self, obj):
        return mark_safe("""
        <script>
            window.addEventListener('DOMContentLoaded', function() {
                const lockField = (id) => {
                    let el = document.getElementById(id);
                    if (el) {
                        el.readOnly = true;
                        el.style.backgroundColor = '#e9ecef';
                        el.style.pointerEvents = 'none';
                    }
                };
                lockField('id_cost_price');
                lockField('id_total_price');
                lockField('id_gross_profit');
            });

            function updateKotiFinance() {
                const getNum = (id) => {
                    let el = document.getElementById(id);
                    if (!el) return 0;
                    let val = parseFloat(el.value.replace(',', '.'));
                    return isNaN(val) ? 0 : val;
                };

                const setNum = (id, val) => {
                    let el = document.getElementById(id);
                    if (el) el.value = val.toFixed(2).replace('.', ',');
                };

                let retail = getNum('id_items_retail_price');
                let purchase = getNum('id_items_purchase_price');
                let supShip = getNum('id_supplier_shipping_price');
                let delivery = getNum('id_delivery_price');

                let cost = purchase + supShip;
                let total = retail + delivery;
                let profit = retail - cost;

                setNum('id_cost_price', cost);
                setNum('id_total_price', total);
                setNum('id_gross_profit', profit);
            }

            document.addEventListener('input', function(e) {
                if (e.target.id && ['id_items_retail_price', 'id_items_purchase_price', 'id_supplier_shipping_price', 'id_delivery_price'].includes(e.target.id)) {
                    updateKotiFinance();
                }
            });
        </script>
        <div style="color:#1E3F35; font-size:13px; font-weight:bold; padding:5px 0;">
            ⚡ Живой калькулятор включен. Начните вводить цифры выше, и эти поля обновятся сами.
        </div>
        """)

    live_calc_script.short_description = "Автоматизация"

    def items_summary_short(self, obj):
        return obj.items_summary[:50] + '...' if len(obj.items_summary) > 50 else obj.items_summary

    items_summary_short.short_description = "Состав заказа"

    def save_model(self, request, obj, form, change):
        retail = obj.items_retail_price or 0
        purchase = obj.items_purchase_price or 0
        sup_ship = obj.supplier_shipping_price or 0
        delivery = obj.delivery_price or 0

        obj.items_retail_price = retail
        obj.items_purchase_price = purchase
        obj.supplier_shipping_price = sup_ship
        obj.delivery_price = delivery

        obj.cost_price = purchase + sup_ship
        obj.total_price = retail + delivery
        obj.gross_profit = retail - obj.cost_price
        super().save_model(request, obj, form, change)


@admin.register(OrderReport)
class OrderReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/order_report_change_list.html'
    date_hierarchy = 'created'
    list_display = ('id', 'created', 'total_price', 'cost_price', 'gross_profit')
    list_filter = ('created',)

    def has_add_permission(self, request):
        return False

    actions = ['export_to_csv']

    @admin.action(description="Скачать выбранные в Excel (CSV)")
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="koti_finance_report.csv"'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Заказ №', 'Дата создания', 'Выручка (руб)', 'Себестоимость (руб)', 'Валовая прибыль (руб)'])
        for obj in queryset:
            date_str = obj.created.strftime("%d.%m.%Y %H:%M")
            writer.writerow([obj.id, date_str, obj.total_price, obj.cost_price, obj.gross_profit])
        return response

    def changelist_view(self, request, extra_context=None):
        report_data = Order.objects.annotate(month=TruncMonth('created')).values('month').annotate(
            revenue=Sum('total_price'), profit=Sum('gross_profit')).order_by('month')
        labels, revenue_data, profit_data = [], [], []
        for entry in report_data:
            if entry['month']:
                labels.append(entry['month'].strftime('%m.%Y'))
                revenue_data.append(float(entry['revenue'] or 0))
                profit_data.append(float(entry['profit'] or 0))

        extra_context = extra_context or {}
        extra_context['chart_labels'] = json.dumps(labels, cls=DjangoJSONEncoder)
        extra_context['chart_revenue'] = json.dumps(revenue_data, cls=DjangoJSONEncoder)
        extra_context['chart_profit'] = json.dumps(profit_data, cls=DjangoJSONEncoder)
        extra_context['summary_revenue'] = sum(revenue_data)
        extra_context['summary_profit'] = sum(profit_data)

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(OrderFormField)
class OrderFormFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'field_name', 'field_type', 'section', 'is_required', 'sort_order')
    list_editable = ('is_required', 'sort_order')


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'method_type', 'price', 'is_active')
    list_editable = ('price', 'is_active')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    list_editable = ('is_active',)


@admin.register(PriceUpdate)
class PriceUpdateAdmin(admin.ModelAdmin):
    list_display = ('created_at',)
    readonly_fields = ('created_at', 'log')

    def get_exclude(self, request, obj=None):
        if obj is None: return ['log']
        return []


admin.site.register(Category)
admin.site.register(MainBanner)
admin.site.register(PromoBanner)
admin.site.register(FeaturedProductsSettings)
admin.site.register(HeaderSettings)
admin.site.register(HeaderNavigation)
admin.site.register(FooterSettings)
admin.site.register(Purpose)
admin.site.register(Color)