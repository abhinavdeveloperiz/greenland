# static_data.py - Greenland Foodstuff Static Data & Catalog

CATEGORIES = [
  {
    'id': 'spices-and-seeds',
    'name': 'Spices and seeds',
    'slug': 'spices-and-seeds',
    'description': 'Pure stone-ground single-origin spices, aromatic powders & whole seeds.',
    'image': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80',
    'itemCount': '24+ Items',
    'featured': True
  },
  {
    'id': 'cereals-and-legumes',
    'name': 'Cereals and legumes',
    'slug': 'cereals-and-legumes',
    'description': 'Protein-dense unpolished pulses, whole dals, hearty grains & wholesome cereals.',
    'image': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=600&q=80',
    'itemCount': '20+ Items',
    'featured': True
  },
  {
    'id': 'rice',
    'name': 'Rice',
    'slug': 'rice',
    'description': 'Aged royal basmati, daily sonamasuri, seeraga samba & harvest brown rice.',
    'image': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80',
    'itemCount': '18+ Items',
    'featured': True
  },
  {
    'id': 'nuts-and-dry-fruits',
    'name': 'Nuts and dry fruits',
    'slug': 'nuts-and-dry-fruits',
    'description': 'Hand-picked California almonds, jumbo cashews, walnuts, raisins & pistachios.',
    'image': 'https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?auto=format&fit=crop&w=600&q=80',
    'itemCount': '22+ Items',
    'featured': True
  },
  {
    'id': 'milk',
    'name': 'Milk',
    'slug': 'milk',
    'description': 'Farm fresh full cream UHT milk, traditional desi A2 cow milk & coconut milk.',
    'image': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=600&q=80',
    'itemCount': '12+ Items',
    'featured': True
  },
  {
    'id': 'tea',
    'name': 'Tea',
    'slug': 'tea',
    'description': 'Green Land Indian premium CTC tea blends, Assam golden leaf & herbal kahwa.',
    'image': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=600&q=80',
    'itemCount': '16+ Items',
    'featured': True
  },
  {
    'id': 'canned-products',
    'name': 'Canned products',
    'slug': 'canned-products',
    'description': 'Sealed golden sweet corn, alphonso mango pulp, plum tomatoes & legumes.',
    'image': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80',
    'itemCount': '15+ Items',
    'featured': True
  }
]

