import heapq
import time

class Order:
    def __init__(self, order_id, items, time_received, estimated_prep_time):
        self.order_id = order_id
        self.items = items
        self.time_received = time_received
        self.estimated_prep_time = estimated_prep_time
        self.status = "pending"
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        waiting_time = time.time() - self.time_received
        complexity = len(self.items)
        return waiting_time * complexity

class KitchenOrderQueue:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def complete_order(self):
        if not self.is_empty():
            completed_order = self.orders.pop()
            completed_order.status = "completed"
            return completed_order
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.orders[-1]
        else:
            return None

    def is_empty(self):
        return len(self.orders) == 0


class CustomerOrderQueue:
    def __init__(self):
        self.orders = []
        self.order_counter = 0

    def enqueue(self, order):
        self.order_counter += 1
        heapq.heappush(self.orders, (order.priority, self.order_counter, order))

    def dequeue(self):
        if self.orders:
            _, _, order = heapq.heappop(self.orders)
            return order
        else:
            return None

    def peek(self):
        if self.orders:
            _, _, order = self.orders[0]
            return order
        else:
            return None

    def is_empty(self):
        return len(self.orders) == 0

    def add_order(self, order):
        self.enqueue(order)
        print(f"Order {order.order_id} added to queue.")

    def process_orders(self):
        while not self.is_empty():
            order = self.peek()
            if self._is_order_ready(order):
                completed_order = self.dequeue()
                completed_order.status = "completed"
                self._notify_customer(completed_order)
            else:
                break

    def _is_order_ready(self, order):
        elapsed_time = time.time() - order.time_received
        return elapsed_time >= order.estimated_prep_time

    def _notify_customer(self, order):
        print(f"Order {order.order_id} is ready for pickup/delivery!")

kitchen_queue = KitchenOrderQueue()
customer_queue = CustomerOrderQueue()

orders = [
    Order(1, ["Burger", "Fries"], time.time(), 15),
    Order(2, ["Salad"], time.time(), 5),
    Order(3, ["Pizza", "Wings", "Soda"], time.time(), 20),
    Order(4, ["Steak", "Baked Potato", "Broccoli"], time.time(), 25),
    Order(5, ["Pasta Primavera"], time.time(), 12),
]

for order in orders:
    customer_queue.add_order(order)

while not customer_queue.is_empty() or not kitchen_queue.is_empty():
    while not customer_queue.is_empty() and len(kitchen_queue.orders) < 3:
        kitchen_queue.add_order(customer_queue.dequeue())

    kitchen_queue.complete_order()

    customer_queue.process_orders()

    time.sleep(1)