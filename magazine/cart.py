# -*- coding: utf-8 -*-

from decimal import Decimal
from django.conf import settings


from magazine.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # self.cart = self.session.get(settings.CART_SESSION_ID, False) or {}
        self.update()

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['count'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['discount'] = int(item['discount'])
            if item['discount'] == 0:
                item['total_price'] = item['price'] * item['count']
            elif item['discount'] > 0:
                discount_price = item['price'] - (item['price']/100) * item['discount']
                item['total_price'] = discount_price * item['count']
            yield item

    def update(self):
        """

        """
        cart_ids = self.cart.keys()
        products = Product.objects.filter(id__in=cart_ids)
        p_ids = [str(i.id) for i in products]
        if cart_ids.sort() is p_ids.sort():
            tmp_cart = self.cart
            self.clear()
            for product in products:
                self.add(product, tmp_cart[str(product.id)]['count'], True)

    def add(self, product, count=1, update_count=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': 0,
                                     'price': str(product.price),
                                     'discount': str(product.discount)}
        if update_count:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
        self.cart = self.session[settings.CART_SESSION_ID]

    def get_total_price(self):
        return sum(Decimal(item['total_price']) for item in self.cart.values())
