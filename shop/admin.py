from django.contrib import admin
from .models import (Category, Product, MainBanner, CategoryBlockSettings, PromoBanner,
                     FeaturedProductsSettings, HeaderSettings, HeaderNavigation, FooterSettings,
                     Purpose, Color, WorkingSchedule, Courier, CourierSchedule, DeliveryMethod, PaymentMethod, OrderFormField, Order)

# Возможность редактировать график курьера прямо в его карточке
class CourierScheduleInline(admin.TabularInline):
    model = CourierSchedule
    extra = 7  # Сразу выведет 7 строк под каждый день недели
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

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_editable = ('price', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('purposes', 'colors', 'related_products')

@admin.register(OrderFormField)
class OrderFormFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'field_name', 'field_type', 'section', 'is_required', 'sort_order')
    list_editable = ('is_required', 'sort_order')
    list_filter = ('section', 'field_type', 'is_required')

@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'method_type', 'price', 'is_active')
    list_editable = ('price', 'is_active')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    list_editable = ('is_active', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_method', 'payment_method', 'total_price', 'created')
    readonly_fields = ('created', 'delivery_method', 'payment_method', 'delivery_price', 'total_price', 'items_summary', 'form_data')

admin.site.register(Category)
admin.site.register(MainBanner)
admin.site.register(CategoryBlockSettings)
admin.site.register(PromoBanner)
admin.site.register(FeaturedProductsSettings)
admin.site.register(HeaderSettings)
admin.site.register(HeaderNavigation)
admin.site.register(FooterSettings)
admin.site.register(Purpose)
admin.site.register(Color)