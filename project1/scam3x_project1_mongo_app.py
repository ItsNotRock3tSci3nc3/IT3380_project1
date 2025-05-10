from pymongo import MongoClient

def connect_to_mongo():
    try:
        mongo_client = MongoClient(
            host="localhost:17027",
            username = "",
            password = "",
            socketTimeoutMS=3000
        )
        db = mongo_client["classicmodels"]
        return db
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return None

def view_orders_by_customer(db):
    customer_name = input("Enter customer name: ")
    pipeline = [
        {"$match": {"customerName": customer_name}},
        {"$group": {"_id": "$customerName", "Orders Placed": {"$sum": 1}}}
    ]
    result = list(db.orders.aggregate(pipeline))
    return result

def view_customers_by_state(db):
    state = input("Enter state: ")
    pipeline = [
        {"$match": {"state": state}},
        {"$group": {"_id": "$state", "Number of Customers in State": {"$sum": 1}}}
    ]
    result = list(db.customers.aggregate(pipeline))
    return result


def view_employees_by_manager(db):
    manager_name = input("Enter manager name: ")
    pipeline = [
        {"$match": {"managerName": manager_name}},
        {"$group": {"_id": "$managerName", "Number of Reports": {"$sum": 1}}}
    ]
    result = list(db.employees.aggregate(pipeline))
    return result


def view_dollar_value_of_product(db):
    product_name = input("Enter product name: ")
    pipeline = [
        {"$match": {"productName": product_name}},
        {"$project": {
            "productName": 1,
            "quantityInStock": 1,
            "buyPrice": 1,
            "Dollar Value": {"$multiply": ["$quantityInStock", "$buyPrice"]}
        }}
    ]
    result = list(db.products.aggregate(pipeline))
    return result


def main():
    db = connect_to_mongo()
    if db is None:
        return

    while True:
        print("\nMenu:")
        print("1. View the number of orders placed by a customer")
        print("2. View the number of customers in a state")
        print("3. View the number of employees a manager manages")
        print("4. View the dollar value of a product in stock")
        print("5. Exit application")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_orders_by_customer(db)
        elif choice == "2":
            view_customers_by_state(db)
        elif choice == "3":
            view_employees_by_manager(db)
        elif choice == "4":
            view_dollar_value_of_product(db)
        elif choice == "5":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
