# store/static_data.py - Greenland Foodstuff, 88 Brand & 777 Brand Wholesale Static Catalog

class CategoryItem(dict):
    """Dictionary that also allows attribute-style access like cat.slug and cat.name."""
    def __getattr__(self, name):
        if name in self:
            return self[name]
        return ''

    def __str__(self):
        return self.get('name', '')


class ProductItem(dict):
    """Dictionary that allows attribute access for templates (e.g. product.category.slug, product.images, etc.)."""
    def __getattr__(self, name):
        if name in self:
            return self[name]
        # Friendly aliases
        aliases = {
            'is_featured': 'isFeatured',
            'is_popular': 'isPopular',
            'is_new': 'isNew',
            'original_price': 'originalPrice',
            'category_name': 'categoryName',
            'primary_image_url': 'image',
        }
        if name in aliases and aliases[name] in self:
            return self[aliases[name]]
        return None


CATEGORIES_RAW = [
    {
        'id': 'rice',
        'name': 'Rice & Grains',
        'slug': 'rice',
        'description': 'Authentic Indian origin rice bags (Idli Rice, Long Grain White Rice, Palakkadan Matta, Thanjavur Ponni & XXL Basmathi) in 18-20 KG bulk sacks.',
        'image': '/static/images/products/greenland-thanjavur-ponni-rice-20kg.png',
        'itemCount': '5 Products',
        'featured': True,
        'order': 1,
    },
    {
        'id': 'cereals-and-legumes',
        'name': 'Cereals & Legumes',
        'slug': 'cereals-and-legumes',
        'description': '100% natural retail pulses (Toor Dal, Urad Dal) & 88 Brand commercial bulk sacks of chickpeas, moong, and lentils.',
        'image': '/static/images/products/toor-dal-1kg.png',
        'itemCount': '8 Products',
        'featured': True,
        'order': 2,
    },
    {
        'id': 'canned-products',
        'name': 'Canned Products',
        'slug': 'canned-products',
        'description': 'Pure double concentrated tomato paste, analogue evaporated milk, and culinary canned essentials in commercial tins.',
        'image': '/static/images/products/tomato-paste-3kg.png',
        'itemCount': '2 Products',
        'featured': True,
        'order': 3,
    },
    {
        'id': 'spices-and-seeds',
        'name': 'Spices & Seeds',
        'slug': 'spices-and-seeds',
        'description': 'Aromatic whole spices, ajwain seeds, compounded asafoetida (Hing), and traditional South Indian masala powders.',
        'image': '/static/images/products/88-ajwain-seeds-10kg.png',
        'itemCount': '4 Products',
        'featured': True,
        'order': 4,
    },
    {
        'id': 'tea',
        'name': 'Indian Premium Tea',
        'slug': 'tea',
        'description': 'GreenLand Indian premium tea blends in aroma-sealed 250g gold jars and heavy-duty 5 KG master carry pouches.',
        'image': '/static/images/products/greenland-tea-pouch.png',
        'itemCount': '2 Products',
        'featured': True,
        'order': 5,
    },
    {
        'id': 'nuts-and-dry-fruits',
        'name': 'Nuts & Dry Fruits',
        'slug': 'nuts-and-dry-fruits',
        'description': 'Premium California almonds, jumbo cashews, walnuts, raisins, and wholesale dry fruits.',
        'image': '/static/images/products/88-black-chick-peas-15kg.png',
        'itemCount': 'Wholesale Supply',
        'featured': False,
        'order': 6,
    },
    {
        'id': 'milk',
        'name': 'Dairy & Pantry',
        'slug': 'milk',
        'description': 'Wholesale commercial dairy powders, condensed milk, and essential grocery pantry staples.',
        'image': '/static/images/products/greenland-evaporated-milk-410g.jpg',
        'itemCount': 'Wholesale Supply',
        'featured': False,
        'order': 7,
    },
]

CATEGORIES = [CategoryItem(c) for c in CATEGORIES_RAW]

