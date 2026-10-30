from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, ProductVariant


class ProductDetailTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Pantry', slug='pantry')
        self.product = Product.objects.create(
            id='test-product',
            name='Test Product',
            category=self.category,
            price='1.500',
            weight='500 g',
        )

    def test_product_detail_uses_active_variant_data(self):
        variant = ProductVariant.objects.create(
            product=self.product,
            weight='1 kg',
            price='2.500',
            stock=3,
            is_default=True,
        )

        response = self.client.get(
            reverse('store:product_detail', args=[self.product.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['default_variant_data']['id'], variant.id)
        self.assertEqual(response.context['default_variant_data']['stock'], 3)
        self.assertContains(response, 'Pantry')
        self.assertContains(response, 'product-images-data')

    def test_unknown_or_inactive_product_returns_404(self):
        response = self.client.get(
            reverse('store:product_detail', args=['missing-product'])
        )
        self.assertEqual(response.status_code, 404)

        self.product.is_active = False
        self.product.save(update_fields=['is_active'])
        response = self.client.get(
            reverse('store:product_detail', args=[self.product.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_homepage_categories_only_include_greenland_products(self):
        other_brand_category = Category.objects.create(
            name='Other Brand',
            slug='other-brand',
        )
        Product.objects.create(
            id='other-product-same-category',
            name='Other brand pantry product',
            category=self.category,
            brand_code='88',
        )
        Product.objects.create(
            id='other-product-category',
            name='Other brand category product',
            category=other_brand_category,
            brand_code='777',
        )

        response = self.client.get(reverse('store:home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [category.id for category in response.context['categories']],
            [self.category.id],
        )
        self.assertEqual(response.context['categories'][0].active_count, 1)

    def test_admin_can_edit_product_and_variant_inventory(self):
        variant = ProductVariant.objects.create(
            product=self.product,
            weight='500 g',
            price='1.500',
            stock=4,
        )
        admin_user = get_user_model().objects.create_superuser(
            username='store-admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(admin_user)

        response = self.client.get(
            reverse('admin:store_product_change', args=[self.product.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'availability')
        self.assertContains(response, 'stock')
        self.assertContains(response, '500 g')
        self.assertTrue(ProductVariant.objects.filter(pk=variant.pk).exists())
