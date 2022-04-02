"""File for unit tests"""
import unittest
from marketplace import Marketplace
from product import Product


class MarketplaceTestCase(unittest.TestCase):
    """Test class for Marketplace"""

    product_test = Product("coffee", 10)
    marketplace = Marketplace(4)

    def test_place_order_exception(self):
        """Place order method test with exception"""
        marketplace = Marketplace(2)
        self.assertRaises(ValueError, marketplace.place_order, 1)

    def test_place_order(self):
        """Place order method test"""
        self.marketplace.carts = [[self.product_test]]
        self.marketplace.no_carts = 1
        response = self.marketplace.place_order(0)
        expected = [self.product_test]
        self.assertEqual(response, expected)

    def test_register_producer(self):
        """Register producer test"""
        marketplace = Marketplace(10)
        result = marketplace.register_producer()
        self.assertEqual(result, 1)

    def test_publish_exception(self):
        """Test publish method with exception"""
        marketplace = Marketplace(5)
        self.assertRaises(ValueError, marketplace.publish, 2, Product("coffee", 10))

    def test_publish_method(self):
        """Test publish method"""
        self.marketplace.register_producer()
        result = self.marketplace.publish(1, self.product_test)
        self.assertEqual(result, True)

    def test_publish_method_false(self):
        """
        Test publish method when a product can't be added
        """
        self.marketplace.register_producer()
        for _ in range(0, 4):
            self.marketplace.publish(1, self.product_test)
        response = self.marketplace.publish(1, self.product_test)
        self.assertEqual(response, False)

    def test_new_cart(self):
        """Test for adding a new cart"""
        marketplace = Marketplace(2)
        result = marketplace.new_cart()
        self.assertEqual(result, 1)

    def test_add_cart(self):
        """Test for adding a product to the cart"""
        self.marketplace.register_producer()
        self.marketplace.publish(0, self.product_test)
        self.marketplace.new_cart()
        result = self.marketplace.add_to_cart(1, self.product_test)
        self.assertEqual(result, True)

    def test_add_cart_false(self):
        """Test for adding an invalid product to the cart"""
        self.marketplace.register_producer()
        self.marketplace.new_cart()
        result = self.marketplace.add_to_cart(1, self.product_test)
        self.assertEqual(result, False)

    def test_remove_from_cart(self):
        """Test for cart removal; none value is returned as the function does not return anything"""
        self.marketplace.register_producer()
        self.marketplace.publish(0, self.product_test)
        self.marketplace.new_cart()
        self.assertIsNone(self.marketplace.remove_from_cart(0, self.product_test))


if __name__ == '__main__':
    unittest.main()