BRANDS = [
    {
        'code': 'greenland',
        'name': 'GreenLand Food Stuff',
        'tagline': 'Authentic Indian Foodstuffs, Premium Teas & Wholesale Grains',
        'description': 'Direct farm imports of authentic Indian pulses, aged rice, Ceylon & Assam tea blends, and culinary essentials.',
        'logo': '/static/images/greenland-emblem-logo-tight.png',
        'badge': '🌿 Premium Retail & Wholesale',
        'product_count': 10,
        'order': 1,
    },
    {
        'code': '88',
        'name': '88 Brand Wholesale',
        'tagline': 'Commercial Agro Commodities & Heavy-Duty Bulk Sacks',
        'description': 'Heavy-duty commercial sacks of chickpeas, moong dal, lentils, and aromatic ajwain seeds machine sorted and packed in UAE.',
        'logo': '/static/images/products/88-ajwain-seeds-10kg-trans.png',
        'badge': '🌾 Commercial Bulk Sacks',
        'product_count': 6,
        'order': 2,
    },
    {
        'code': '777',
        'name': '777 Brand',
        'tagline': 'Heritage South Indian Culinary Spices, Hing & Traditional Masalas',
        'description': 'Famous traditional culinary seasonings, pure compounded asafoetida (Hing), sambar, rasam powders, and heritage pickles.',
        'logo': '/static/images/products/toor-dal-1kg.png',
        'badge': '⭐ Authentic Heritage Spices',
        'product_count': 4,
        'order': 3,
    },
]

ADVERTISEMENT_BANNER = {
    'id': 1,
    'title': 'GreenLand Analogue Evaporated Milk (410g)',
    'subtitle': 'Rich, Smooth & Delicious — Coming Soon to Stores',
    'badge_text': 'COMING SOON • NEW PACK',
    'arabic_title': 'شبيه حليب مبخر',
    'formulation': 'Culinary Analogue Evaporated Milk',
    'net_weight': '410g Net Weight',
    'brand': 'GreenLand Food Stuff',
    'image_url': '/static/images/greenland-evaporated-milk-ad.jpg',
    'whatsapp_text': 'Hello GreenLand Foodstuff, I would like to inquire about the upcoming GreenLand Analogue Evaporated Milk (410g).',
    'linked_product': {'id': 'prod-gl-evaporated-milk-410g'},
}

# Helper to find category info dict
def _cat_dict(slug):
    c = next((item for item in CATEGORIES_RAW if item['slug'] == slug), None)
    if c:
        return CategoryItem(c)
    return CategoryItem({'slug': slug, 'name': slug.replace('-', ' ').title()})

