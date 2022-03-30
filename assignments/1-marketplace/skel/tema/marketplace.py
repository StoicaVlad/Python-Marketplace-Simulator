"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import uuid
from queue import Queue
from threading import Lock


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
        self.queue = Queue(queue_size_per_producer)
        print(self.queue.qsize())

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.no_producers += 1
        self.producers[self.no_producers] = []
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
        product_list = self.producers[producer_id]
        self.lock_producer.acquire()
        if len(product_list) == self.queue_size_per_producer:
            self.lock_producer.release()
            return False
        else:
            product_list.append(product)
            self.lock_producer.release()
            return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.no_carts += 1
        self.carts[self.no_carts] = []
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
        index = -1
        self.lock_consumer.acquire()
        for i in range(0, self.no_producers):
            for p in self.producers[i]:
                if p == product:
                    index = i
                    break

        if index >= 0:
            self.producers[index].remove(product)
            self.carts[cart_id].append(product)
            self.lock_consumer.release()
            return True

        self.lock_consumer.release()
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        found = False
        id_producer = -1
        self.lock_consumer.acquire()
        if product in self.carts[cart_id]:
            found = True

        if found:
            self.carts[cart_id].remove(product)
            for i in range(0, self.no_producers):
                if product in self.producers[i]:
                    id_producer = i
            if id_producer >= 0:
                self.producers[id_producer].append(product)
        self.lock_consumer.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts[cart_id].copy()
