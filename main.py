import repository
from repository import repo
from dto import Hat
from dto import Supplier
from dto import Order
import os


def main():
    with open('./example_input/config.txt') as file:
        confing = file.readlines()
        confing = [line.rstrip().split(',') for line in confing]
        num_hats = int(confing[0][0])
        num_suppliers = int(confing[0][1])
        hats = confing[1:num_hats + 1]
        suppliers = confing[num_hats + 1: num_hats + 1 + num_suppliers + 1]
        repo.create_tables()

        print(f"suppliers: {suppliers} ")
        for supplier in suppliers:
            id = int(supplier[0])
            name = supplier[1]
            repo.suppliers.insert(Supplier(id, name))  # TODO: insert all in once

        for hat in hats:
            id = int(hat[0])
            topping = hat[1]
            supplier = int(hat[2])
            quantity = int(hat[3])
            repo.hats.insert(Hat(id, topping, supplier, quantity))  # TODO: insert all in once

        with open('./example_input/orders.txt') as file:
            orders = file.readlines()
            orders = [line.rstrip().split(',') for line in orders]

            for order_id, order in enumerate(orders, 1):
                location, topping = order[0], order[1]
                hat = repo.hats.find_first_ordered('topping', 'topping', 'supplier', 1)
                repo.orders.insert(Order(order_id, topping, hat.id))  # TODO: insert all in once


if __name__ == '__main__':
    main()
