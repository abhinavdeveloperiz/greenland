from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AdvertisementBanner,
    Brand,
    Brand88Product,
    Brand777Product,
    Cart,
    CartItem,
    Category,
    GreenLandProduct,
    Product,
    ProductImage,
    ProductVariant,
    Wishlist,
    WishlistItem,
)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['weight', 'price', 'original_price', 'unit', 'stock', 'is_default', 'order', 'is_active']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image_preview', 'image', 'order', 'alt_text']

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<div style="width: 42px; height: 42px; border-radius: 6px; border: 1px solid #e2e8f0; background: #fff; display: flex; align-items: center; justify-content: center; padding: 2px;">'
                '<img src="{}" style="max-width: 100%; max-height: 100%; object-fit: contain;" />'
                '</div>',
                obj.image.url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No image</span>')
    image_preview.short_description = "Preview"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'code', 'tagline']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'slug', 'is_featured', 'order', 'item_count_label']
    list_display_links = ['image_preview', 'name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'order']
    search_fields = ['name', 'slug', 'description']

    def image_preview(self, obj):
        url = obj.image_url
        if url:
            return format_html(
                '<div style="width: 40px; height: 40px; border-radius: 8px; border: 1px solid #e2e8f0; background: #fff; display: flex; align-items: center; justify-content: center; padding: 2px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">'
                '<img src="{}" style="max-width: 100%; max-height: 100%; object-fit: contain;" alt="{}" />'
                '</div>',
                url,
                obj.name
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">—</span>')
    image_preview.short_description = "Image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview',
        'name',
        'id',
        'category',
        'brand_code',
        'price',
        'original_price',
        'stock',
        'availability',
        'is_featured',
        'is_active',
    ]
    list_display_links = ['image_preview', 'name']
    list_filter = ['brand_code', 'category', 'availability', 'is_featured', 'is_active']
    search_fields = ['id', 'name', 'description', 'brand', 'spec_1', 'spec_2', 'spec_3', 'spec_4']
    list_editable = ['price', 'stock', 'availability', 'is_featured', 'is_active']
    readonly_fields = ['image_detail_preview']
    inlines = [ProductVariantInline, ProductImageInline]

    def image_preview(self, obj):
        url = obj.primary_image_url
        if url:
            return format_html(
                '<div style="width: 48px; height: 48px; border-radius: 8px; border: 1px solid #e2e8f0; background: #ffffff; display: flex; align-items: center; justify-content: center; padding: 2px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">'
                '<img src="{}" style="max-width: 100%; max-height: 100%; object-fit: contain;" alt="{}" />'
                '</div>',
                url,
                obj.name
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No image</span>')
    image_preview.short_description = "Product Image"

    def image_detail_preview(self, obj):
        url = obj.primary_image_url
        if url:
            return format_html(
                '<div style="width: 110px; height: 110px; border-radius: 12px; border: 1px solid #cbd5e1; background: #ffffff; display: flex; align-items: center; justify-content: center; padding: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">'
                '<img src="{}" style="max-width: 100%; max-height: 100%; object-fit: contain;" alt="{}" />'
                '</div>',
                url,
                obj.name
            )
        return format_html('<span style="color: #94a3b8; font-size: 12px;">No image selected yet</span>')
    image_detail_preview.short_description = "Current Image Preview"

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'category', 'brand_code', 'brand', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'original_price', 'weight', 'unit', 'stock', 'availability')
        }),
        ('Product Specifications (4 Simple Fields)', {
            'fields': ('spec_1', 'spec_2', 'spec_3', 'spec_4'),
            'description': 'Add up to 4 specifications. Tip: enter as "Title: Value" (e.g. "Origin: India", "Processing: Sortex Cleaned", "Shelf Life: 24 Months").'
        }),
        ('Images', {
            'fields': ('image_detail_preview', 'primary_image', 'static_image_path')
        }),
        ('Visibility & Badges', {
            'fields': ('is_featured', 'is_popular', 'is_new', 'is_active')
        }),
    )


@admin.register(GreenLandProduct)
class GreenLandProductAdmin(ProductAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(brand_code='greenland')


@admin.register(Brand88Product)
class Brand88ProductAdmin(ProductAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(brand_code='88')


@admin.register(Brand777Product)
class Brand777ProductAdmin(ProductAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(brand_code='777')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'alt_text']
    list_filter = ['product']


@admin.register(AdvertisementBanner)
class AdvertisementBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'badge_text', 'is_active']
    list_editable = ['is_active']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'weight', 'price', 'original_price', 'unit', 'stock', 'is_default', 'is_active']
    list_filter = ['is_active', 'unit', 'product__brand_code', 'product__category']
    search_fields = ['product__name', 'weight']
    list_editable = ['weight', 'price', 'original_price', 'stock', 'is_default', 'is_active']

# =========================================================================
# CART & WISHLIST ADMIN (OPTIMIZED WITH SELECT_RELATED & INLINES)
# =========================================================================

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'variant', 'quantity', 'unit_price_display', 'total_price_display', 'updated_at']
    readonly_fields = ['unit_price_display', 'total_price_display', 'updated_at']

    def unit_price_display(self, obj):
        if obj.id:
            return f"KD {obj.unit_price:.3f}"
        return "—"
    unit_price_display.short_description = "Unit Price"

    def total_price_display(self, obj):
        if obj.id:
            return f"KD {obj.total_price:.3f}"
        return "—"
    total_price_display.short_description = "Subtotal"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_or_guest', 'items_count', 'formatted_subtotal', 'updated_at', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'session_key']
    readonly_fields = ['created_at', 'updated_at', 'formatted_subtotal']
    inlines = [CartItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('items__product', 'items__variant')

    def user_or_guest(self, obj):
        if obj.user:
            return format_html('<strong>{}</strong> <span style="color:#64748b;">({})</span>', obj.user.username, obj.user.email or 'no email')
        key = obj.session_key or 'None'
        return format_html('<span style="color:#f59e0b; font-family:monospace;">Guest ({})</span>', key[:12])
    user_or_guest.short_description = "Customer / Session"

    def items_count(self, obj):
        return obj.total_count
    items_count.short_description = "Total Items"

    def formatted_subtotal(self, obj):
        return f"KD {obj.subtotal:.3f}"
    formatted_subtotal.short_description = "Cart Total"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_link', 'product', 'variant', 'quantity', 'unit_price_display', 'total_price_display', 'updated_at']
    list_filter = ['created_at', 'variant']
    search_fields = ['cart__user__username', 'cart__session_key', 'product__name']
    readonly_fields = ['unit_price_display', 'total_price_display', 'created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cart', 'cart__user', 'product', 'variant')

    def cart_link(self, obj):
        return f"Cart #{obj.cart_id}"
    cart_link.short_description = "Cart"

    def unit_price_display(self, obj):
        return f"KD {obj.unit_price:.3f}"
    unit_price_display.short_description = "Price"

    def total_price_display(self, obj):
        return f"KD {obj.total_price:.3f}"
    total_price_display.short_description = "Total"


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    fields = ['product', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_or_guest', 'items_count', 'updated_at', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'session_key']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [WishlistItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('items__product')

    def user_or_guest(self, obj):
        if obj.user:
            return format_html('<strong>{}</strong> <span style="color:#64748b;">({})</span>', obj.user.username, obj.user.email or 'no email')
        key = obj.session_key or 'None'
        return format_html('<span style="color:#ec4899; font-family:monospace;">Guest ({})</span>', key[:12])
    user_or_guest.short_description = "Customer / Session"

    def items_count(self, obj):
        return obj.total_count
    items_count.short_description = "Saved Items"
