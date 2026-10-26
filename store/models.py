from django.db import models
from django.urls import reverse

class Brand(models.Model):
    code = models.CharField(max_length=50, primary_key=True, help_text="Unique brand code (greenland, 88, 777)")
    name = models.CharField(max_length=150, help_text="Brand display name (e.g. GreenLand Food Stuff, 88 Brand, 777 Brand)")
    tagline = models.CharField(max_length=255, blank=True, help_text="Short brand subtitle or quality promise")
    description = models.TextField(blank=True, help_text="Brand background and history")
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, help_text="Brand logo image")
    order = models.PositiveIntegerField(default=0, help_text="Display sequence")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Category name (e.g. Canned Products, Indian Premium Tea)")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly slug (e.g. canned-products)")
    description = models.TextField(blank=True, help_text="Short description of this category")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text="Upload category display photo")
    static_fallback_image = models.CharField(max_length=255, blank=True, help_text="Default static image path if no image uploaded")
    item_count_label = models.CharField(max_length=100, blank=True, help_text="Optional custom badge text (e.g. '8 Products' or 'Wholesale Supply'). Leave empty to auto-calculate.")
    is_featured = models.BooleanField(default=True, help_text="Display on homepage categories showcase")
    order = models.PositiveIntegerField(default=0, help_text="Display order sequence")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('store:products')}?category={self.slug}"

    @property
    def image_url(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        if self.static_fallback_image:
            return self.static_fallback_image
        import os
        from django.conf import settings
        for ext in ['.png', '.jpg', '.webp']:
            cand = f"categories/{self.slug}{ext}"
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, cand)):
                return f"{settings.MEDIA_URL}{cand}"
        return f"/static/images/products/{self.slug}.png"

    @property
    def image_display(self):
        return self.image_url

    @property
    def active_count(self):
        if hasattr(self, '_active_count'):
            return self._active_count
        return self.products.filter(is_active=True).count()

    @active_count.setter
    def active_count(self, value):
        self._active_count = value

    @property
    def itemCount(self):
        if hasattr(self, '_item_count'):
            return self._item_count
        if self.item_count_label:
            return self.item_count_label
        count = self.active_count
        return f"{count} Products" if count != 1 else "1 Product"

    @itemCount.setter
    def itemCount(self, value):
        self._item_count = value


class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('coming_soon', 'Coming Soon'),
        ('out_of_stock', 'Out of Stock'),
    ]

    BRAND_CHOICES = [
        ('greenland', 'GreenLand Food Stuff'),
        ('88', '88 Brand'),
        ('777', '777 Brand'),
    ]

    id = models.CharField(max_length=100, primary_key=True, help_text="Unique Product ID (e.g. prod-gl-toor-dal, prod-88-ajwain-seeds, prod-777-asafoetida-100g)")
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand_code = models.CharField(max_length=50, choices=BRAND_CHOICES, default='greenland', db_index=True, help_text="Select brand (GreenLand, 88 Brand, or 777 Brand)")
    brand = models.CharField(max_length=150, default='GreenLand Food Stuff', help_text="Display brand title")
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, help_text="Price in KD (e.g. 0.350 or 5.500)")
    original_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text="Original price before discount in KD")
    weight = models.CharField(max_length=100, default='1 KG', help_text="Weight or volume (e.g. 410g, 1 KG Pouch, 20 KG Bulk Sack)")
    unit = models.CharField(max_length=100, blank=True, default='pack', help_text="Packing unit (e.g. tin, retail pack, commercial sack)")
    stock = models.PositiveIntegerField(default=100)
    availability = models.CharField(max_length=30, choices=AVAILABILITY_CHOICES, default='in_stock')
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage New Arrivals section")
    is_popular = models.BooleanField(default=False, help_text="Mark as popular item")
    is_new = models.BooleanField(default=False, help_text="Mark as New Arrival")
    is_active = models.BooleanField(default=True, help_text="Show in storefront")
    description = models.TextField(blank=True)
    spec_1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Specification 1", help_text="e.g. Origin: Selected Indian Grains")
    spec_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Specification 2", help_text="e.g. Processing: 100% Natural")
    spec_3 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Specification 3", help_text="e.g. Quality: Sortex Cleaned")
    spec_4 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Specification 4", help_text="e.g. Shelf Life: 24 Months")
    primary_image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Main product photo")
    static_image_path = models.CharField(max_length=255, blank=True, help_text="Fallback static image path")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name = "All Products (Master List)"
        verbose_name_plural = "📦 All Products (Master Catalog)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.id})"

    def save(self, *args, **kwargs):
        brand_names = {
            'greenland': 'GreenLand Food Stuff',
            '88': '88 Brand Wholesale',
            '777': '777 Brand',
        }
        if self.brand_code in brand_names:
            if not self.brand or self.brand == 'GreenLand Food Stuff':
                self.brand = brand_names[self.brand_code]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'product_id': self.id})

    @property
    def category_slug(self):
        return self.category.slug if self.category else ''

    @property
    def specs_list(self):
        items = []
        for s in [self.spec_1, self.spec_2, self.spec_3, self.spec_4]:
            if s:
                if ':' in s:
                    k, v = s.split(':', 1)
                    items.append({'title': k.strip(), 'value': v.strip()})
                else:
                    items.append({'title': 'Specification', 'value': s.strip()})
        return items

    @property
    def specs(self):
        d = {}
        for s in [self.spec_1, self.spec_2, self.spec_3, self.spec_4]:
            if s:
                if ':' in s:
                    k, v = s.split(':', 1)
                    d[k.strip()] = v.strip()
                else:
                    d[s.strip()] = ''
        return d

    @property
    def originalPrice(self):
        return self.original_price

    @property
    def isFeatured(self):
        return self.is_featured

    @property
    def isPopular(self):
        return self.is_popular

    @property
    def isNew(self):
        return self.is_new

    @property
    def primary_image_url(self):
        if self.primary_image:
            return self.primary_image.url
        if self.static_image_path:
            return self.static_image_path
        return '/static/images/products/greenland-tea-pouch.png'

    @property
    def images(self):
        img_list = []
        if self.primary_image:
            img_list.append(self.primary_image.url)
        elif self.static_image_path:
            img_list.append(self.static_image_path)
            
        for gallery_item in self.gallery_images.all():
            if gallery_item.image:
                img_list.append(gallery_item.image.url)
                
        if not img_list:
            img_list.append('/static/images/products/greenland-tea-pouch.png')
        return img_list

    @property
    def has_variants(self):
        return self.variants.filter(is_active=True).exists()

    @property
    def active_variants(self):
        return list(self.variants.filter(is_active=True).order_by('order', 'price'))

    @property
    def min_price(self):
        vars_qs = self.variants.filter(is_active=True)
        if vars_qs.exists():
            return min(v.price for v in vars_qs)
        return self.price

    @property
    def max_price(self):
        vars_qs = self.variants.filter(is_active=True)
        if vars_qs.exists():
            return max(v.price for v in vars_qs)
        return self.price


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    weight = models.CharField(max_length=100, help_text="Variant weight (e.g. 200g, 500g, 1 KG, 5 KG, 20 KG)")
    unit = models.CharField(max_length=100, blank=True, default='pack', help_text="Packaging type (e.g. pouch, jar, tin, sack)")
    price = models.DecimalField(max_digits=10, decimal_places=3, help_text="Price in KD for this weight (e.g. 0.450)")
    original_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text="Original price before discount in KD")
    stock = models.PositiveIntegerField(default=100)
    is_default = models.BooleanField(default=False, help_text="Default selected variant")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Weight Variant"
        verbose_name_plural = "⚖️ Product Weight Variants"
        ordering = ['order', 'price', 'id']

    def __str__(self):
        return f"{self.product.name} - {self.weight} (KD {self.price:.3f})"