PRODUCTS = [
  # =========================================================================
  # 1. SPICES AND SEEDS
  # =========================================================================
  {
    'id': 'prod-spice-01',
    'name': 'Salem Pure Golden Turmeric Powder',
    'category': 'spices-and-seeds',
    'categoryName': 'Spices and seeds',
    'price': 145,
    'originalPrice': 180,
    'weight': '500g',
    'unit': 'pouch',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'High-curcumin (3.5%+) pure single-origin turmeric powder grown in Salem, Tamil Nadu. Cold stone ground to preserve beneficial antioxidants and intense natural aroma.',
    'specs': {
      'Curcumin Content': 'Min 3.5% Certified',
      'Origin': 'Salem, Tamil Nadu',
      'Processing': 'Slow Stone Ground (Unheated)',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-spice-02',
    'name': 'Guntur Stemless Red Chilli Powder',
    'category': 'spices-and-seeds',
    'categoryName': 'Spices and seeds',
    'price': 160,
    'originalPrice': 195,
    'weight': '500g',
    'unit': 'pouch',
    'stock': 35,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Finely powdered stemless Guntur Sannam chillies. Yields a deep crimson red curry color with sharp, balanced heat and zero artificial colorants or adulterants.',
    'specs': {
      'Pungency Rating': 'Medium-Hot (35,000 SHU)',
      'Origin': 'Guntur, Andhra Pradesh',
      'Purity': '100% Stemless Pure Pods',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-spice-03',
    'name': 'Malabar Whole Black Peppercorns & Cumin Seeds',
    'category': 'spices-and-seeds',
    'categoryName': 'Spices and seeds',
    'price': 220,
    'originalPrice': 260,
    'weight': '250g',
    'unit': 'pack',
    'stock': 30,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': 'Sun-dried jumbo Tellicherry black peppercorns paired with aromatic Rajasthani jeera seeds. Essential whole pantry spice pairing for daily tempering and gravies.',
    'specs': {
      'Grade': 'Tellicherry Garbled Extra Bold (TGEB)',
      'Origin': 'Wayanad, Kerala & Jodhpur, Rajasthan',
      'Moisture': '< 10%',
      'Shelf Life': '18 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-spice-04',
    'name': 'Royal Green Cardamom Pods (Elaichi)',
    'category': 'spices-and-seeds',
    'categoryName': 'Spices and seeds',
    'price': 380,
    'originalPrice': 450,
    'weight': '100g',
    'unit': 'jar',
    'stock': 28,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': False,
    'description': '8mm+ jumbo green cardamom pods from the high altitudes of Idukki. Bursting with sweet camphoraceous oils, ideal for premium tea, biryani, and festive sweets.',
    'specs': {
      'Pod Size': '8mm Jumbo Bold',
      'Origin': 'Idukki Hills, Kerala',
      'Color': 'Natural Lush Green (Unbleached)',
      'Shelf Life': '24 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80'
    ]
  },

  # =========================================================================
  # 2. CEREALS AND LEGUMES
  # =========================================================================
  {
    'id': 'prod-legume-01',
    'name': 'Unpolished Desi Toor Dal (Pigeon Pea)',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals and legumes',
    'price': 175,
    'originalPrice': 210,
    'weight': '1kg',
    'unit': 'bag',
    'stock': 50,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Pure unpolished Desi toor dal sourced directly from Latur farmers. Natural dehulling without oil, water, or marble powder polish keeps natural protein intact.',
    'specs': {
      'Purity': '100% Unpolished & Oil-Free',
      'Protein': '22g per 100g',
      'Origin': 'Latur, Maharashtra',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-legume-02',
    'name': 'Organic Whole Moong Beans (Green Gram)',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals and legumes',
    'price': 160,
    'originalPrice': 190,
    'weight': '1kg',
    'unit': 'bag',
    'stock': 35,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': 'Small-grained, tender whole green moong beans excellent for high-yield nutrient sprouting, hearty gravies, and light dietary khichdi.',
    'specs': {
      'Type': 'Sabut Green Moong',
      'Sprout Rate': '95%+ High Germination',
      'Origin': 'Madhya Pradesh',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-legume-03',
    'name': 'Premium Jumbo Kabuli Chickpeas (Chole)',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals and legumes',
    'price': 195,
    'originalPrice': 240,
    'weight': '1kg',
    'unit': 'bag',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': False,
    'description': 'Extra-large 12mm Kabuli chana that cooks into melt-in-the-mouth, buttery chickpeas. Perfect for Amritsari chole, salads, and fresh hummus.',
    'specs': {
      'Size': '12mm Extra Jumbo Count',
      'Origin': 'Indore, Madhya Pradesh',
      'Cooking Time': '35 mins after overnight soak',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1587486913049-53fc88980cfc?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-legume-04',
    'name': 'Golden Whole Rolled Oats & Multi-Millet Cereal',
    'category': 'cereals-and-legumes',
    'categoryName': 'Cereals and legumes',
    'price': 225,
    'originalPrice': 270,
    'weight': '1kg',
    'unit': 'pack',
    'stock': 25,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': 'Heart-healthy blend of steamed rolled oats combined with ragi, bajra, and jowar flakes. High in soluble beta-glucan fiber and sustained energy.',
    'specs': {
      'Grains': 'Rolled Oats, Ragi, Bajra, Jowar',
      'Fiber Content': '11g per 100g',
      'Dietary': 'No Added Sugar or Preservatives',
      'Shelf Life': '9 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80'
    ]
  },

  # =========================================================================
  # 3. RICE
  # =========================================================================
  {
    'id': 'prod-rice-01',
    'name': 'Royal Heritage Extra Long Basmati Rice',
    'category': 'rice',
    'categoryName': 'Rice',
    'price': 349,
    'originalPrice': 420,
    'weight': '5kg',
    'unit': 'bag',
    'stock': 45,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Aged for two years in Himalayan foothills to ensure distinct, non-sticky, fluffiest grains with a signature aroma. Elongates to over 24mm upon cooking.',
    'specs': {
      'Grain Type': '1121 Super Long Grain Aged Basmati',
      'Aging': '24 Months Naturally Aged',
      'Origin': 'Dehradun Valley, Uttarakhand',
      'Shelf Life': '24 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-rice-02',
    'name': 'Greenland Daily Sona Masoori Raw Rice',
    'category': 'rice',
    'categoryName': 'Rice',
    'price': 650,
    'originalPrice': 740,
    'weight': '10kg',
    'unit': 'bag',
    'stock': 60,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Lightweight, aromatic medium-grain rice cultivated along the Tungabhadra river basin. Naturally low in starch and ideal for everyday meals, rasam, and sambar rice.',
    'specs': {
      'Grain Type': 'Medium Fine Sona Masoori',
      'Cultivation': 'Kurnool Delta Basin',
      'Starch Index': 'Low Glycemic Friendly',
      'Shelf Life': '18 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-rice-03',
    'name': 'Kerala Palakkadan Matta Brown Rice',
    'category': 'rice',
    'categoryName': 'Rice',
    'price': 280,
    'originalPrice': 330,
    'weight': '5kg',
    'unit': 'bag',
    'stock': 30,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': False,
    'description': 'Nutrient-dense parboiled red rice with rich pericarp outer layer. Earthy flavor, chewy texture, packed with dietary magnesium and zinc.',
    'specs': {
      'Grain Type': 'Bold Parboiled Red Matta',
      'Origin': 'Palakkad, Kerala',
      'Nutrition': 'High Fiber & Minerals',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=800&q=80'
    ]
  },

  # =========================================================================
  # 4. NUTS AND DRY FRUITS
  # =========================================================================
  {
    'id': 'prod-nut-01',
    'name': 'Premium California Whole Almonds (Badam Giri)',
    'category': 'nuts-and-dry-fruits',
    'categoryName': 'Nuts and dry fruits',
    'price': 440,
    'originalPrice': 520,
    'weight': '500g',
    'unit': 'pouch',
    'stock': 45,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Crisp, whole jumbo Nonpareil California almonds rich in Vitamin E, dietary magnesium, and protein. Vacuum nitrogen flushed for enduring garden-fresh crunch.',
    'specs': {
      'Grade': 'California Nonpareil Extra #1',
      'Nutrients': 'High Vitamin E & Heart-Healthy Fats',
      'Packaging': 'Resealable Zip Foil Pouch',
      'Shelf Life': '9 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1508061253366-f7da158b6d46?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-nut-02',
    'name': 'Royal King Cashew Nuts (Kaju W240)',
    'category': 'nuts-and-dry-fruits',
    'categoryName': 'Nuts and dry fruits',
    'price': 520,
    'originalPrice': 610,
    'weight': '500g',
    'unit': 'pouch',
    'stock': 35,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Grade W240 whole king cashews with a rich buttery taste and sweet natural finish. Sourced from Mangalore estates, unsalted and unroasted for versatile cooking.',
    'specs': {
      'Grade': 'White Whole 240 (W240)',
      'Origin': 'Coastal Karnataka',
      'Taste': 'Naturally Sweet & Creamy',
      'Shelf Life': '9 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1508061253366-f7da158b6d46?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-nut-03',
    'name': 'Kashmiri Walnut Kernels (Akhrot Giri)',
    'category': 'nuts-and-dry-fruits',
    'categoryName': 'Nuts and dry fruits',
    'price': 490,
    'originalPrice': 580,
    'weight': '500g',
    'unit': 'pack',
    'stock': 28,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': 'Light-amber Kashmiri walnut halves packed with plant-based Omega-3 fatty acids. Tender, sweet, and free from bitter aftertaste.',
    'specs': {
      'Variety': 'Kashmir Snow Halves',
      'Omega-3': '2.5g ALA per 28g serving',
      'Origin': 'Anantnag, Kashmir Valley',
      'Shelf Life': '6 Months (Store Cold)'
    },
    'images': [
      'https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-nut-04',
    'name': 'Golden Afghani Seedless Raisins (Kismis)',
    'category': 'nuts-and-dry-fruits',
    'categoryName': 'Nuts and dry fruits',
    'price': 195,
    'originalPrice': 240,
    'weight': '500g',
    'unit': 'pouch',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': False,
    'description': 'Long green and golden seedless raisins naturally sun-dried in Kandahar vineyards. Chewy, luscious, and rich in natural iron and dietary energy.',
    'specs': {
      'Type': 'Kandahar Long Green Kismis',
      'Treatment': 'No Added Sugar / Sulphur-Free',
      'Origin': 'Afghani Vineyards',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?auto=format&fit=crop&w=800&q=80'
    ]
  },

  # =========================================================================
  # 5. MILK
  # =========================================================================
  {
    'id': 'prod-milk-01',
    'name': 'Pure Farm Fresh UHT Full Cream Milk',
    'category': 'milk',
    'categoryName': 'Milk',
    'price': 85,
    'originalPrice': 95,
    'weight': '1L',
    'unit': 'tetra-pack',
    'stock': 70,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Homogenized, ultra-heat treated full cream milk sourced from grass-fed dairy cattle. Rich in natural calcium, vitamin D, and essential proteins with no preservative additives.',
    'specs': {
      'Fat Content': '6.0% Rich Cream',
      'SNF (Solid-Not-Fat)': '9.0% Min',
      'Sterilization': 'Aseptic UHT Technology',
      'Shelf Life': '6 Months (Unopened)'
    },
    'images': [
      'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-milk-02',
    'name': 'Traditional Pure Desi A2 Cow Milk',
    'category': 'milk',
    'categoryName': 'Milk',
    'price': 120,
    'originalPrice': 140,
    'weight': '1L',
    'unit': 'bottle',
    'stock': 35,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Nutrient-rich A2 beta-casein milk obtained exclusively from indigenous Gir and Sahiwal cows. Gentle on digestion, easy to assimilate, and deeply nourishing.',
    'specs': {
      'Protein Type': '100% Certified A2 Beta-Casein',
      'Cattle Breed': 'Indigenous Gir Cow',
      'Homogenization': 'Gently Pasteurized',
      'Shelf Life': '5 Days (Refrigerated)'
    },
    'images': [
      'https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-milk-03',
    'name': 'Creamy Thick Coconut Milk (First Extract)',
    'category': 'milk',
    'categoryName': 'Milk',
    'price': 135,
    'originalPrice': 160,
    'weight': '400ml',
    'unit': 'tin',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': False,
    'description': 'Thick, luscious first-press coconut milk squeezed from fresh matured Malabar coconuts. Lactose-free, dairy-free base for Thai curries, Kerala stews, and desserts.',
    'specs': {
      'Extract': 'First Cold-Press Coconut Milk',
      'Fat Content': '18% Natural Coconut Cream',
      'Dietary': '100% Vegan & Dairy-Free',
      'Shelf Life': '18 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=800&q=80'
    ]
  },

  # =========================================================================
  # 6. TEA
  # =========================================================================
  {
    'id': 'prod-tea-01',
    'name': 'Green Land Indian Premium Tea (5kg Master Pack)',
    'category': 'tea',
    'categoryName': 'Tea',
    'price': 780,
    'originalPrice': 920,
    'weight': '5kg',
    'unit': 'master-pack',
    'stock': 50,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'The signature flagship Green Land blend! High-grown Assam CTC granules blended with tender Darjeeling orthodox leaves. Yields a brisk amber-golden liquor, malt aroma, and rich, invigorating body.',
    'specs': {
      'Blend Type': 'CTC Grain & Orthodox Golden Leaves',
      'Packaging': 'Heavy-Duty 5kg Commercial Foil Sack',
      'Strength': 'Strong Kadak with Malty Finish',
      'Shelf Life': '24 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-tea-02',
    'name': 'Assam Gold CTC Strong Kadak Tea',
    'category': 'tea',
    'categoryName': 'Tea',
    'price': 180,
    'originalPrice': 220,
    'weight': '500g',
    'unit': 'pouch',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Selected from second-flush Upper Assam gardens. Deep red-coppery cup with robust strength, ideally matched for Indian spiced masala chai with milk and cardamom.',
    'specs': {
      'Estate': 'Upper Assam Brahmaputra Valley',
      'Grade': 'BOPL Extra Strong Granules',
      'Cupping Notes': 'Malty, Brisk, Full Bodied',
      'Shelf Life': '18 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-tea-03',
    'name': 'Darjeeling First Flush Muscatel Black Tea',
    'category': 'tea',
    'categoryName': 'Tea',
    'price': 340,
    'originalPrice': 410,
    'weight': '250g',
    'unit': 'tin',
    'stock': 25,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': False,
    'description': 'The champagne of teas! Hand-plucked tender two leaves and a bud from 6,000ft high Himalayan slopes. Delicate pale amber brew with floral notes and muscatel grape finish.',
    'specs': {
      'Grade': 'FTGFOP-1 Whole Leaf',
      'Flush': 'Spring First Flush',
      'Elevation': '6,200 Feet Darjeeling',
      'Shelf Life': '24 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-tea-04',
    'name': 'Kashmiri Shahi Saffron Green Tea (Kahwa)',
    'category': 'tea',
    'categoryName': 'Tea',
    'price': 295,
    'originalPrice': 360,
    'weight': '250g',
    'unit': 'jar',
    'stock': 30,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': 'Traditional royal Kashmiri kahwa combining pure green tea leaves with whole saffron strands, crushed cardamom, cinnamon bark, and rose petals.',
    'specs': {
      'Ingredients': 'Green Tea, Kashmiri Kesar, Cardamom, Cinnamon',
      'Caffeine': 'Low / Gentle Revitalizer',
      'Origin': 'Srinagar, Kashmir',
      'Shelf Life': '12 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=800&q=80'
    ]
  },

  # =========================================================================
  # 7. CANNED PRODUCTS
  # =========================================================================
  {
    'id': 'prod-can-01',
    'name': 'Sweet Golden Corn Kernels in Brine',
    'category': 'canned-products',
    'categoryName': 'Canned products',
    'price': 95,
    'originalPrice': 115,
    'weight': '400g',
    'unit': 'can',
    'stock': 60,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Crisp, naturally tender sweet corn picked at the peak of sweetness and hermetically sealed in light sea-salt brine within hours of harvest.',
    'specs': {
      'Net Weight': '400g (Drained Wt: 250g)',
      'Processing': 'Non-GMO Fresh Harvest Steam Packed',
      'Preservatives': 'Zero Chemical Additives',
      'Shelf Life': '24 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-can-02',
    'name': 'Canned Royal Alphonso Mango Pulp',
    'category': 'canned-products',
    'categoryName': 'Canned products',
    'price': 185,
    'originalPrice': 225,
    'weight': '850g',
    'unit': 'tin',
    'stock': 45,
    'availability': 'in_stock',
    'isFeatured': True,
    'isPopular': True,
    'description': 'Prepared 100% from tree-ripened Ratnagiri Alphonso (Hapus) mangoes. Luscious golden-orange pulp for homemade aamras, mango lassi, kulfi, and desserts.',
    'specs': {
      'Mango Variety': '100% Ratnagiri Alphonso',
      'Sugar Level': 'Natural Sweetness + Minimal Cane Syrup',
      'Origin': 'Konkan Coast, Maharashtra',
      'Shelf Life': '24 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-can-03',
    'name': 'Peeled Plum Italian Tomatoes in Rich Puree',
    'category': 'canned-products',
    'categoryName': 'Canned products',
    'price': 140,
    'originalPrice': 175,
    'weight': '800g',
    'unit': 'can',
    'stock': 35,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': True,
    'description': 'Whole sun-ripened plum tomatoes steam-peeled and submerged in rich, savory tomato coulis. Authentic robust acid-sweet base for pasta sauces and stews.',
    'specs': {
      'Tomato Type': '100% Italian San Marzano Style Plum',
      'Pack': 'BPA-Free Lined Can',
      'Ingredients': 'Tomatoes, Tomato Juice, Sea Salt',
      'Shelf Life': '36 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?auto=format&fit=crop&w=800&q=80'
    ]
  },
  {
    'id': 'prod-can-04',
    'name': 'Premium Red Kidney Beans (Rajma) in Savoury Brine',
    'category': 'canned-products',
    'categoryName': 'Canned products',
    'price': 110,
    'originalPrice': 135,
    'weight': '400g',
    'unit': 'can',
    'stock': 40,
    'availability': 'in_stock',
    'isFeatured': False,
    'isPopular': False,
    'description': 'Pre-soaked, tender cooked dark red kidney beans canned at source. Ready to toss into quick Punjabi rajma masala, salads, chili, and wraps without boiling delay.',
    'specs': {
      'Net Weight': '400g (Drained Wt: 240g)',
      'Convenience': 'Pre-Cooked, Heat & Serve',
      'Origin': 'Himachal Highlands',
      'Shelf Life': '24 Months'
    },
    'images': [
      'https://images.unsplash.com/photo-1597362925123-77861d3fbac7?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=800&q=80'
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
