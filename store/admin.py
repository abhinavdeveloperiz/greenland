from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Brand, Category, Product, ProductImage, AdvertisementBanner,
    GreenLandProduct, Brand88Product, Brand777Product
)

# Customize Admin Site Titles
admin.site.site_header = "GreenLand Foodstuff Management Portal"
admin.site.site_title = "Greenland Admin"
admin.site.index_title = "Foodstuff Inventory & Storefront Administration"

# Inject dynamic storefront metrics into all admin templates
original_each_context = admin.site.each_context

def custom_each_context(request):
    ctx = original_each_context(request)
    try:
        ctx['total_categories'] = Category.objects.count()
        ctx['total_products'] = Product.objects.count()
        ctx['in_stock_products'] = Product.objects.filter(availability='in_stock', is_active=True).count()
        ctx['coming_soon_products'] = Product.objects.filter(availability='coming_soon', is_active=True).count()
        ctx['active_banners'] = AdvertisementBanner.objects.filter(is_active=True).count()
        
        # Brand-specific metrics
        ctx['greenland_count'] = Product.objects.filter(brand_code='greenland').count()
        ctx['brand88_count'] = Product.objects.filter(brand_code='88').count()
        ctx['brand777_count'] = Product.objects.filter(brand_code='777').count()
    except Exception:
        pass
    return ctx

