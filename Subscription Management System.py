import json
from datetime import datetime, timedelta
import re  


DATA_FILE = "customers.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data(customers):
    with open(DATA_FILE, "w") as file:
        json.dump(customers, file, indent=4)


def add_customer(customers):
    print("\n-- Add New Customer --")
    name = input("Enter customer name (or type 'back' to return): ").strip().lower()
    if name == "back":
        return
    
    if name in customers:
        print(f"Customer '{name}' already exists.")
        return
    
    while True:
        price_input = input("Enter subscription price (or type 'back' to return): ").strip()
        if price_input.lower() == "back":
            return

        
        price_cleaned = re.sub(r"[^\d.]", "", price_input)

        try:
            price = float(price_cleaned)
            if price <= 0:
                raise ValueError
            break 
        except ValueError:
            print("Invalid price entered. Please enter a positive number.")

    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)  
    
    customers[name] = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "price": price
    }
    save_data(customers)
    print(f"Customer '{name}' added with subscription ending on {end_date.strftime('%Y-%m-%d')}.")


def check_subscription(customers):
    print("\n-- Check Customer Subscription --")
    name = input("Enter customer name to check (or type 'back' to return): ").strip().lower()
    if name == "back":
        return
    
    customer = customers.get(name)
    if customer:
        start_date = datetime.strptime(customer["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(customer["end_date"], "%Y-%m-%d")
        current_date = datetime.now()
        
       
        if current_date <= end_date:
            days_left = (end_date - current_date).days
            status = "active"
            print(f"\nCustomer Name: {name.capitalize()}")
            print(f"Subscription Status: {status} ({days_left} days remaining)")
        else:
            days_expired = (current_date - end_date).days
            status = "expired"
            print(f"\nCustomer Name: {name.capitalize()}")
            print(f"Subscription Status: {status} ({days_expired} days since expiration)")
        
        
        print(f"Subscription Price: {customer['price']}")
        print(f"Subscription Start Date: {start_date.strftime('%Y-%m-%d')}")
        print(f"Subscription End Date: {end_date.strftime('%Y-%m-%d')}\n")
    else:
        print("Customer not found.")


def cancel_subscription(customers):
    print("\n-- Cancel Customer Subscription --")
    name = input("Enter customer name to cancel (or type 'back' to return): ").strip().lower()
    if name == "back":
        return
    
    if name in customers:
        confirmation = input(f"Are you sure you want to cancel '{name}' subscription? (yes/no): ").strip().lower()
        if confirmation == "yes":
            del customers[name]
            save_data(customers)
            print(f"Customer '{name}' subscription canceled.")
        else:
            print("Cancellation aborted.")
    else:
        print("Customer not found.")


def edit_subscription(customers):
    print("\n-- Edit Customer Subscription --")
    name = input("Enter customer name to edit (or type 'back' to return): ").strip().lower()
    if name == "back":
        return
    
    customer = customers.get(name)
    if customer:
        while True:
            price_input = input("Enter new subscription price (or type 'back' to return): ").strip()
            if price_input.lower() == "back":
                return

           
            price_cleaned = re.sub(r"[^\d.]", "", price_input)

            try:
                new_price = float(price_cleaned)
                if new_price <= 0:
                    raise ValueError
                break  
            except ValueError:
                print("Invalid price entered. Please enter a positive number.")

        customer["price"] = new_price
        save_data(customers)
        print(f"Customer '{name}' subscription price updated to {new_price}.")
    else:
        print("Customer not found.")


def main():
    customers = load_data()
    while True:
        print("\nSubscription Management System")
        print("1. Add New Customer")
        print("2. Check Customer Subscription")
        print("3. Cancel Customer Subscription")
        print("4. Edit Customer Subscription")
        print("5. Exit")
        choice = input("Select an option: ")
        
        if choice == "1":
            add_customer(customers)
        elif choice == "2":
            check_subscription(customers)
        elif choice == "3":
            cancel_subscription(customers)
        elif choice == "4":
            edit_subscription(customers)
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
