from repository import repo
from dto import Hat
from dto import Supplier
from dto import Order
import sys


def main():
    config = None
    try:
        # load hats and suppliers
        with open(sys.argv[1]) as config_file:
            config = config_file.readlines()
            config = [line.rstrip().split(',') for line in config]
    except IOError as e:
        print("failed to load the config file, exception: ", e)
        return

    #  loading the config file has succeed
    num_hats = int(config[0][0])
    num_suppliers = int(config[0][1])
    hats = config[1:num_hats + 1]
    suppliers = config[num_hats + 1: num_hats + 1 + num_suppliers + 1]
    repo.create_tables()

    for supplier in suppliers:
        id = int(supplier[0])
        name = supplier[1]
        repo.suppliers.insert(Supplier(id, name))

    for hat in hats:
        id = int(hat[0])
        topping = hat[1]
        supplier = int(hat[2])
        quantity = int(hat[3])
        repo.hats.insert(Hat(id, topping, supplier, quantity))

    orders = None
    try:
        #  load orders
        with open(sys.argv[2]) as orders_file:
            orders = orders_file.readlines()
            orders = [line.rstrip().split(',') for line in orders]


    except IOError as e:
        print("failed to load the orders file, exception: ", e)
        return

    #  loading the config file has succeed

    try:
        # creating the output file:
        with open(sys.argv[3], 'w') as output_file:
            for order_index, order in enumerate(orders, 1):
                location, topping = order[0], order[1]
                hat = repo.hats.find_first_ordered('topping', topping, 'supplier', 1)[0]
                repo.orders.insert(Order(order_index, location, hat.id))

                supplier_name = repo.suppliers.find(id=hat.supplier)[0].name
                output_file.write(f"{topping},{supplier_name},{location}\n")

                if hat.quantity == 1:  # last hat
                    repo.hats.delete(id=hat.id)
                else:
                    repo.hats.update({'quantity': hat.quantity - 1}, {'id': hat.id})

    except IOError as e:
        print("failed to open output file, exception: ", e)
        return

    except Exception as e:
        print("failed to execute the orders, exception: ", e)
        return


if __name__ == '__main__':
    main()
