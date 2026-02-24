class Drink:
    def __init__(s, name, price, stock):
        # Initialize drink details
        # s.name = name
        # s.price = price
        # s.stock = stock

        s.name, s.price, s.stock = name, price, stock

class DrinkApp:
    def __init__(s):
        # Initialize drinks list and cart
        s.drinks, s.cart = [], []

    # Adding method -> Add new drink to the menu
    def add_drink(s, name, price, stock):
        s.drinks.append(Drink(name, price, stock))

    # Viewing method -> Display available drinks
    def view_drinks(s):
        if not s.drinks:
            print("No drinks available yet.")
            return
        
        for d in s.drinks:
            print(f"{d.name} - ${d.price} - Stock: {d.stock}") 

    # Purchasing method -> Buy a drink
    def order_drink(s, name, qty):
        for d in s.drinks:
            if d.name == name:
                if d.stock >= qty:
                    d.stock -= qty
                    s.cart.append((d.name, d.price, qty))
                    print(f"Added {qty} x {d.name} to cart.")
                else:
                    print(f"Sorry, only {d.stock} left in stock.")
                return
        print("Drink not found.")

    # Updating method -> Update drink stock
    def update_drink(s, name, price=None, stock=None):
        for d in s.drinks:
            if d.name == name:
                if price: d.price = price
                if stock is not None: d.stock = stock

                print(f"Updated {d.name}.")
                return
        print("Drink not found.")

    # Billing method -> View cart and total
    def bill(s):
        total = sum(p * q for _, p, q in s.cart)

        if not s.cart:
            print("Your cart is empty.")
            return
        
        print("\n--- Your Cart / Bill ---")
        for n, p, q in s.cart:
            print(f"{q} x {n} = ${p * q}")
        print(f"Total: ${total}") 

        s.cart.clear()  # Clear cart after billing

# Manin application loop
app = DrinkApp()

while True:
    print("\n1. Add Drink\n2. View Drinks\n3. Order Drink\n4. Update Drink\n5. View Bill\n6. Exit")

    ch = input("Choose an option: ")

    if ch == '1':
        n = input("Drink Name: "); 
        p = float(input("Price: ")); 
        s = int(input("Stock: "))

        app.add_drink(n, p, s)

    elif ch == '2':
        app.view_drinks()
    elif ch == '3':
        n = input("Drink Name: "); 
        q = int(input("Quantity: "))

        app.order_drink(n, q)
    elif ch == '4':
        n = input("Drink Name: "); 
        p = input("New Price (leave blank to skip): "); 
        s = input("New Stock (leave blank to skip): ")

        p = float(p) if p else None
        s = int(s) if s else None

        app.update_drink(n, p, s) 
    elif ch == '5':
        app.bill()
    elif ch == '6':
        print("Exiting...")
        break
 


 # Run the app using: python main.py
 