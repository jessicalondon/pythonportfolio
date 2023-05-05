# Create Shoes class

class Shoes:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return int(self.cost)

    def get_quanty(self):
        return int(self.quantity)

    def __str__(self):
        return f"The {self.product} ({self.code}) in {self.country} cost {self.cost} per unit, and there are {self.quantity} in stock. "

shoes_list = []
shoes_quantity = []   # list object is created at the beginning, and populated once the restock() function is called 
#### check if quantity is empty or not. 

# Open & read data to append into a list of Shoes objects, 
# with using try-except for error handling 
def read_shoes_data(): 
    shoes_list.clear() # start with fresh data
    with open('inventory.txt', 'r') as file: 
        for line in file: # Inputting each line as 1 string, so need to convert into 4 arguments
            # Split each line into a list of 4 items
            line = line.replace("\n", "").split(',')
            try:
                # This will skip the first line in the file (of labels), and any 
                # lines with non-integer / invalid values for cost and quantity
                int(line[3])
                int(line[4])
                shoes_list.append(Shoes(line[0],line[1],line[2], line[3], line[4]))
            except ValueError:

                continue
    file.close()


# Allow user to create and append a new shoe object
def capture_shoes():
    product = input("Please enter the shoe's product name: ")
    code = input("Please enter the shoe's product code: ")
    country = input("Please enter the shoe's country: ")

    while True:
        try:
            cost = input("Please enter the shoe's cost per pair (integer input only): ")
            int(cost)
            break
        except ValueError:
            print("Please enter a valid integer")

    while True:
        try:
            quantity = input("Please enter the quantity of stock for the shoes (integer input only): ")
            int(quantity)
            break
        except ValueError:
            print("Please enter a valid integer")

    shoes_list.append(Shoes(country, code, product, cost, quantity))
    with open("inventory.txt", "a") as file:
        file.write(f"{country},{code},{product},{cost},{quantity}")

# print all shoes and details
def view_all():
    for shoe in shoes_list:
        print(shoe)

# Find shoe object with lowest quantity
def re_stock():
    global shoes_quantity  # Reference the global shoes_quantity list
    shoes_quantity.clear()  # Clear the shoes_quantity list
    for shoe in shoes_list:
        shoes_quantity.append(shoe.get_quanty()) # make list of shoe quantities
    min_qty = min(shoes_quantity)
    min_index = shoes_quantity.index(min(shoes_quantity)) # get index of minimum 

    while True:
        restock = input(f"The {shoes_list[min_index].product} shoes have the lowest stock, with a current quantity of {min(shoes_quantity)} pairs. Do you want to add more? (y/n)").lower()
        # Update quantity levels
        if restock == "y":
            while True:
                try:
                    restock_qty = int(input("How many pairs do you want to add?"))
                    break
                except ValueError:
                    print("Please enter a valid integer")
            shoes_list[min_index].quantity = min(shoes_quantity) + restock_qty 
            print(f"There are now {shoes_list[min_index].quantity} pairs.")
            shoes_quantity[min_index] = shoes_list[min_index].quantity  # Update the global shoes_quantity list
            break
        elif restock == "n":
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

    # Update our source file
    new_lines = ['Country,Code,Product,Cost,Quantity\n']
    for shoe in shoes_list:
        shoe_str = f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n"
        new_lines.append(shoe_str)
    new_lines_string = "".join(new_lines) 
    # print(new_lines_string)
    with open('inventory.txt', 'w') as f:
        f.truncate(0)
        # Get the previous contents
        f.write(new_lines_string)
    new_lines_string = ""

# Search for shoe from list using shoe code, returning entire object
def search_shoe(search_code): 
    try: 
        shoes_codes = []
        for shoe in shoes_list:
            shoes_codes.append(shoe.code)
        search_index = shoes_codes.index(search_code)
        print(shoes_list[search_index])
    except ValueError:
        print("**** The product code you entered does not exist in the inventory. You will be taken back to the main menu. ****")

# Calculate total value per product, need to be printed per product
def value_per_item():
    for shoe in shoes_list:
        print(f"The {shoe.product} has a value of {shoe.get_cost() * shoe.get_quanty()}.")

# Find shoe with highest quantity (similar to re_stock()), print as sale
def highest_qty():
    read_shoes_data()
    for shoe in shoes_list:
        shoes_quantity.append(shoe.get_quanty()) # make list of shoe quantities
    max(shoes_quantity) 
    max_index = shoes_quantity.index(max(shoes_quantity)) # get index of minimum 
    print(f"The {shoes_list[max_index].product} shoes are now ON SALE as they have the highest stock, with a current quantity of {max(shoes_quantity)} pairs.")

# Menu executing each function above
# Task specificiations: Allow other store managers to use this program for the following:
#   > Search products by product code
#   > Determine product with lowest quantity and restock
#   > Determine product with highest quantity
#   > Calculate value of each item entry (cost x quantity)

user_choice = ""

while user_choice != "e":
    user_choice = input("""Main Menu - please select enter a letter corresponding to one of the following:
    s - search products by product code
    r - restock lowest quantity product
    h - find product with highest quantity and put on sale
    v - determine value of each product
    c - add new shoe product
    a - view all shoe products
    e - exit
    """).lower()
    read_shoes_data() # shoe_qantity is empty, and only loaded once re_stock() and highest_qty() are called. shoe quantity is not needed for the other functions 
    if user_choice == "s":
        search_code = input("Please enter in the product code: ").strip().upper() # Remove any spaces the user may input. e..g 'sku 90000'
        search_shoe(search_code)
    elif user_choice == "r":
        re_stock()
    elif user_choice == "h":
        highest_qty()
    elif user_choice == "v":
        value_per_item()
    elif user_choice == "c":
        capture_shoes()
    elif user_choice == "a":
        view_all()
    elif user_choice == "e":
        print("Goodbye")
    else:
        print("Oops - incorrect input")