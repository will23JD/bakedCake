import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Bakedcake')


print(SHEET.sheet1.acell('B2'))


def start():
    """
    Gets a user ID to grant access to the program
    repeats code unit a vadil ID is given.
    """
    while True:
        login = input("Please enter your Login ID: ")
        print("-" * 30)

        if validate_id(login):
            print("valid ID, welcome")
            print("-" * 30)
            break


def validate_id(data):
    """
    Checkes to see if the given id is correct.
    Checkes to see if all values are integers
    and that they are the correct ones if not
    raises a ValueError.
    """
    code = "1"

    try:
        if code != data:
            raise ValueError()
    except ValueError:
        print(f"Incorrect ID: {data}, Please try again.")
        print("x" * 30)
        return False

    return True


def update_check():
    """
    Asks the user if they want to check on stock levels
    or update them.
    """
    while True:
        print("To check all stock levels enter: 1")
        print("To update all stock levels enter: 2")
        print("To update individual stock levels enter: 3")
        print("To add a new item enter: 4")
        print("To delete a item enter: 5")
        user_choice = input("Enter: ")
        print("-" * 30)

        if validate_c(user_choice):
            break


def validate_c(data):
    """
    checks whether the user wants to update stock levels
    or check them.
    """

    try:
        if data == "1":
            get_stock_values()
        elif data == "2":
            update_all()
        elif data == "3":
            update_ind()
        elif data == "4":
            add_items()
        elif data == "5":
            get_del_item()
        else:
            raise ValueError()
    except ValueError:
        print(f"Invalid choice: {data}")
        print("Please enter 1, 2, 3, 4 or 5.\n")
        return False

    return True


def get_stock_values():
    """
    get stock values and headings to create a dictionary
    """
    headings = SHEET.worksheet("stock").col_values(1)
    stock = SHEET.worksheet("stock").col_values(2)
    stock_table = {headings[i]: stock[i] for i in range(len(headings))}

    print("All units are in grams.\n")
    for key, value in stock_table.items():
        print(f"{key} : {value}")

    option = input("Would you like to update stocks y/n: ")
    continue_program(option)


def update_all():
    """
    Get new data for all stock levels
    """
    headings = SHEET.worksheet("stock").col_values(1)
    while True:
        print("Remeber units are in gram's apart from eggs")
        print("And should be separated by commas(1000,200, ...)")
        print(f"Enter new stock blow in the order {headings}\n")
        all_stock = input("New stock: ")

        new_stock = all_stock.split(",")

        if validate_stock(new_stock):
            print("Correct input")
            break

    add_new_stock(new_stock)


def validate_stock(data):
    """
    The try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't 7 values.
    """
    headings = SHEET.worksheet("stock").col_values(1)
    index = []
    for i in range(len(headings)):
        index.append(i)
    try:
        [int(num) for num in data]
        if len(data) != len(index):
            raise ValueError(
                f"{len(index)} values required, you provided {len(data)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_ind():
    """
    function to change individual stock levels.
    """
    while True:
        headings = SHEET.worksheet("stock").col_values(1)
        names = {headings[i]: i + 1 for i in range(len(headings))}
        for key, value in names.items():
            print(f"{key} : {value}")
        ind_c = input("\nPlease enter the number of the stock to change: ")
        ind_stock = input("And the new stock level: ")

        if val_ind_name(ind_c) and val_ind_stock(ind_stock):
            break
    print("\nAdding new stock...")
    update_stock(ind_c, ind_stock)
    print("New stock added.")


def val_ind_name(name):
    """
    Function to check is input stock is on the worksheet.
    If not returns false causing the while loop to continue.
    """
    headings = SHEET.worksheet("stock").col_values(1)
    index = []
    for i in range(len(headings)):
        index.append(i + 1)
    try:
        if int(name) not in index:
            raise ValueError()
    except ValueError as e:
        print(f"{e}{name} is not in stock worksheet please try again.")
        return False

    return True


def val_ind_stock(data):
    """
    Validate if stock is a int.
    If not returns false causing the while loop to continue.
    """
    try:
        [int(num) for num in data]
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def add_new_stock(data):
    """
    Add's new stock data to the worksheet.
    """
    print(f"Adding stock new {data}...")
    all_stock = {data[i]: i + 1 for i in range(len(data))}

    for stock, name in all_stock.items():
        update_stock(name, stock)
    print("New stock added.")


def update_stock(name, data):
    """
    Add new stock name and stock level to google sheet.
    """
    SHEET.sheet1.update_cell(name, 2, data)


def add_items():
    """
    Get new stock new and stock level.
    pass them to validation function.
    """
    while True:
        print("Please enter the name of the item you wish to add:")
        name = input("Enter: ")
        print("\nPlease enter the quantity of the item(in grams)")
        stock = input("Enter: ")

        if val_ind_stock(stock):
            break
    print(f"\nAdding new item: {name} and value: {stock}...")
    append_n_stock(name, stock)
    print(f"New item: {name} and value: {stock} Added.")


def append_n_stock(name, data):
    """
    Append new stock new and data.
    """
    headings = SHEET.worksheet("stock").col_values(1)
    for i in range(len(headings)):
        new = i + 2
    SHEET.sheet1.update_cell(new, 1, name)
    SHEET.sheet1.update_cell(new, 2, data)


def get_del_item():
    """
    Get user choice for item to delete from google sheets.
    Pass choice to validation to check its an int.
    """
    while True:
        print("Please enter the number of the item you would like to delete.")
        headings = SHEET.worksheet("stock").col_values(1)
        names = {headings[i]: i + 1 for i in range(len(headings))}
        for key, value in names.items():
            print(key, ':', value)
        remove = input("\nEnter: ")

        if val_ind_name(remove):
            break
    print("\nRemoving item....")
    delete_item(remove)
    print("Item deleted.")


def delete_item(row):
    """
    get row from user input and delete from google sheet.
    """
    SHEET.sheet1.delete_rows(int(row))


def continue_program(data):
    """
    checkes input is the right value.
    if not raise ValueError
    if input is correct opens the asked for function.
    """
    try:
        if data == "y":
            update_all()
        elif data == "n":
            exit()
        else:
            raise ValueError()
    except ValueError:
        print(f"Invalid choice: {data}")
        print("Please enter y or n(selection is case sensitive).\n")


def control():
    """
    Main function which starts and controls the program
    """
    print("Welcome to Bakecake stock control terminal")
    print("-" * 30)
    start()
    update_check()


control()