admin.site.each_context = custom_each_context


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_logo_display', 'name', 'code', 'products_count', 'tagline', 'order', 'is_active')
    list_display_links = ('brand_logo_display', 'name')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'code', 'tagline', 'description')
    
    fieldsets = (
        ("Brand Information", {
            'fields': ('code', 'name', 'tagline', 'description', 'order', 'is_active')
        }),
        ("Brand Logo", {
            'fields': ('logo',),
            'description': "Upload official logo for this brand."
        }),
    )

    def brand_logo_display(self, obj):
        if obj.logo:
            return format_html(
                '<div class="gl-thumb-container"><img src="{}" class="gl-thumb-img" alt="{}" /></div>',
                obj.logo.url, obj.name
            )
        icons = {'greenland': '🌿', '88': '🌾', '777': '⭐'}
        icon = icons.get(obj.code, '🏷️')
        return format_html('<span style="font-size: 24px;">{}</span>', icon)
    brand_logo_display.short_description = "Brand"

    def products_count(self, obj):
        count = Product.objects.filter(brand_code=obj.code).count()
        url = reverse('admin:store_product_changelist') + f"?brand_code__exact={obj.code}"
        return format_html(
            '<a href="{}" style="font-weight: 800; color: #124A2E; background: #FAF6EE; border: 1px solid #E2DDD3; padding: 4px 10px; border-radius: 6px;">{} Products</a>',
            url, count
        )
    products_count.short_description = "Catalog Items"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'slug', 'products_count', 'is_featured', 'order', 'updated_at')
    list_display_links = ('image_preview', 'name')
    list_filter = ('is_featured',)
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_featured')
    readonly_fields = ('current_image_display', 'created_at', 'updated_at')
    
    fieldsets = (
        ("Category Details", {
            'fields': ('name', 'slug', 'description', 'order', 'is_featured')
        }),
        ("Category Photo & Upload", {
            'fields': ('image', 'current_image_display', 'item_count_label'),
            'description': "Upload an official photo for this foodstuff category. It will display immediately in the homepage grid and category headers."
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        url = obj.image_url
        if url:
            return format_html(
                '<div class="gl-thumb-container"><img src="{}" class="gl-thumb-img" alt="{}" /></div>',
                url, obj.name
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = "Photo"

    def current_image_display(self, obj):
        url = obj.image_url
        if url:
            return format_html(
                '<div class="gl-form-preview"><img src="{}" alt="{}" /><div><strong>Current Active Photo</strong><br><small style="color:#666;">{}</small></div></div>',
                url, obj.name, url
            )
        return "No image uploaded yet."
    current_image_display.short_description = "Current Image Preview"

    def products_count(self, obj):
        count = obj.products.count()
        url = reverse('admin:store_product_changelist') + f"?category__id__exact={obj.id}"
        return format_html(
            '<a href="{}" style="font-weight: 700; color: #124A2E; background: #FAF6EE; border: 1px solid #E2DDD3; padding: 3px 8px; border-radius: 6px;">{} Items</a>',
            url, count
        )
    products_count.short_description = "Products"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'inline_image_preview', 'alt_text', 'order')
    readonly_fields = ('inline_image_preview',)

    def inline_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 45px; max-width: 60px; object-fit: contain; border-radius: 4px; border: 1px solid #ccc;" />', obj.image.url)
        return "-"
    inline_image_preview.short_description = "Preview"


class BaseProductAdmin(admin.ModelAdmin):
    """Base Admin with rich preview, pricing format, inline gallery, and badge styling."""
    list_display = ('product_preview', 'name', 'id', 'category', 'price_display', 'weight', 'availability_badge', 'is_featured', 'is_new', 'is_active')
    list_display_links = ('product_preview', 'name')
    list_filter = ('category', 'availability', 'is_featured', 'is_new', 'is_active')
    search_fields = ('name', 'id', 'brand', 'description')
    list_editable = ('is_featured', 'is_new', 'is_active')
    inlines = [ProductImageInline]
    readonly_fields = ('primary_image_preview', 'created_at', 'updated_at')

    fieldsets = (
        ("Core Information", {
            'fields': ('id', 'name', 'category', 'brand_code', 'brand', 'weight', 'unit')
        }),
        ("Pricing & Stock", {
            'fields': ('price', 'original_price', 'stock', 'availability')
        }),
        ("Storefront Flags", {
            'fields': ('is_featured', 'is_popular', 'is_new', 'is_active'),
            'description': "Configure whether this product appears on the homepage, new arrival grids, or search results."
        }),
        ("Primary Product Photo", {
            'fields': ('primary_image', 'primary_image_preview'),
            'description': "Upload the main image for this product. Use the Gallery section below for additional photos."
        }),
        ("Description & Technical Specs", {
            'fields': ('description', 'specs'),
            'classes': ('collapse',)
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def product_preview(self, obj):
        url = obj.primary_image_url
        if url:
            return format_html(
                '<div class="gl-thumb-container"><img src="{}" class="gl-thumb-img" alt="{}" /></div>',
                url, obj.name
            )
        return format_html('<span style="color: #999;">No image</span>')
    product_preview.short_description = "Photo"

    def primary_image_preview(self, obj):
        url = obj.primary_image_url
        if url:
            return format_html(
                '<div class="gl-form-preview"><img src="{}" alt="{}" /><div><strong>Current Product Photo</strong><br><small style="color:#666;">{}</small></div></div>',
                url, obj.name, url
            )
        return "No photo uploaded yet."
    primary_image_preview.short_description = "Current Image Preview"

    def price_display(self, obj):
        return format_html('<strong style="color: #BA1B1D; font-family: Outfit, sans-serif;">KD {}</strong>', f"{float(obj.price):.3f}")
    price_display.short_description = "Price"
    price_display.admin_order_field = 'price'

    def availability_badge(self, obj):
        if obj.availability == 'in_stock':
            return format_html('<span class="gl-badge gl-badge-in-stock">● In Stock</span>')
        elif obj.availability == 'coming_soon':
            return format_html('<span class="gl-badge gl-badge-coming-soon">✨ Coming Soon</span>')
        else:
            return format_html('<span class="gl-badge gl-badge-out-of-stock">✖ Out of Stock</span>')
    availability_badge.short_description = "Status"
    availability_badge.admin_order_field = 'availability'


# =========================================================================
# 1. GREENLAND PRODUCTS ADMIN (DEDICATED BRAND SECTION)
# =========================================================================
@admin.register(GreenLandProduct)
class GreenLandProductAdmin(BaseProductAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(brand_code='greenland')

    def save_model(self, request, obj, form, change):
        obj.brand_code = 'greenland'
        if not obj.brand or obj.brand == 'GreenLand Food Stuff':
            obj.brand = 'GreenLand Food Stuff'
        super().save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        return {
            'brand_code': 'greenland',
            'brand': 'GreenLand Food Stuff'
        }


# =========================================================================
# 2. 88 BRAND PRODUCTS ADMIN (DEDICATED BRAND SECTION)
# =========================================================================
@admin.register(Brand88Product)
class Brand88ProductAdmin(BaseProductAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(brand_code='88')

    def save_model(self, request, obj, form, change):
        obj.brand_code = '88'
        if not obj.brand:
            obj.brand = '88 Brand Wholesale'
        super().save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        return {
            'brand_code': '88',
            'brand': '88 Brand Wholesale'
        }


# =========================================================================
# 3. 777 BRAND PRODUCTS ADMIN (DEDICATED BRAND SECTION)
# =========================================================================
@admin.register(Brand777Product)
class Brand777ProductAdmin(BaseProductAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(brand_code='777')

    def save_model(self, request, obj, form, change):
        obj.brand_code = '777'
        if not obj.brand:
            obj.brand = '777 Brand'
        super().save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        return {
            'brand_code': '777',
            'brand': '777 Brand'
        }


# =========================================================================
# 4. MASTER CATALOG (ALL PRODUCTS COMBINED)
# =========================================================================
@admin.register(Product)
class ProductAdmin(BaseProductAdmin):
    list_display = ('product_preview', 'brand_pill', 'name', 'id', 'category', 'price_display', 'weight', 'availability_badge', 'is_featured', 'is_new', 'is_active')
    list_filter = ('brand_code', 'category', 'availability', 'is_featured', 'is_new', 'is_active')

    def brand_pill(self, obj):
        colors = {
            'greenland': ('#124A2E', '#FAF6EE', '🌿 GreenLand'),
            '88': ('#8A6000', '#FFF8E7', '🌾 88 Brand'),
            '777': ('#BA1B1D', '#FDF2F2', '⭐ 777 Brand'),
        }
        color, bg, label = colors.get(obj.brand_code, ('#666', '#eee', obj.brand))
        return format_html(
            '<span style="display:inline-block; font-weight:800; font-size:11px; padding:3px 8px; border-radius:12px; background:{}; color:{}; border:1px solid {};">{}</span>',
            bg, color, color, label
        )
    brand_pill.short_description = "Brand"
    brand_pill.admin_order_field = 'brand_code'


@admin.register(AdvertisementBanner)
class AdvertisementBannerAdmin(admin.ModelAdmin):
    list_display = ('banner_preview', 'title', 'badge_text', 'net_weight', 'linked_product', 'is_active', 'created_at')
    list_display_links = ('banner_preview', 'title')
    list_filter = ('is_active', 'badge_text')
    search_fields = ('title', 'subtitle', 'arabic_title', 'formulation')
    list_editable = ('is_active',)
    readonly_fields = ('banner_preview_large', 'created_at', 'updated_at')

    fieldsets = (
        ("Banner Content", {
            'fields': ('title', 'subtitle', 'arabic_title', 'formulation', 'badge_text', 'net_weight', 'brand')
        }),
        ("Poster Image", {
            'fields': ('image', 'banner_preview_large'),
            'description': "Upload high-resolution advertisement poster graphic."
        }),
        ("Call to Action & Links", {
            'fields': ('whatsapp_text', 'linked_product', 'is_active')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def banner_preview(self, obj):
        url = obj.image_url
        if url:
            return format_html(
                '<div class="gl-thumb-container" style="width: 70px; height: 70px;"><img src="{}" class="gl-thumb-img" alt="{}" /></div>',
                url, obj.title
            )
        return "-"
    banner_preview.short_description = "Poster"

    def banner_preview_large(self, obj):
        url = obj.image_url
        if url:
            return format_html(
                '<div class="gl-form-preview" style="max-width: 500px;"><img src="{}" style="max-height: 180px; max-width: 220px;" alt="{}" /><div><strong>Active Poster Graphic</strong><br><small style="color:#666;">{}</small></div></div>',
                url, obj.title, url
            )
        return "No image uploaded yet."
    banner_preview_large.short_description = "Current Poster Preview"
