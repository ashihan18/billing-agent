import re

class BillBotCore:
    def __init__(self):
        self.cart = []
        self.inventory = {
            "parle g": {"price": 10, "stock": 100},
            "surf excel": {"price": 50, "stock": 50},
            "coca cola": {"price": 40, "stock": 80},
            "maggi": {"price": 15, "stock": 60},
            "rice": {"price": 60, "stock": 30},
            "dal": {"price": 80, "stock": 40},
        }

    def fuzzy_match(self, item_name):
        item_name = item_name.lower().strip()
        for key in self.inventory.keys():
            if item_name in key or key in item_name:
                return key
        return None

    def add_item(self, text):
        match = re.search(r'(\d+)?\s*(.+)', text.lower())
        qty = int(match.group(1)) if match and match.group(1) else 1
        item_name = match.group(2).strip() if match else text.lower()

        product = self.fuzzy_match(item_name)
        if not product:
            return f"❌ Product '{item_name}' not found in inventory."

        if self.inventory[product]["stock"] < qty:
            return f"❌ Only {self.inventory[product]['stock']} left in stock!"

        self.inventory[product]["stock"] -= qty
        self.cart.append({"name": product, "qty": qty, "price": self.inventory[product]["price"]})
        total = sum(i["qty"]*i["price"] for i in self.cart)
        return f"✅ Added {qty}× {product.title()}. Running Total: ₹{total}"

    def get_cart(self):
        if not self.cart:
            return "🛒 Cart is empty"
        total = sum(i["qty"]*i["price"] for i in self.cart)
        gst = total * 0.18
        items = "\n".join([f"• {i['qty']}× {i['name'].title()} = ₹{i['qty']*i['price']}" for i in self.cart])
        return f"**Current Cart**\n{items}\n\nSubtotal: ₹{total}\nGST (18%): ₹{gst:.2f}\n**Grand Total: ₹{total + gst:.2f}**"

    def generate_receipt(self):
        if not self.cart:
            return "Cart is empty!"
        receipt = self.get_cart()
        self.cart = []
        return f"🧾 OFFICIAL RECEIPT\n\n{receipt}\n\nThank you for shopping! ❤️"

    def get_inventory(self):
        return "\n".join([f"📦 {k.title()}: ₹{v['price']} | Stock: {v['stock']}" for k, v in self.inventory.items()])
