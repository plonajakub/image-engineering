from typing import List


class Product:

    def __init__(self, price, name, quantity):
        self.price = price
        self.name = name
        self.quantity = quantity
        print('Constructed object ' + str(self))

    def __str__(self):
        return 'Product({}, {}, {})'.format(self.price, self.name, self.quantity)

    def get_price(self):
        print('Get price, self.price = {}'.format(self.price))
        return self.price

    def get_name(self):
        print('Get name, self.name = {}'.format(self.name))
        return self.name

    def get_quantity(self):
        print('Get quantity, self.quantity = {}'.format(self.quantity))
        return self.quantity

    def set_price(self, price):
        self.price = price
        print('Set price, self.price = {}'.format(self.price))

    def set_name(self, name):
        self.name = name
        print('Set name, self.name = {}'.format(self.name))

    def set_quantity(self, quantity):
        self.quantity = quantity
        print('Set quantity, self.quantity = {}'.format(self.quantity))


class Shop:

    def __init__(self, products: List[Product]):
        self.products = {p.name: p for p in products}
        self.products_keys = list(self.products.keys())
        self.it_pos = 0
        print('Constructed object ' + str(self))

    def __str__(self):
        shop_str = 'Shop:\n'
        for v in self.products.values():
            shop_str += '\t*' + str(v) + '\n'
        return shop_str

    def __len__(self):
        return sum(p.quantity for p in self.products.values())

    def __iter__(self):
        self.it_pos = 0
        return self

    def __next__(self):
        if self.it_pos >= len(self.products_keys):
            raise StopIteration
        next_product = self.products[self.products_keys[self.it_pos]]
        self.it_pos += 1
        return next_product

    def buy(self, p_name):
        self.products[p_name].quantity += 1
        print('{} bought, current quantity: {}'.format(p_name, self.products[p_name].quantity))

    def sell(self, p_name):
        if self.products[p_name].quantity < 1:
            print('There is no {} to sell!'.format(p_name))
            return
        self.products[p_name].quantity -= 1
        print('{} sold, current quantity: {}'.format(p_name, self.products[p_name].quantity))

    def get_total_price(self):
        print('Calculating total product value...')
        return sum(p.quantity * p.price for p in self.products.values())


if __name__ == '__main__':
    my_products = [Product(3, 'bread', 50),
                   Product(2, 'milk', 100),
                   Product(10, 'toilet paper', 0)]
    my_shop = Shop(my_products)

    my_shop.buy('toilet paper')
    my_shop.sell('milk')
    print('Total product value = {}'.format(my_shop.get_total_price()))
    print('Shop has {} products in total'.format(len(my_shop)))

    shop_it = iter(my_shop)
    print('Iterator next No. 1: ' + str(next(shop_it)))
    print('Iterator next No. 2: ' + str(next(shop_it)))
    print('Iterator next No. 3: ' + str(next(shop_it)))
    try:
        print('Iterator next No. 4: ' + str(next(shop_it)))
    except StopIteration:
        print('Further iteration impossible')

    print('Iterating over my_shop in a for loop:')
    for product in my_shop:
        print('\t*' + str(product))
