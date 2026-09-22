import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Category, Product, ProductImage, AdvertisementBanner
from store.static_data import CATEGORIES, PRODUCTS

class Command(BaseCommand):
    help = "Seed database with all Greenland Foodstuff categories, products, and advertisement banners"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting Greenland Catalog Database Seeding..."))

        # Ensure media directories exist
        categories_media_dir = Path(settings.MEDIA_ROOT) / 'categories'
        products_media_dir = Path(settings.MEDIA_ROOT) / 'products'
        banners_media_dir = Path(settings.MEDIA_ROOT) / 'banners'
        categories_media_dir.mkdir(parents=True, exist_ok=True)
        products_media_dir.mkdir(parents=True, exist_ok=True)
        banners_media_dir.mkdir(parents=True, exist_ok=True)

        base_dir = Path(settings.BASE_DIR)

        # 1. SEED CATEGORIES
        cat_map = {}
        for index, cat_data in enumerate(CATEGORIES, start=1):
            slug = cat_data['slug']
            name = cat_data['name']
            desc = cat_data.get('description', '')
            item_count = cat_data.get('itemCount', '')
            is_feat = cat_data.get('featured', True)
            static_img = cat_data.get('image', '').split('?')[0] # strip query param

            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': desc,
                    'item_count_label': item_count,
                    'is_featured': is_feat,
                    'order': index * 10,
                    'static_fallback_image': static_img,
                }
            )

            # Copy image to media if exists and not already set
            if static_img and static_img.startswith('/static/'):
                rel_path = static_img.replace('/static/', '')
                src_path = base_dir / 'static' / rel_path
                if src_path.exists():
                    dest_filename = f"{slug}{src_path.suffix}"
                    dest_path = categories_media_dir / dest_filename
                    shutil.copy2(src_path, dest_path)
                    cat.image = f"categories/{dest_filename}"
                    cat.save()

            cat_map[slug] = cat
            status_text = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"Category [{status_text}]: {cat.name} ({slug})"))

        # 2. SEED PRODUCTS
        for prod_data in PRODUCTS:
            p_id = prod_data['id']
            p_name = prod_data['name']
            cat_slug = prod_data['category']
            category = cat_map.get(cat_slug)

            if not category:
                # Fallback to category by slug if not in map
                category = Category.objects.filter(slug=cat_slug).first()

            if not category:
                self.stdout.write(self.style.WARNING(f"Skipping product {p_name}: category {cat_slug} not found."))
                continue

            images = prod_data.get('images', [])
            primary_static = images[0].split('?')[0] if images else ''

            product, created = Product.objects.get_or_create(
                id=p_id,
                defaults={
                    'name': p_name,
                    'category': category,
                    'brand': prod_data.get('brand', 'GreenLand Food Stuff'),
                    'price': prod_data.get('price', 0.0),
                    'original_price': prod_data.get('originalPrice'),
                    'weight': prod_data.get('weight', '1 KG'),
                    'unit': prod_data.get('unit', 'pack'),
                    'stock': prod_data.get('stock', 100),
                    'availability': prod_data.get('availability', 'in_stock'),
                    'is_featured': prod_data.get('isFeatured', False),
                    'is_popular': prod_data.get('isPopular', False),
                    'is_new': prod_data.get('isNew', False),
                    'is_active': True,
                    'description': prod_data.get('description', ''),
                    'specs': prod_data.get('specs', {}),
                    'static_image_path': primary_static,
                }
            )

            # Copy primary image to media if exists
            if primary_static and primary_static.startswith('/static/'):
                rel_path = primary_static.replace('/static/', '')
                src_path = base_dir / 'static' / rel_path
                if src_path.exists():
                    dest_filename = f"{p_id}{src_path.suffix}"
                    dest_path = products_media_dir / dest_filename
                    shutil.copy2(src_path, dest_path)
                    product.primary_image = f"products/{dest_filename}"
                    product.save()

            # Additional gallery images
            if len(images) > 1:
                for idx, extra_img in enumerate(images[1:], start=1):
                    extra_clean = extra_img.split('?')[0]
                    if extra_clean.startswith('/static/'):
                        extra_rel = extra_clean.replace('/static/', '')
                        extra_src = base_dir / 'static' / extra_rel
                        if extra_src.exists():
                            extra_dest_filename = f"{p_id}_gallery_{idx}{extra_src.suffix}"
                            extra_dest_path = products_media_dir / extra_dest_filename
                            shutil.copy2(extra_src, extra_dest_path)
                            ProductImage.objects.get_or_create(
                                product=product,
                                image=f"products/{extra_dest_filename}",
                                defaults={'order': idx}
                            )

            p_status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"Product [{p_status}]: {product.name} ({product.id})"))

        # 3. SEED ADVERTISEMENT BANNER
        ad_src = base_dir / 'static' / 'images' / 'greenland-evaporated-milk-ad.jpg'
        ad_img_rel = ''
        if ad_src.exists():
            ad_dest = banners_media_dir / 'greenland-evaporated-milk-ad.jpg'
            shutil.copy2(ad_src, ad_dest)
            ad_img_rel = 'banners/greenland-evaporated-milk-ad.jpg'

        linked_p = Product.objects.filter(id='prod-gl-evaporated-milk-410g').first()

        banner, b_created = AdvertisementBanner.objects.get_or_create(
            title='GreenLand Analogue Evaporated Milk',
            defaults={
                'subtitle': 'Rich, Smooth & Delicious',
                'arabic_title': 'شبيه حليب مبخر',
                'formulation': 'Replaced Milk Fat with Vegetable Oil',
                'badge_text': 'Coming Soon',
                'net_weight': '410g',
                'brand': 'GreenLand Food Stuff',
                'image': ad_img_rel,
                'static_image_path': '/static/images/greenland-evaporated-milk-ad.jpg',
                'whatsapp_text': 'Hello Greenland Foodstuff, I am inquiring about GreenLand Analogue Evaporated Milk (410g).',
                'linked_product': linked_p,
                'is_active': True,
            }
        )
        b_status = "Created" if b_created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"Advertisement Banner [{b_status}]: {banner.title}"))

        # 4. SEED BRANDS
        from store.models import Brand, Brand777Product
        b_gl, _ = Brand.objects.get_or_create(
            code='greenland',
            defaults={
                'name': 'GreenLand Food Stuff',
                'tagline': 'Premium Indian Tea, 100% Natural Pulses, Grains & Spices',
                'description': 'Greenland Food Stuff is our flagship brand offering pure, sortex-cleaned pantry staples, aromatic spices, and natural pulses.',
                'order': 1,
                'is_active': True,
            }
        )
        b_88, _ = Brand.objects.get_or_create(
            code='88',
            defaults={
                'name': '88 Brand',
                'tagline': 'Wholesale Lentils, Grains & Specialty Flours',
                'description': '88 Brand Wholesale offers high-grade commercial and retail pulses, whole lentils, and traditional flours for catering and family kitchens.',
                'order': 2,
                'is_active': True,
            }
        )
        b_777, _ = Brand.objects.get_or_create(
            code='777',
            defaults={
                'name': '777 Brand',
                'tagline': 'Authentic Traditional Compounded Asafoetida & Pure Oils',
                'description': '777 Brand represents heritage South Indian culinary excellence, celebrated for pure compounded asafoetida and cold-pressed gingelly sesame oils.',
                'order': 3,
                'is_active': True,
            }
        )
        self.stdout.write(self.style.SUCCESS("Brands seeded: greenland, 88, 777"))

        # 5. SEED 777 STARTER PRODUCTS IF NEEDED
        spices_cat = Category.objects.filter(slug='spices-and-seeds').first()
        oil_cat = Category.objects.filter(slug='canned-products').first()

        Brand777Product.objects.get_or_create(
            id='prod-777-asafoetida-100g',
            defaults={
                'name': '777 Compounded Asafoetida Powder (100g)',
                'category': spices_cat,
                'brand': '777 Brand',
                'brand_code': '777',
                'price': 0.850,
                'original_price': 1.100,
                'weight': '100g Jar',
                'unit': 'jar',
                'stock': 85,
                'availability': 'in_stock',
                'is_featured': True,
                'is_new': True,
                'is_active': True,
                'description': 'Authentic South Indian compounded Hing (Asafoetida) powder by legendary 777 Brand. Aromatic culinary enhancer for sambar, rasam, and traditional curries.',
                'specs': {'Brand': '777 Brand', 'Origin': 'India', 'Packaging': '100g Sealed Bottle', 'Purity': 'Compounded Pure Asafoetida'},
                'static_image_path': '/static/images/products/greenland-tea-pouch.png',
            }
        )

        Brand777Product.objects.get_or_create(
            id='prod-777-pure-gingelly-oil-1l',
            defaults={
                'name': '777 Pure Cold-Pressed Gingelly (Sesame) Oil (1L)',
                'category': oil_cat,
                'brand': '777 Brand',
                'brand_code': '777',
                'price': 2.450,
                'original_price': 2.900,
                'weight': '1 Litre Bottle',
                'unit': 'bottle',
                'stock': 60,
                'availability': 'in_stock',
                'is_featured': True,
                'is_new': True,
                'is_active': True,
                'description': 'Traditional 777 pure cold-pressed sesame / gingelly oil. Unrefined and nutrient-rich, ideal for authentic culinary dishes and pickle preparations.',
                'specs': {'Brand': '777 Brand', 'Type': 'Cold Pressed Gingelly Oil', 'Volume': '1 Litre Pet Bottle'},
                'static_image_path': '/static/images/products/tomato-paste-3kg.png',
            }
        )
        self.stdout.write(self.style.SUCCESS("777 Starter products verified"))

        # 6. SEED DEFAULT ADMIN USER IF NONE EXISTS
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@greenland.com', 'admin')
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created with password 'admin'"))

        self.stdout.write(self.style.SUCCESS("\nGreenland catalog seeding successfully completed!"))
