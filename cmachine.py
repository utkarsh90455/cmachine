import requests


class CoffeMachine:
    """
    Class for CoffeeMachine
    """

    def __init__(self, total_quantity, beverages):
        """
        initializing the object with data
        :param total_quantity: 
        :param beverages: 
        """
        self.total_items_quantity = total_quantity  # total quantity
        self.total_capacity = total_quantity.copy()  # total capacity if need to refill
        self.beverages = beverages  # allowed beverages
        self.max_item_quantity = dict()  # max required quantity for items
        for item in beverages.values():
            for item_name, item_val in item.items():
                if self.max_item_quantity.get(item_name, 0) < item_val:
                    self.max_item_quantity[item_name] = item_val

    def prepare(self, beverage_option):
        """
        prepare beverage
        :param beverage_option: 
        :return: 
        """
        beverage = self.beverages.get(beverage_option, {})
        if not beverage:
            return "This machine dosent support this beverage"
        less_quantity_flag, less_quantities = False, []
        for item, val in beverage.items():  # check if quantity is less than required quantity
            if self.total_items_quantity.get(item, 0) < val:
                less_quantity_flag = True
                less_quantities.append(item)
        if less_quantity_flag:
            return beverage_option + " cannot be prepared because " + ",".join(less_quantities) + " is not available"
        for item, val in beverage.items():
            if self.total_items_quantity.get(item, 0) >= val:
                self.total_items_quantity[item] = self.total_items_quantity[item] - val
        self.check_for_refill()  # when beverage is prepared check if refill required or not
        return beverage_option + " is prepared"

    def check_for_refill(self):
        """
        check if refill required or not
        :return: 
        """
        item_to_refill = []
        for item, item_val in self.total_items_quantity.items():
            # print(item, item_val, self.max_item_quantity.get(item, 0))
            if self.max_item_quantity.get(item, 0) > item_val or item_val == 0:
                item_to_refill.append(item)

        if item_to_refill:
            print("***Please refill " + ",".join(item_to_refill) + "***")


def parse_validate_data(data):
    """
    process the input data parsing and check validation
    :param data: 
    :return: 
    """
    total_quantity, beverages, error = {}, {}, False
    if not data:
        error = True
        print("Not a valid input data !")
        return (total_quantity, beverages)
    machine = data.get('machine', {})
    if not machine:
        error = True
        print("Not a valid input data !")
    total_quantity = machine.get('total_items_quantity') or {}
    beverages = machine.get('beverages') or {}
    # checking data if present or not
    if not total_quantity:
        error = True
        print("Total Quantity is missing !")
    if not beverages:
        error = True
        print("Beverages is missing !")
    outlets = machine.get('outlets', {}).get('count_n', 0) or 0
    if not outlets or outlets != len(beverages):
        error = True
        print("Outlet count and beverages mismatch !")
    # checking quantity type validations
    total_quantity_error = []
    for item, item_val in total_quantity.items():
        if not isinstance(item_val, int):
            total_quantity_error.append(item)
    if total_quantity_error:
        error = True
        print("Invalid datatype (required int) in total quantity for " + ",".join(total_quantity_error))
    total_bev_error = []
    for item in beverages.values():
        for item_name, item_val in item.items():
            if not isinstance(item_val, int):
                total_bev_error.append(item_name)
    if total_bev_error:
        error = True
        print("Invalid datatype (required int) in beverages for " + ",".join(total_bev_error))
    if error:
        print("*** Exiting the application ***")
        return ({}, {})
    return (total_quantity, beverages)


data = requests.get("https://api.npoint.io/77e0bf528e4af43cdc10")  # getting input data
data = data.json()
# if you want to add test case manually uncomment below variable (data) and comment above two (113,114) line
# data = {
#   "machine": {
#     "outlets": {
#       "count_n": 4
#     },
#     "total_items_quantity": {
#       "hot_water": 500,
#       "hot_milk": 500,
#       "ginger_syrup": 100,
#       "sugar_syrup": 100,
#       "tea_leaves_syrup": 100
#     },
#     "beverages": {
#       "hot_tea": {
#         "hot_water": 200,
#         "hot_milk": 100,
#         "ginger_syrup": 10,
#         "sugar_syrup": 10,
#         "tea_leaves_syrup": 30
#       },
#       "hot_coffee": {
#         "hot_water": 100,
#         "ginger_syrup": 30,
#         "hot_milk": 400,
#         "sugar_syrup": 50,
#         "tea_leaves_syrup": 30
#       },
#       "black_tea": {
#         "hot_water": 300,
#         "ginger_syrup": 30,
#         "sugar_syrup": 50,
#         "tea_leaves_syrup": 30
#       },
#       "green_tea": {
#         "hot_water": 100,
#         "ginger_syrup": 30,
#         "sugar_syrup": 50,
#         "green_mixture": 30
#       },
#     }
#   }
# }
total_quantity, beverages = parse_validate_data(data)
cMachine = CoffeMachine(total_quantity, beverages)
for item, val in beverages.items():
    print(cMachine.prepare(item))