PRODUCTS_RAW = [
    # =========================================================================
    # 1. GREENLAND CULINARY ESSENTIALS (Canned & Dairy)
    # =========================================================================
    {
        'id': 'prod-gl-evaporated-milk-410g',
        'name': 'GreenLand Analogue Evaporated Milk (410g)',
        'category': _cat_dict('canned-products'),
        'category_slug': 'canned-products',
        'categoryName': 'Canned Products',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 0.350,
        'originalPrice': 0.450,
        'weight': '410g',
        'unit': 'tin',
        'stock': 0,
        'availability': 'coming_soon',
        'isFeatured': True,
        'isPopular': True,
        'isNew': True,
        'description': 'COMING SOON — GreenLand Analogue Evaporated Milk. Rich, Smooth & Delicious. شبيه حليب مبخر. Net Weight: 410g.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Product': 'Analogue Evaporated Milk',
            'Arabic Name': 'شبيه حليب مبخر',
            'Attributes': 'Rich, Smooth & Delicious',
            'Net Weight': '410g',
            'Status': 'Coming Soon',
        },
        'images': [
            '/static/images/greenland-evaporated-milk-ad.jpg',
            '/static/images/products/greenland-evaporated-milk-410g.jpg',
        ],
    },
    {
        'id': 'prod-gl-tomato-paste',
        'name': 'GreenLand Double Concentrated Tomato Paste (3 KG)',
        'category': _cat_dict('canned-products'),
        'category_slug': 'canned-products',
        'categoryName': 'Canned Products',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 5.500,
        'originalPrice': 6.250,
        'weight': '3 KG (Box of 4)',
        'unit': 'box of 4 cans',
        'stock': 45,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '100% Pure & Natural Culinary Essential Tomato Paste by GreenLand Food Stuff. Rich crimson color and thick velvety texture prepared from vine-ripened tomatoes. Packed in heavy commercial 3 KG tins (Box of 4).',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '3 KG per Can (Box of 4)',
            'Origin / Processing': 'GreenLand Foodstuff Certified',
            'Classification': 'Culinary Essential Double Concentrated',
            'Shelf Life': '24 Months',
        },
        'images': [
            '/static/images/products/tomato-paste-3kg.png',
        ],
    },

    # =========================================================================
    # 2. GREENLAND 100% NATURAL RETAIL PACK PULSES (Cereals & Legumes)
    # =========================================================================
    {
        'id': 'prod-gl-toor-dal',
        'name': 'GreenLand Toor Dal (Split Pigeon Peas)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 0.950,
        'originalPrice': 1.200,
        'weight': '1 KG Pouch',
        'unit': 'retail pack',
        'stock': 120,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '100% Natural split pigeon peas (Toor Dal) by GreenLand. Premium unpolished grains rich in plant protein and dietary fibre for wholesome daily nutrition and traditional culinary cooking.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '1 KG Retail Pack Pouch',
            'Origin / Processing': '100% Natural Selected Grains',
            'Nutrition': 'Rich in Protein & Fibre',
            'Common Name': 'Split Pigeon Peas (Toor Dal)',
        },
        'images': [
            '/static/images/products/toor-dal-1kg.png',
        ],
    },
    {
        'id': 'prod-gl-urad-dal',
        'name': 'GreenLand Urad Dal (Peeled Black Gram)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 1.100,
        'originalPrice': 1.350,
        'weight': '1 KG Pouch',
        'unit': 'retail pack',
        'stock': 100,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': 'Healthy Choice peeled black gram (Urad Dal) by GreenLand. High in natural protein, diet-friendly, and perfect for soft idli/dosa batters, dal makhani, and culinary recipes.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '1 KG Retail Pack Pouch',
            'Origin / Processing': '100% Natural Selected Grains',
            'Nutrition': 'High Protein • Diet Friendly',
            'Common Name': 'Peeled Black Gram (Urad Dal)',
        },
        'images': [
            '/static/images/products/urad-dal-1kg.png',
        ],
    },
    {
        'id': 'prod-gl-urad-split',
        'name': 'GreenLand Urad Split (Split Black Gram)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 1.150,
        'originalPrice': 1.400,
        'weight': '1 KG Pouch',
        'unit': 'retail pack',
        'stock': 90,
        'availability': 'in_stock',
        'isFeatured': False,
        'isPopular': True,
        'isNew': False,
        'description': 'Healthy Choice split black gram with skin (Urad Split). Finest traditional selection with natural grain texture, rich earthy taste, and balanced aroma.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '1 KG Retail Pack Pouch',
            'Origin / Processing': '100% Natural Selected Grains',
            'Quality Grade': 'Finest Traditional Selection',
            'Common Name': 'Split Black Gram (Urad Split)',
        },
        'images': [
            '/static/images/products/urad-split-1kg.png',
        ],
    },

    # =========================================================================
    # 3. 88 BRAND WHOLESALE AGRO COMMODITIES (Commercial & Bulk Sacks)
    # =========================================================================
    {
        'id': 'prod-88-ajwain-seeds',
        'name': '88 Brand Wholesale Ajwain Seeds (10 KG)',
        'category': _cat_dict('spices-and-seeds'),
        'category_slug': 'spices-and-seeds',
        'categoryName': 'Spices & Seeds',
        'brand': '88 Brand Wholesale',
        'brand_code': '88',
        'price': 6.000,
        'originalPrice': 7.200,
        'weight': '10 KG Sack (Net 9.9 KG)',
        'unit': 'commercial sack',
        'stock': 40,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': True,
        'description': '88 Brand premium wholesale aromatic ajwain seeds (Carom Seeds). Processed & packed in UAE in heavy-duty commercial sacks. Natural high-thymol seeds with intense fragrance and medicinal aroma.',
        'specs': {
            'Brand': '88 Brand™ Wholesale Agro Commodities',
            'Pack Size': 'Gross: 10 KG | Net: 9.9 KG',
            'Origin / Processing': 'Processed & Packed in UAE',
            'Type': 'Aromatic Spice (Carom Seeds)',
            'Packaging': 'Heavy-Duty Commercial Sack',
        },
        'images': [
            '/static/images/products/88-ajwain-seeds-10kg.png',
        ],
    },
    {
        'id': 'prod-88-black-chick-peas',
        'name': '88 Brand Wholesale Black Chick Peas (15 KG)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': '88 Brand Wholesale',
        'brand_code': '88',
        'price': 5.400,
        'originalPrice': 6.500,
        'weight': '15 KG Bulk Pack',
        'unit': 'commercial sack',
        'stock': 65,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '88 Brand wholesale premium black chick peas (Kala Chana). High protein agro commodity, machine sorted and packed in UAE in heavy-duty 15 KG sacks with transparent viewing window.',
        'specs': {
            'Brand': '88 Brand™ Wholesale Agro Commodities',
            'Gross Weight': '15 KG Bulk Pack',
            'Origin / Processing': 'Processed & Packed in UAE',
            'Grade': 'Wholesale Bulk Premium',
            'Packaging': 'Commercial Printed Bulk Sack',
        },
        'images': [
            '/static/images/products/88-black-chick-peas-15kg.png',
        ],
    },
    {
        'id': 'prod-88-chick-peas-8mm',
        'name': '88 Brand Chick Peas Kabuli 8mm (15 KG)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': '88 Brand Wholesale',
        'brand_code': '88',
        'price': 5.000,
        'originalPrice': 6.000,
        'weight': '15 KG Bulk Pack',
        'unit': 'commercial sack',
        'stock': 85,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '88 Brand standard grade 8mm Kabuli chick peas (Size 8mm). Clean, calibrated 8mm grains with high boiling yield and tender skin. Processed and packed in UAE in 15 KG sacks.',
        'specs': {
            'Brand': '88 Brand™ Wholesale Agro Commodities',
            'Grain Calibration': '8MM Standard Calibrated',
            'Gross Weight': '15 KG Bulk Pack',
            'Origin / Processing': 'Processed & Packed in UAE',
            'Packaging': 'Commercial Blue Sack with Window',
        },
        'images': [
            '/static/images/products/88-chick-peas-kabuli-8mm-15kg.png',
        ],
    },
    {
        'id': 'prod-88-chick-peas-premium',
        'name': '88 Brand Chick Peas Kabuli Premium Grade (14 KG)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': '88 Brand Wholesale',
        'brand_code': '88',
        'price': 8.000,
        'originalPrice': 9.500,
        'weight': '14/15 KG Pack',
        'unit': 'commercial sack',
        'stock': 55,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '88 Brand Premium Grade jumbo Kabuli chick peas. Selected top-tier bold grains, exceptional tenderness, high water absorption, and superior culinary presentation. Processed and packed in UAE.',
        'specs': {
            'Brand': '88 Brand™ Wholesale Agro Commodities',
            'Grade': 'Premium Grade Jumbo Selection',
            'Gross Weight': '14/15 KG Pack',
            'Origin / Processing': 'Processed & Packed in UAE',
            'Packaging': 'Heavy-Duty Commercial Blue Sack',
        },
        'images': [
            '/static/images/products/88-chick-peas-kabuli-premium-14kg.png',
        ],
    },
    {
        'id': 'prod-88-green-moong-split',
        'name': '88 Brand Green Moong Split (15 KG)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': '88 Brand Wholesale',
        'brand_code': '88',
        'price': 7.750,
        'originalPrice': 9.000,
        'weight': '15 KG Bulk Pack',
        'unit': 'commercial sack',
        'stock': 50,
        'availability': 'in_stock',
        'isFeatured': False,
        'isPopular': True,
        'isNew': False,
        'description': '88 Brand Selected Green Moong Split. Cleaned, uniformly split green gram lentils with high nutrient density, processed and packed in UAE in 15 KG sacks with clear product display window.',
        'specs': {
            'Brand': '88 Brand™ Wholesale Agro Commodities',
            'Gross Weight': '15 KG Bulk Pack',
            'Origin / Processing': 'Processed & Packed in UAE',
            'Selection': 'Selected Split Green Gram',
            'Packaging': 'Commercial Green Wholesale Sack',
        },
        'images': [
            '/static/images/products/88-green-moong-split-15kg.png',
        ],
    },
    {
        'id': 'prod-88-green-whole-lentils',
        'name': '88 Brand Green Whole Lentils (15 KG)',
        'category': _cat_dict('cereals-and-legumes'),
        'category_slug': 'cereals-and-legumes',
        'categoryName': 'Cereals & Legumes',
        'brand': '88 Brand Wholesale',
        'brand_code': '88',
        'price': 5.000,
        'originalPrice': 6.000,
        'weight': '15 KG Bulk Pack',
        'unit': 'commercial sack',
        'stock': 70,
        'availability': 'in_stock',
        'isFeatured': False,
        'isPopular': True,
        'isNew': False,
        'description': '88 Brand Selected Whole Green Lentils. Rich in dietary fiber, earthy flavor, processed and packed in UAE in heavy-duty 15 KG commercial sacks.',
        'specs': {
            'Brand': '88 Brand™ Wholesale Agro Commodities',
            'Gross Weight': '15 KG Bulk Pack',
            'Origin / Processing': 'Processed & Packed in UAE',
            'Selection': 'Selected Whole Green Lentils',
            'Packaging': 'Commercial Heavy-Duty Green Sack',
        },
        'images': [
            '/static/images/products/88-green-whole-lentils-15kg.png',
        ],
    },

    # =========================================================================
    # 4. GREENLAND INDIAN PREMIUM TEA (Tea Line)
    # =========================================================================
    {
        'id': 'prod-gl-tea-pouch-5kg',
        'name': 'GreenLand Indian Premium Tea (5 KG Master Pouch)',
        'category': _cat_dict('tea'),
        'category_slug': 'tea',
        'categoryName': 'Indian Premium Tea',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 7.500,
        'originalPrice': 9.000,
        'weight': '5 KG Master Pouch',
        'unit': 'master pouch',
        'stock': 40,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': 'GreenLand Indian Premium Tea. Selected estate tea blend with brisk aroma and rich reddish liquor, packed in durable 5 KG carry-handle master pouch.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Pack Size': '5 KG Master Pouch with Handle',
            'Origin': 'Indian Premium Estates',
            'Grade': 'Premium Tea Blend',
            'Aroma': 'Brisk, Kadak Golden Liquor',
        },
        'images': [
            '/static/images/products/greenland-tea-pouch.png',
        ],
    },
    {
        'id': 'prod-gl-tea-gold-jar',
        'name': 'GreenLand Indian Premium Tea Gold (250g Jar)',
        'category': _cat_dict('tea'),
        'category_slug': 'tea',
        'categoryName': 'Indian Premium Tea',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 1.850,
        'originalPrice': 2.200,
        'weight': '250g',
        'unit': 'pack',
        'stock': 80,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': True,
        'description': 'GreenLand Indian Premium Tea Gold edition. Selected premium tea blend packed to preserve maximum freshness, strength, and rich aroma.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '250 Grams',
            'Packaging': 'Airtight Aroma Seal Pack',
            'Grade': 'Gold Reserve Premium Tea',
            'Aroma': 'Intense Kadak Blend',
        },
        'images': [
            '/static/images/products/greenland-tea-jar.png',
        ],
    },

    # =========================================================================
    # 5. GREENLAND AUTHENTIC RICE & GRAINS (18 - 20 KG Wholesale Sacks)
    # =========================================================================
    {
        'id': 'prod-gl-basmathi-xxl-19kg',
        'name': 'GreenLand XXL 1121 Sella Basmathi Rice (19 KG)',
        'category': _cat_dict('rice'),
        'category_slug': 'rice',
        'categoryName': 'Rice & Grains',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 8.500,
        'originalPrice': 10.000,
        'weight': '19 KG Bulk Sack',
        'unit': 'commercial sack',
        'stock': 70,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': True,
        'description': 'Authentic Indian XXL 1121 Steam Sella Basmathi Rice by GreenLand. Extra-long slender grains that elongate up to 2.5x upon cooking with exceptional aroma and non-sticky fluffy texture.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '19 KG Wholesale Sack',
            'Origin': 'Product of India (Himalayan Foothills)',
            'Variety': '1121 Steam Sella Basmathi Rice',
            'Grain Length': 'Extra Long Grain XXL',
            'Packaging': 'Heavy-Duty Commercial Stitched Sack',
        },
        'images': [
            '/static/images/products/greenland-basmathi-rice-xxl-19kg.png',
        ],
    },
    {
        'id': 'prod-gl-idli-rice-20kg',
        'name': 'GreenLand Idli Rice (20 KG)',
        'category': _cat_dict('rice'),
        'category_slug': 'rice',
        'categoryName': 'Rice & Grains',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 6.250,
        'originalPrice': 7.500,
        'weight': '20 KG Bulk Sack',
        'unit': 'commercial sack',
        'stock': 60,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '100% Indian Origin premium Idli Rice by GreenLand Food Stuff. Selected short, plump grains ideal for producing soft, fluffy idlis and crispy dosas with authentic fermentation. Net Weight: 20 KG wholesale sack.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '20 KG Wholesale Sack',
            'Origin': '100% Indian Origin',
            'Variety': 'South Indian Short Grain Idli Rice',
            'Usage': 'Traditional Idli & Dosa Batter',
            'Packaging': 'Heavy-Duty Stitched Grain Sack',
        },
        'images': [
            '/static/images/products/greenland-idli-rice-20kg.png',
        ],
    },
    {
        'id': 'prod-gl-long-grain-rice-19kg',
        'name': 'GreenLand Long Grain White Rice (19 KG)',
        'category': _cat_dict('rice'),
        'category_slug': 'rice',
        'categoryName': 'Rice & Grains',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 6.800,
        'originalPrice': 8.000,
        'weight': '19 KG Bulk Sack',
        'unit': 'commercial sack',
        'stock': 75,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '100% Natural long grain white rice by GreenLand Food Stuff. Milled to perfection with non-sticky grains, bright pearl white texture, and uniform length. Ideal for mandi, biryani, and daily meals. Net Weight: 19 KG sack.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '19 KG Wholesale Sack',
            'Origin': 'Product of India',
            'Variety': 'Long Grain Pearl White Rice',
            'Grain Type': 'Long Grain Pearl White',
            'Packaging': 'Durable Woven Commercial Sack',
        },
        'images': [
            '/static/images/products/greenland-long-grain-white-rice-19kg.png',
        ],
    },
    {
        'id': 'prod-gl-palakkadan-matta-18kg',
        'name': 'GreenLand Palakkadan Matta Rice (18 KG)',
        'category': _cat_dict('rice'),
        'category_slug': 'rice',
        'categoryName': 'Rice & Grains',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 6.500,
        'originalPrice': 7.800,
        'weight': '18 KG Bulk Sack',
        'unit': 'commercial sack',
        'stock': 50,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '100% Natural parboiled red/brown rice grown in the nutrient-dense fields of Palakkad, Kerala. Rich in vitamins, high dietary fibre, and authentic earthy flavour. Net Weight: 18 KG sack.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '18 KG Wholesale Sack',
            'Origin': 'Product of India (Palakkad, Kerala)',
            'Variety': 'Palakkadan Matta Parboiled Red Rice',
            'Nutrition': 'High Dietary Fibre & Minerals',
            'Packaging': 'Commercial Heavy-Duty Sack',
        },
        'images': [
            '/static/images/products/greenland-palakkadan-matta-rice-18kg.png',
        ],
    },
    {
        'id': 'prod-gl-thanjavur-ponni-20kg',
        'name': 'GreenLand Thanjavur Ponni Rice (20 KG)',
        'category': _cat_dict('rice'),
        'category_slug': 'rice',
        'categoryName': 'Rice & Grains',
        'brand': 'GreenLand Food Stuff',
        'brand_code': 'greenland',
        'price': 7.200,
        'originalPrice': 8.500,
        'weight': '20 KG Bulk Sack',
        'unit': 'commercial sack',
        'stock': 80,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': '100% Natural Thanjavur Ponni Rice by GreenLand Food Stuff. Grown in the fertile Kaveri delta of Thanjavur. Aged for perfect softness, non-sticky cooking, and delicate aroma. Net Weight: 20 KG sack.',
        'specs': {
            'Brand': 'GreenLand Food Stuff',
            'Net Weight': '20 KG Wholesale Sack',
            'Origin': 'Product of India (Thanjavur, Tamil Nadu)',
            'Variety': 'Thanjavur Aged Ponni Rice',
            'Quality': '100% Natural Aged Ponni',
            'Packaging': 'Heavy-Duty Stitched Grain Sack',
        },
        'images': [
            '/static/images/products/greenland-thanjavur-ponni-rice-20kg.png',
        ],
    },

    # =========================================================================
    # 6. 777 BRAND TRADITIONAL HERITAGE SPICES & CONDIMENTS
    # =========================================================================
    {
        'id': 'prod-777-asafoetida-100g',
        'name': '777 Compounded Asafoetida Powder (Hing 100g)',
        'category': _cat_dict('spices-and-seeds'),
        'category_slug': 'spices-and-seeds',
        'categoryName': 'Spices & Seeds',
        'brand': '777 Brand',
        'brand_code': '777',
        'price': 0.650,
        'originalPrice': 0.800,
        'weight': '100g Container',
        'unit': 'container',
        'stock': 150,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': True,
        'description': 'Famous 777 brand pure compounded asafoetida (Hing) powder. Imparts distinctive savory aroma and authentic taste to sambar, rasam, and lentil curries.',
        'specs': {
            'Brand': '777 Brand™ Heritage Spices',
            'Net Weight': '100g Container',
            'Type': 'Compounded Asafoetida (Perungayam / Hing)',
            'Origin': 'Product of India',
            'Packaging': 'Airtight Sealed Jar',
        },
        'images': [
            '/static/images/products/toor-dal-1kg.png',
        ],
    },
    {
        'id': 'prod-777-sambar-powder-500g',
        'name': '777 Authentic Madras Sambar Powder (500g)',
        'category': _cat_dict('spices-and-seeds'),
        'category_slug': 'spices-and-seeds',
        'categoryName': 'Spices & Seeds',
        'brand': '777 Brand',
        'brand_code': '777',
        'price': 1.450,
        'originalPrice': 1.750,
        'weight': '500g Pouch',
        'unit': 'retail pack',
        'stock': 110,
        'availability': 'in_stock',
        'isFeatured': True,
        'isPopular': True,
        'isNew': False,
        'description': 'Traditional South Indian Madras Sambar Powder by 777 Brand. Expertly roasted coriander, red chillies, toor dal, and aromatic whole spices for hotel-style fragrant sambar.',
        'specs': {
            'Brand': '777 Brand™ Heritage Spices',
            'Net Weight': '500 Grams',
            'Recipe': 'Traditional Madras Style Sambar',
            'Origin': 'Product of India',
            'Packaging': 'Flavor-Lock Foil Pouch',
        },
        'images': [
            '/static/images/products/88-ajwain-seeds-10kg.png',
        ],
    },
    {
        'id': 'prod-777-mango-pickle-300g',
        'name': '777 Heritage Cut Mango Thokku Pickle (300g)',
        'category': _cat_dict('canned-products'),
        'category_slug': 'canned-products',
        'categoryName': 'Canned Products',
        'brand': '777 Brand',
        'brand_code': '777',
        'price': 0.850,
        'originalPrice': 1.100,
        'weight': '300g Glass Jar',
        'unit': 'glass jar',
        'stock': 85,
        'availability': 'in_stock',
        'isFeatured': False,
        'isPopular': True,
        'isNew': False,
        'description': 'Traditional spicy home-style cut mango thokku pickle made with gingelly (sesame) oil, mustard seeds, and hand-selected raw green mangoes.',
        'specs': {
            'Brand': '777 Brand™ Heritage Spices',
            'Net Weight': '300 Grams',
            'Base Oil': 'Pure Gingelly Sesame Oil',
            'Origin': 'Product of India',
            'Packaging': 'Sealed Glass Jar',
        },
        'images': [
            '/static/images/products/tomato-paste-3kg.png',
        ],
    },
]

