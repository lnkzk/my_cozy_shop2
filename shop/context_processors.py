from .cart import Cart
from .models import HeaderSettings, HeaderNavigation, Category, CategoryBlockSettings, PromoBanner, \
    FeaturedProductsSettings, FooterSettings


def cart(request):
    return {'cart': Cart(request)}


def header_data(request):
    featured_section = FeaturedProductsSettings.objects.first()
    return {
        'header_settings': HeaderSettings.objects.first(),
        'header_menu': HeaderNavigation.objects.all(),
        'category_block_settings': CategoryBlockSettings.objects.first(),
        'featured_categories': Category.objects.filter(is_featured=True),
        'promo_banner': PromoBanner.objects.filter(is_active=True).first(),
        'featured_section': featured_section,
        'featured_products': featured_section.products.filter(available=True) if featured_section else [],

        # Автоматическая доставка настроек футера во все макеты
        'footer_settings': FooterSettings.objects.first()
    }