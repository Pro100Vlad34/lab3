from django.test import TestCase, Client
from shop.models import Product, Purchase
from shop.views import PurchaseCreate


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(name="Футболка", price=1000, category="Одежда")

    def test_view_config(self):
        """Представление настроено на модель Purchase и после покупки ведёт на главную"""
        self.assertIs(PurchaseCreate.model, Purchase)
        self.assertEqual(PurchaseCreate.success_url, '/')

    def test_webpage_accessibility(self):
        """Главная страница доступна и показывает список товаров"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')
        self.assertEqual(len(response.context['products']), 1)