PRODUCTS = [ProductItem(p) for p in PRODUCTS_RAW]


# Helper query functions
def get_all_products():
    """Return all products wrapped as ProductItem."""
    return list(PRODUCTS)

def get_category_by_slug(slug):
    """Retrieve category dictionary by slug."""
    return next((c for c in CATEGORIES if c['slug'] == slug), None)

def get_product_by_id(product_id):
    """Retrieve product dictionary by ID."""
    return next((p for p in PRODUCTS if p['id'] == product_id), None)

def get_products_by_category(category_slug):
    """Retrieve all products belonging to a given category."""
    return [p for p in PRODUCTS if p['category_slug'] == category_slug]

def get_products_by_brand(brand_code):
    """Retrieve all products belonging to a given brand code."""
    return [p for p in PRODUCTS if p.get('brand_code') == brand_code]

def get_featured_products():
    """Retrieve featured products."""
    return [p for p in PRODUCTS if p.get('isFeatured')]

def get_new_arrivals(limit=4):
    """Retrieve new arrival products."""
    return [p for p in PRODUCTS if p.get('isNew')][:limit]

def get_related_products(product, limit=4):
    """Retrieve related products within the same category excluding the item itself."""
    current_cat = product.get('category_slug') if isinstance(product, dict) else ''
    current_id = product.get('id') if isinstance(product, dict) else ''
    return [p for p in PRODUCTS if p.get('category_slug') == current_cat and p.get('id') != current_id][:limit]

