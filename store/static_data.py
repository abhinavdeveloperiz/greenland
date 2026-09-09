# static_data.py - Greenland Foodstuff & 88 Brand Wholesale Static Data & Catalog

CATEGORIES = [
  {
    'id': 'cereals-and-legumes',
    'name': 'Cereals & Legumes',
    'slug': 'cereals-and-legumes',
    'description': '100% natural retail pulses (Toor Dal, Urad Dal) & 88 Brand commercial bulk sacks of chickpeas, moong and lentils.',
    'image': '/static/images/products/toor-dal-1kg.png',
    'itemCount': '8 Products',
    'featured': True
  },
  {
    'id': 'canned-products',
    'name': 'Canned Products',
    'slug': 'canned-products',
    'description': 'Pure double concentrated tomato paste and culinary canned essentials in commercial 3 KG tins (Box of 4).',
    'image': '/static/images/products/tomato-paste-3kg.png',
    'itemCount': '1 Product',
    'featured': True
  },
  {
    'id': 'spices-and-seeds',
    'name': 'Spices & Seeds',
    'slug': 'spices-and-seeds',
    'description': 'Aromatic whole spices and carom seeds including 88 Brand wholesale Ajwain seeds in 10 KG commercial sacks.',
    'image': '/static/images/products/88-ajwain-seeds-10kg.png',
    'itemCount': '1 Product',
    'featured': True
  },
  {
    'id': 'tea',
    'name': 'Indian Premium Tea',
    'slug': 'tea',
    'description': 'GreenLand Indian premium CTC tea blends in aroma-sealed glass jars and heavy-duty 5 KG master carry pouches.',
    'image': '/static/images/products/greenland-tea-pouch.png?v=clean2',
    'itemCount': '2 Products',
    'featured': True
  },
  {
    'id': 'rice',
    'name': 'Rice & Grains',
    'slug': 'rice',
    'description': 'Authentic Indian origin rice bags (Idli Rice, Long Grain White Rice, Palakkadan Matta & Thanjavur Ponni) in wholesale 18-20 KG bulk sacks.',
    'image': '/static/images/products/greenland-thanjavur-ponni-rice-20kg.png',
    'itemCount': '4 Products',
    'featured': True
  },
  {
    'id': 'nuts-and-dry-fruits',
    'name': 'Nuts & Dry Fruits',
    'slug': 'nuts-and-dry-fruits',
    'description': 'Premium California almonds, jumbo cashews, walnuts, raisins & wholesale dry fruits.',
    'image': '/static/images/products/88-black-chick-peas-15kg.png',
    'itemCount': 'Wholesale Supply',
    'featured': False
  },
  {
    'id': 'milk',
    'name': 'Dairy & Pantry',
    'slug': 'milk',
    'description': 'Wholesale commercial dairy powders, condensed milk, and essential pantry staples.',
    'image': '/static/images/products/greenland-tea-jar.png',
    'itemCount': 'Wholesale Supply',
    'featured': False
  }
]