# =========================================================================
# BRAND PROXY MODELS (FOR DEDICATED SEPARATE ADMIN MANAGEMENT)
# =========================================================================
class BrandProductManager(models.Manager):
    def __init__(self, brand_code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.brand_code = brand_code

    def get_queryset(self):
        qs = super().get_queryset()
        if self.brand_code:
            return qs.filter(brand_code=self.brand_code)
        return qs


class GreenLandProduct(Product):
    objects = BrandProductManager('greenland')

    class Meta:
        proxy = True
        verbose_name = "GreenLand Product"
        verbose_name_plural = "🌿 GreenLand Products"

    def save(self, *args, **kwargs):
        self.brand_code = 'greenland'
        if not self.brand or self.brand == 'GreenLand Food Stuff':
            self.brand = 'GreenLand Food Stuff'
        super().save(*args, **kwargs)


class Brand88Product(Product):
    objects = BrandProductManager('88')

    class Meta:
        proxy = True
        verbose_name = "88 Brand Product"
        verbose_name_plural = "🌾 88 Brand Products"

    def save(self, *args, **kwargs):
        self.brand_code = '88'
        if not self.brand:
            self.brand = '88 Brand Wholesale'
        super().save(*args, **kwargs)


class Brand777Product(Product):
    objects = BrandProductManager('777')

    class Meta:
        proxy = True
        verbose_name = "777 Brand Product"
        verbose_name_plural = "⭐ 777 Brand Products"

    def save(self, *args, **kwargs):
        self.brand_code = '777'
        if not self.brand:
            self.brand = '777 Brand'
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='products/gallery/', help_text="Additional gallery photo for this product")
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product Gallery Image"
        verbose_name_plural = "Product Gallery Images"
        ordering = ['order', 'id']

    def __str__(self):
        return f"Photo for {self.product.name}"


class AdvertisementBanner(models.Model):
    title = models.CharField(max_length=255, default='GreenLand Analogue Evaporated Milk')
    subtitle = models.CharField(max_length=255, default='Rich, Smooth & Delicious')
    arabic_title = models.CharField(max_length=255, default='شبيه حليب مبخر', blank=True)
    formulation = models.CharField(max_length=255, default='', blank=True)
    badge_text = models.CharField(max_length=100, default='Coming Soon')
    net_weight = models.CharField(max_length=100, default='410g')
    brand = models.CharField(max_length=150, default='GreenLand Food Stuff')
    image = models.ImageField(upload_to='banners/', blank=True, null=True, help_text="Upload advertisement poster photo")
    static_image_path = models.CharField(max_length=255, default='/static/images/greenland-evaporated-milk-ad.jpg', blank=True)
    whatsapp_text = models.CharField(max_length=255, blank=True, default='Hello Greenland Foodstuff, I am inquiring about GreenLand Analogue Evaporated Milk (410g).')
    linked_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "New Arrival Advertisement Banner"
        verbose_name_plural = "New Arrival Advertisement Banners"

    def __str__(self):
        return f"{self.title} ({self.badge_text})"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.static_image_path:
            return self.static_image_path
        return '/static/images/greenland-evaporated-milk-ad.jpg'
