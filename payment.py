import sys
sys.dont_write_bytecode = True

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from user import Admin, Customer
from product import Product
from cart import Cart
from order import Order


class Payment:
    def __init__(self, id, order, method):
        self.id = id
        self.order_id = order.id
        self.method = method
        order.status = "PAID"
        self.status = "SUCCESS"


users = {1: Admin(1, "Admin"), 2: Customer(2, "John")}
products = {1: Product(1, "Laptop", 75000), 2: Product(2, "Phone", 30000)}
cart = Cart()
orders = {}


class Handler(BaseHTTPRequestHandler):
    def route(self):
        n = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(n)) if n else {}
        view = lambda: {"items": [p.name for p in cart.items], "total": cart.total()}

        if self.path == "/products":
            return [vars(p) for p in products.values()]
        if self.path == "/orders":
            return [vars(o) for o in orders.values()]
        if self.path == "/cart":
            return view()
        if self.path == "/cart/add":
            cart.add(products[data["product_id"]])
            return view()
        if self.path == "/checkout":
            oid = len(orders) + 1
            orders[oid] = Order(oid, cart.items, cart.total())
            cart.items = []
            return vars(orders[oid])
        if self.path == "/pay":
            return vars(Payment(1, orders[data["order_id"]], data["method"]))
        return {"error": "not found"}

    def reply(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(self.route()).encode())

    do_GET = do_POST = reply


if __name__ == "__main__":
    print("Running at http://127.0.0.1:5000")
    HTTPServer(("127.0.0.1", 5000), Handler).serve_forever()
