from django.test import TestCase
from shop.models import Product, Order, Purchase


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Футболка", price=1000, category="Одежда")
        Product.objects.create(name="Кепка", price=500, category="Головные уборы")

    def test_correctness_types(self):
        """Поля товара имеют правильные типы"""
        tshirt = Product.objects.get(name="Футболка")
        self.assertIsInstance(tshirt.name, str)
        self.assertIsInstance(tshirt.price, int)

    def test_correctness_data(self):
        """Данные товара сохраняются корректно"""
        tshirt = Product.objects.get(name="Футболка")
        self.assertEqual(tshirt.price, 1000)
        self.assertEqual(tshirt.category, "Одежда")


class OrderTestCase(TestCase):
    def setUp(self):
        self.order = Order.objects.create(person="Иван", address="Москва")

    def test_default_total_price(self):
        """У нового заказа итоговая сумма по умолчанию равна 0"""
        self.assertEqual(self.order.total_price, 0)

    def test_str(self):
        """Дата заказа ставится автоматически, строковое представление содержит имя покупателя"""
        self.assertIsNotNone(self.order.date)
        self.assertTrue(str(self.order).startswith("Заказ от Иван"))


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.order = Order.objects.create(person="Пётр", address="Казань")
        self.jeans = Product.objects.create(name="Джинсы", price=2000, category="Одежда")
        self.cap = Product.objects.create(name="Кепка", price=500, category="Головные уборы")
        Purchase.objects.create(order=self.order, product=self.jeans)
        Purchase.objects.create(order=self.order, product=self.cap)

    def test_purchase_linked_to_order(self):
        """Покупки привязаны к заказу и доступны через order.items"""
        self.assertEqual(self.order.items.count(), 2)

    def test_cascade_delete(self):
        """При удалении заказа удаляются и его покупки"""
        self.order.delete()
        self.assertEqual(Purchase.objects.count(), 0)
