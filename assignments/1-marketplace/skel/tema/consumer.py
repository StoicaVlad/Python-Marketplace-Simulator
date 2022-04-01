"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    def run(self):
        cart_id = self.marketplace.new_cart()
        for p in self.carts:
            for elem in p:
                command = elem.get("type")
                product = elem.get("product")
                quantity = elem.get("quantity")
                if command == "remove":
                    i = 0
                    while i < quantity:
                        self.marketplace.remove_from_cart(cart_id, product)
                        i += 1
                elif command == "add":
                    i = 0
                    while i < quantity:
                        no_wait = self.marketplace.add_to_cart(cart_id, product)
                        if no_wait:
                            i += 1
                        else:
                            time.sleep(self.retry_wait_time)
        order = self.marketplace.place_order(cart_id)
        for prod in order:
            print(self.name, "bought", prod)
