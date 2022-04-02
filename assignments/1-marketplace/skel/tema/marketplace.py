"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock
from logging.handlers import RotatingFileHandler
import logging
import time

logger = logging.getLogger('marketplace_logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
formatter.converter = time.gmtime()

handler = RotatingFileHandler('marketplace.log', maxBytes=2500, backupCount=10)
handler.setFormatter(formatter)

logger.addHandler(handler)


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer: int):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.lock_consumer = Lock()
        self.lock_producer = Lock()

        self.producers = [[]]
        self.carts = [[]]
        self.no_producers = 0
        self.no_carts = 0

        self.queue_size_per_producer = queue_size_per_producer

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        logger.info("A new producer is registered.")
        self.no_producers += 1
        self.producers.append([])
        logger.info("Producer with id %s registerd.", self.no_producers)
        return self.no_producers

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        logger.info('Producer with id %d is publishig the product: %s', producer_id, product)
        if producer_id > self.no_producers:
            logger.error('Producer with id: %d does not exist', producer_id)
            raise ValueError("Producer does not exist!")
        product_list = self.producers[producer_id]
        with self.lock_producer:
            if len(product_list) >= self.queue_size_per_producer:
                can_publish = False
            else:
                product_list.append(product)
                can_publish = True
        logger.info("Producer published: %s", str(can_publish))
        return can_publish

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        logger.info("New cart with id %d is being created.", self.no_carts + 1)
        self.no_carts += 1
        self.carts.append([])
        return self.no_carts

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        logger.info("Cart with id %d is adding %s.", cart_id, product)
        can_add = False
        index = -1
        with self.lock_consumer:
            for i in range(0, self.no_producers):
                for prod_in_list in self.producers[i]:
                    if prod_in_list == product:
                        index = i
                        break
            if index >= 0:
                self.producers[index].remove(product)
                self.carts[cart_id].append(product)
                can_add = True

        if can_add:
            logger.info("Product was added to the cart.")
        else:
            logger.info("Product could not be added to the cart.")

        return can_add

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        logger.info("Cart with id %d is removing product %s.", cart_id, product)
        found = False
        id_producer = -1
        with self.lock_consumer:
            if product in self.carts[cart_id]:
                found = True
            if found:
                self.carts[cart_id].remove(product)
                for i in range(0, self.no_producers):
                    if product in self.producers[i]:
                        id_producer = i
                logger.info("Product was removed.")
                if id_producer >= 0:
                    self.producers[id_producer].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        logger.info("Cart with id %d placed an order.", cart_id)
        if cart_id > self.no_carts:
            logger.error("Cart with id %d is invalid!", cart_id)
            raise ValueError("Cart does not exist!")
        logger.info("Product list: %s.", self.carts[cart_id])
        return self.carts[cart_id].copy()