def filter_products(search_query='', selected_category='all', selected_brand='all', availability='all', sort_by='featured', min_price=None, max_price=None):
    """Filter in-memory static catalog by search query, category, brand, price range, and sort."""
    results = list(PRODUCTS)

    if search_query:
        sq = search_query.lower()
        results = [
            p for p in results
            if sq in p['name'].lower()
            or sq in p.get('description', '').lower()
            or sq in p.get('brand', '').lower()
            or sq in p.get('categoryName', '').lower()
        ]

    if selected_category and selected_category != 'all':
        results = [p for p in results if p.get('category_slug') == selected_category]

    if selected_brand and selected_brand != 'all':
        results = [p for p in results if p.get('brand_code') == selected_brand]

    if availability and availability != 'all':
        results = [p for p in results if p.get('availability') == availability]

    if min_price is not None:
        results = [p for p in results if float(p.get('price', 0)) >= float(min_price)]

    if max_price is not None:
        results = [p for p in results if float(p.get('price', 0)) <= float(max_price)]

    # Sorting
    if sort_by == 'price_asc':
        results = sorted(results, key=lambda x: x.get('price', 0))
    elif sort_by == 'price_desc':
        results = sorted(results, key=lambda x: x.get('price', 0), reverse=True)
    elif sort_by == 'name_asc':
        results = sorted(results, key=lambda x: x.get('name', ''))
    else:  # featured default
        results = sorted(results, key=lambda x: (not x.get('isFeatured', False), not x.get('isNew', False)))

    return results