PRODUCTS = [
  # =========================================================================
  # 1. GREENLAND CULINARY ESSENTIALS (Canned Products)
  # =========================================================================
  {
    'id': 'prod-gl-tomato-paste',
    'name': 'GreenLand Double Concentrated Tomato Paste (3 KG)',
    'category': 'canned-products',
    'categoryName': 'Canned Products',
    'brand': 'GreenLand Food Stuff',
    'price': 5.500,
    'originalPrice': 6.250,
    'weight': '3 KG (Box of 4)',
    'unit': 'box of 4 cans',
    'stock': 45,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '100% Pure & Natural Culinary Essential Tomato Paste by GreenLand Food Stuff. Rich crimson color and thick velvety texture prepared from vine-ripened tomatoes. Packed in heavy commercial 3 KG tins (Box of 4).',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '3 KG per Can (Box of 4)',
      'Origin / Processing': 'GreenLand Foodstuff Certified',
      'Classification': 'Culinary Essential Double Concentrated',
      'Shelf Life': '24 Months'
    },
    'images': [
      '/static/images/products/tomato-paste-3kg.png'
    ]
  },

  # =========================================================================
  # 2. GREENLAND 100% NATURAL RETAIL PACK PULSES (Cereals & Legumes)
  # =========================================================================
  {
    'id': 'prod-gl-toor-dal',
    'name': 'GreenLand Toor Dal (Split Pigeon Peas)',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': 'GreenLand Food Stuff',
    'price': 0.950,
    'originalPrice': 1.200,
    'weight': '1 KG Pouch',
    'unit': 'retail pack',
    'stock': 120,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '100% Natural split pigeon peas (Toor Dal) by GreenLand. Premium unpolished grains rich in plant protein and dietary fibre for wholesome daily nutrition and traditional culinary cooking.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '1 KG Retail Pack Pouch',
      'Origin / Processing': '100% Natural Selected Grains',
      'Nutrition': 'Rich in Protein & Fibre',
      'Common Name': 'Split Pigeon Peas (Toor Dal)'
    },
    'images': [
      '/static/images/products/toor-dal-1kg.png'
    ]
  },
  {
    'id': 'prod-gl-urad-dal',
    'name': 'GreenLand Urad Dal (Peeled Black Gram)',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': 'GreenLand Food Stuff',
    'price': 1.100,
    'originalPrice': 1.350,
    'weight': '1 KG Pouch',
    'unit': 'retail pack',
    'stock': 100,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Healthy Choice peeled black gram (Urad Dal) by GreenLand. High in natural protein, diet-friendly, and perfect for soft idli/dosa batters, dal makhani, and culinary recipes.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '1 KG Retail Pack Pouch',
      'Origin / Processing': '100% Natural Selected Grains',
      'Nutrition': 'High Protein • Diet Friendly',
      'Common Name': 'Peeled Black Gram (Urad Dal)'
    },
    'images': [
      '/static/images/products/urad-dal-1kg.png'
    ]
  },
  {
    'id': 'prod-gl-urad-split',
    'name': 'GreenLand Urad Split (Split Black Gram)',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': 'GreenLand Food Stuff',
    'price': 1.150,
    'originalPrice': 1.400,
    'weight': '1 KG Pouch',
    'unit': 'retail pack',
    'stock': 90,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': 'Healthy Choice split black gram with skin (Urad Split). Finest traditional selection with natural grain texture, rich earthy taste, and balanced aroma.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '1 KG Retail Pack Pouch',
      'Origin / Processing': '100% Natural Selected Grains',
      'Quality Grade': 'Finest Traditional Selection',
      'Common Name': 'Split Black Gram (Urad Split)'
    },
    'images': [
      '/static/images/products/urad-split-1kg.png'
    ]
  },

  # =========================================================================
  # 3. 88 BRAND WHOLESALE AGRO COMMODITIES (Commercial & Bulk Sacks)
  # =========================================================================
  {
    'id': 'prod-88-ajwain-seeds',
    'name': '88 Brand Wholesale Ajwain Seeds',
    'category': 'spices-and-seeds',
    'categoryName': 'Spices & Seeds',
    'brand': '88 Brand Wholesale',
    'price': 6.000,
    'originalPrice': 7.200,
    'weight': '10 KG Sack (Net 9.9 KG)',
    'unit': 'commercial sack',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '88 Brand premium wholesale aromatic ajwain seeds (Carom Seeds). Processed & packed in UAE in heavy-duty commercial sacks. Natural high-thymol seeds with intense fragrance and medicinal aroma.',
    'specs': {
      'Brand': '88 Brand™ Wholesale Agro Commodities',
      'Pack Size': 'Gross: 10 KG | Net: 9.9 KG',
      'Origin / Processing': 'Processed & Packed in UAE',
      'Type': 'Aromatic Spice (Carom Seeds)',
      'Packaging': 'Heavy-Duty Commercial Sack'
    },
    'images': [
      '/static/images/products/88-ajwain-seeds-10kg.png'
    ]
  },
  {
    'id': 'prod-88-black-chick-peas',
    'name': '88 Brand Wholesale Black Chick Peas',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': '88 Brand Wholesale',
    'price': 5.400,
    'originalPrice': 6.500,
    'weight': '15 KG Bulk Pack',
    'unit': 'commercial sack',
    'stock': 65,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '88 Brand wholesale premium black chick peas (Kala Chana). High protein agro commodity, machine sorted and packed in UAE in heavy-duty 15 KG sacks with transparent viewing window.',
    'specs': {
      'Brand': '88 Brand™ Wholesale Agro Commodities',
      'Gross Weight': '15 KG Bulk Pack',
      'Origin / Processing': 'Processed & Packed in UAE',
      'Grade': 'Wholesale Bulk Premium',
      'Packaging': 'Commercial Printed Bulk Sack'
    },
    'images': [
      '/static/images/products/88-black-chick-peas-15kg.png'
    ]
  },
  {
    'id': 'prod-88-chick-peas-8mm',
    'name': '88 Brand Chick Peas Kabuli 8mm',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': '88 Brand Wholesale',
    'price': 5.000,
    'originalPrice': 6.000,
    'weight': '15 KG Bulk Pack',
    'unit': 'commercial sack',
    'stock': 85,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '88 Brand standard grade 8mm Kabuli chick peas (Size 8mm). Clean, calibrated 8mm grains with high boiling yield and tender skin. Processed and packed in UAE in 15 KG sacks.',
    'specs': {
      'Brand': '88 Brand™ Wholesale Agro Commodities',
      'Grain Calibration': '8MM Standard Calibrated',
      'Gross Weight': '15 KG Bulk Pack',
      'Origin / Processing': 'Processed & Packed in UAE',
      'Packaging': 'Commercial Blue Sack with Window'
    },
    'images': [
      '/static/images/products/88-chick-peas-kabuli-8mm-15kg.png'
    ]
  },
  {
    'id': 'prod-88-chick-peas-premium',
    'name': '88 Brand Chick Peas Kabuli Premium Grade',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': '88 Brand Wholesale',
    'price': 8.000,
    'originalPrice': 9.500,
    'weight': '14/15 KG Pack',
    'unit': 'commercial sack',
    'stock': 55,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '88 Brand Premium Grade jumbo Kabuli chick peas. Selected top-tier bold grains, exceptional tenderness, high water absorption, and superior culinary presentation. Processed and packed in UAE.',
    'specs': {
      'Brand': '88 Brand™ Wholesale Agro Commodities',
      'Grade': 'Premium Grade Jumbo Selection',
      'Gross Weight': '14/15 KG Pack',
      'Origin / Processing': 'Processed & Packed in UAE',
      'Packaging': 'Heavy-Duty Commercial Blue Sack'
    },
    'images': [
      '/static/images/products/88-chick-peas-kabuli-premium-14kg.png'
    ]
  },
  {
    'id': 'prod-88-green-moong-split',
    'name': '88 Brand Green Moong Split',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': '88 Brand Wholesale',
    'price': 7.750,
    'originalPrice': 9.000,
    'weight': '15 KG Bulk Pack',
    'unit': 'commercial sack',
    'stock': 50,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': '88 Brand Selected Green Moong Split. Cleaned, uniformly split green gram lentils with high nutrient density, processed and packed in UAE in 15 KG sacks with clear product display window.',
    'specs': {
      'Brand': '88 Brand™ Wholesale Agro Commodities',
      'Gross Weight': '15 KG Bulk Pack',
      'Origin / Processing': 'Processed & Packed in UAE',
      'Selection': 'Selected Split Green Gram',
      'Packaging': 'Commercial Green Wholesale Sack'
    },
    'images': [
      '/static/images/products/88-green-moong-split-15kg.png'
    ]
  },
  {
    'id': 'prod-88-green-whole-lentils',
    'name': '88 Brand Green Whole Lentils',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals & Legumes',
    'brand': '88 Brand Wholesale',
    'price': 5.000,
    'originalPrice': 6.000,
    'weight': '15 KG Bulk Pack',
    'unit': 'commercial sack',
    'stock': 70,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': '88 Brand Selected Whole Green Lentils. Rich in dietary fiber, earthy flavor, processed and packed in UAE in heavy-duty 15 KG commercial sacks.',
    'specs': {
      'Brand': '88 Brand™ Wholesale Agro Commodities',
      'Gross Weight': '15 KG Bulk Pack',
      'Origin / Processing': 'Processed & Packed in UAE',
      'Selection': 'Selected Whole Green Lentils',
      'Packaging': 'Commercial Heavy-Duty Green Sack'
    },
    'images': [
      '/static/images/products/88-green-whole-lentils-15kg.png'
    ]
  },

  # =========================================================================
  # 4. GREENLAND INDIAN PREMIUM TEA (Tea Line)
  # =========================================================================
  {
    'id': 'prod-gl-tea-pouch-5kg',
    'name': 'GreenLand Indian Premium Tea (5 KG Master Pouch)',
    'category': 'tea',
    'categoryName': 'Indian Premium Tea',
    'brand': 'GreenLand Food Stuff',
    'price': 7.500,
    'originalPrice': 9.000,
    'weight': '5 KG Master Pouch',
    'unit': 'master pouch',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'GreenLand Indian Premium CTC Tea. High-grown estate tea blend with brisk aroma and rich reddish liquor, packed in durable 5 KG carry-handle master pouch.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Pack Size': '5 KG Master Pouch with Handle',
      'Origin': 'Indian Premium Estates',
      'Grade': 'CTC Premium Tea Blend',
      'Aroma': 'Brisk, Kadak Golden Liquor'
    },
    'images': [
      '/static/images/products/greenland-tea-pouch.png?v=clean2'
    ]
  },
  {
    'id': 'prod-gl-tea-gold-jar',
    'name': 'GreenLand Indian Premium Tea Gold (250g Glass Jar)',
    'category': 'tea',
    'categoryName': 'Indian Premium Tea',
    'brand': 'GreenLand Food Stuff',
    'price': 1.850,
    'originalPrice': 2.200,
    'weight': '250g Jar',
    'unit': 'aroma seal jar',
    'stock': 80,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'GreenLand Indian Premium Tea Gold edition. Premium CTC leaf granules packed in a sealed square glass jar with red airtight cap to lock in freshness, strength, and aroma.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '250 Grams',
      'Packaging': 'Square Airtight Aroma Seal Jar',
      'Grade': 'Gold Reserve Premium Tea',
      'Aroma': 'Intense Kadak Blend'
    },
    'images': [
      '/static/images/products/greenland-tea-jar.png?v=clean2'
    ]
  },

  # =========================================================================
  # 5. GREENLAND AUTHENTIC RICE & GRAINS (18 - 20 KG Wholesale Sacks)
  # =========================================================================
  {
    'id': 'prod-gl-idli-rice-20kg',
    'name': 'GreenLand Idli Rice (20 KG)',
    'category': 'rice',
    'categoryName': 'Rice & Grains',
    'brand': 'GreenLand Food Stuff',
    'price': 6.250,
    'originalPrice': 7.500,
    'weight': '20 KG Bulk Sack',
    'unit': 'commercial sack',
    'stock': 60,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '100% Indian Origin premium Idli Rice by GreenLand Food Stuff. Selected short, plump grains ideal for producing soft, fluffy idlis and crispy dosas with authentic fermentation. Net Weight: 20 KG wholesale sack.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '20 KG Wholesale Sack',
      'Origin': '100% Indian Origin',
      'Variety': 'South Indian Short Grain Idli Rice',
      'Usage': 'Traditional Idli & Dosa Batter',
      'Packaging': 'Heavy-Duty Stitched Grain Sack'
    },
    'images': [
      '/static/images/products/greenland-idli-rice-20kg.png'
    ]
  },
  {
    'id': 'prod-gl-long-grain-rice-19kg',
    'name': 'GreenLand Long Grain White Rice (19 KG)',
    'category': 'rice',
    'categoryName': 'Rice & Grains',
    'brand': 'GreenLand Food Stuff',
    'price': 6.800,
    'originalPrice': 8.000,
    'weight': '19 KG Bulk Sack',
    'unit': 'commercial sack',
    'stock': 75,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '100% Natural long grain white rice by GreenLand Food Stuff. Milled to perfection with non-sticky grains, bright pearl white texture, and uniform length. Ideal for mandy, biryani, and daily meals. Net Weight: 19 KG sack.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '19 KG Wholesale Sack',
      'Origin': 'Product of India',
      'Variety': 'Long Grain Pearl White Rice',
      'Grain Type': 'Long Grain Pearl White',
      'Packaging': 'Durable Woven Commercial Sack'
    },
    'images': [
      '/static/images/products/greenland-long-grain-white-rice-19kg.png'
    ]
  },
  {
    'id': 'prod-gl-palakkadan-matta-18kg',
    'name': 'GreenLand Palakkadan Matta Rice (18 KG)',
    'category': 'rice',
    'categoryName': 'Rice & Grains',
    'brand': 'GreenLand Food Stuff',
    'price': 6.500,
    'originalPrice': 7.800,
    'weight': '18 KG Bulk Sack',
    'unit': 'commercial sack',
    'stock': 50,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '100% Natural parboiled red/brown rice grown in the nutrient-dense fields of Palakkad, Kerala. Rich in vitamins, high dietary fibre, and authentic earthy flavour. Net Weight: 18 KG sack.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '18 KG Wholesale Sack',
      'Origin': 'Product of India (Palakkad, Kerala)',
      'Variety': 'Palakkadan Matta Parboiled Red Rice',
      'Nutrition': 'High Dietary Fibre & Minerals',
      'Packaging': 'Commercial Heavy-Duty Sack'
    },
    'images': [
      '/static/images/products/greenland-palakkadan-matta-rice-18kg.png'
    ]
  },
  {
    'id': 'prod-gl-thanjavur-ponni-20kg',
    'name': 'GreenLand Thanjavur Ponni Rice (20 KG)',
    'category': 'rice',
    'categoryName': 'Rice & Grains',
    'brand': 'GreenLand Food Stuff',
    'price': 7.200,
    'originalPrice': 8.500,
    'weight': '20 KG Bulk Sack',
    'unit': 'commercial sack',
    'stock': 80,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': '100% Natural Thanjavur Ponni Rice by GreenLand Food Stuff. Grown in the fertile Kaveri delta of Thanjavur. Aged for perfect softness, non-sticky cooking, and delicate aroma. Net Weight: 20 KG sack.',
    'specs': {
      'Brand': 'GreenLand Food Stuff',
      'Net Weight': '20 KG Wholesale Sack',
      'Origin': 'Product of India (Thanjavur, Tamil Nadu)',
      'Variety': 'Thanjavur Aged Ponni Rice',
      'Quality': '100% Natural Aged Ponni',
      'Packaging': 'Heavy-Duty Stitched Grain Sack'
    },
    'images': [
      '/static/images/products/greenland-thanjavur-ponni-rice-20kg.png'
    ]
  }
]

# Helper query utilities to prevent repetitive filter/lookup loops
def get_category_by_slug(slug):
    """Retrieve category dictionary by slug."""
    return next((c for c in CATEGORIES if c['slug'] == slug), None)

def get_product_by_id(product_id):
    """Retrieve product dictionary by ID."""
    return next((p for p in PRODUCTS if p['id'] == product_id), None)

def get_products_by_category(category_slug):
    """Retrieve all products belonging to a given category."""
    return [p for p in PRODUCTS if p['category'] == category_slug]

def get_related_products(product, limit=4):
    """Retrieve related products within the same category excluding the item itself."""
    return [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product['id']][:limit]
