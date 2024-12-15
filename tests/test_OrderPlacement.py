import unittest
from unittest import mock  # 导入 mock 模块，用于模拟支付失败的情况。

from tests.integration_tests import User


# 购物车商品类
class CartItem:
    """
    表示购物车中的单个商品。

    属性：
        name (str): 商品名称。
        price (float): 商品价格。
        quantity (int): 商品在购物车中的数量。
    """

    def __init__(self, name, price, quantity):
        """
        初始化一个 CartItem 对象，设置名称、价格和数量。

        参数：
            name (str): 商品名称。
            price (float): 商品价格。
            quantity (int): 商品在购物车中的数量。
        """
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, new_quantity):
        """
        更新购物车中商品的数量。

        参数：
            new_quantity (int): 商品的新数量。
        """
        self.quantity = new_quantity

    def get_subtotal(self):
        """
        计算该商品的小计价格，基于其价格和数量。

        返回：
            float: 该商品的小计价格。
        """
        return self.price * self.quantity


# 购物车类
class Cart:
    """
    表示一个可以包含多个 CartItem 对象的购物车。

    属性：
        items (list): 购物车中的商品列表。
    """

    def __init__(self):
        """
        初始化一个空的购物车，没有商品。
        """
        self.items = []

    def add_item(self, name, price, quantity):
        """
        将新商品添加到购物车，或更新现有商品的数量。

        参数：
            name (str): 商品名称。
            price (float): 商品价格。
            quantity (int): 要添加到购物车的数量。

        返回：
            str: 表示商品已添加或更新的消息。
        """
        for item in self.items:
            if item.name == name:
                # 如果商品已在购物车中，更新其数量。
                item.update_quantity(item.quantity + quantity)
                return f"Updated {name} quantity to {item.quantity}"

        # 如果商品不在购物车中，作为新商品添加。
        new_item = CartItem(name, price, quantity)
        self.items.append(new_item)
        return f"Added {name} to cart"

    def remove_item(self, name):
        """
        通过商品名称从购物车中移除商品。

        参数：
            name (str): 要移除的商品名称。

        返回：
            str: 表示商品已移除的消息。
        """
        self.items = [item for item in self.items if item.name!= name]
        return f"Removed {name} from cart"

    def update_item_quantity(self, name, new_quantity):
        """
        通过商品名称更新购物车中商品的数量。

        参数：
            name (str): 商品名称。
            new_quantity (int): 商品的新数量。

        返回：
            str: 表示商品数量已更新或商品未找到的消息。
        """
        for item in self.items:
            if item.name == name:
                item.update_quantity(new_quantity)
                return f"Updated {name} quantity to {new_quantity}"
        return f"{name} not found in cart"

    def calculate_total(self):
        """
        计算购物车中商品的总成本，包括税费和运费。

        返回：
            dict: 包含小计、税费、运费和总成本的字典。
        """
        subtotal = sum(item.get_subtotal() for item in self.items)
        tax = subtotal * 0.10  # 假设 10% 的税率。
        delivery_fee = 5.00  # 固定运费。
        total = subtotal + tax + delivery_fee
        return {"subtotal": subtotal, "tax": tax, "delivery_fee": delivery_fee, "total": total}

    def view_cart(self):
        """
        提供购物车中商品的视图。

        返回：
            list: 包含每个商品名称、数量和小计价格的字典列表。
        """
        return [{"name": item.name, "quantity": item.quantity, "subtotal": item.get_subtotal()} for item in self.items]


# 订单放置类
class OrderPlacement:
    """
    表示放置订单的过程，包括验证、结账和确认。

    属性：
        cart (Cart): 包含订单商品的购物车。
        user_profile (UserProfile): 用户的个人资料，包括配送地址。
        restaurant_menu (RestaurantMenu): 包含可用餐厅商品的菜单。
    """

    def __init__(self, cart, user_profile, restaurant_menu):
        """
        初始化 OrderPlacement 对象，设置购物车、用户资料和餐厅菜单。

        参数：
            cart (Cart): 购物车。
            user_profile (UserProfile): 用户的个人资料对象。
            restaurant_menu (RestaurantMenu): 餐厅菜单。
        """
        self.cart = cart
        self.user_profile = user_profile  # 直接使用 UserProfile 对象
        self.restaurant_menu = restaurant_menu

    def _create_user_profile_from_dict(self, user_dict):
        # 假设用户字典中至少包含 'delivery_address' 键
        delivery_address = user_dict.get('delivery_address', 'No address provided')
        return UserProfile(delivery_address)

    def validate_order(self):
        """
        通过检查购物车是否为空以及所有商品是否在餐厅菜单中可用来验证订单。

        返回：
            dict: 表示订单是否有效以及伴随的消息的字典。
        """
        if not self.cart.items and len(self.user_profile.delivery_address.strip())!=0:
            return {"success": False, "message": "Cart is empty"}
        # 新增：检查用户资料是否完整
        if not self.user_profile.delivery_address or len(self.user_profile.delivery_address.strip())==0:
            return {"success": False, "message": "User profile is incomplete or address is missing"}
        # 验证购物车中每个商品的可用性。
        for item in self.cart.items:
            if not self.restaurant_menu.is_item_available(item.name):
                return {"success": False, "message": f"{item.name} is not available"}
        return {"success": True, "message": "Order is valid"}

    def proceed_to_checkout(self):
        """
        准备结账订单，计算总价并获取配送地址。

        返回：
            dict: 包含购物车商品、总成本详情和配送地址的字典。
        """
        total_info = self.cart.calculate_total()
        return {
            "items": self.cart.view_cart(),
            "total_info": total_info,
            "delivery_address": self.user_profile.delivery_address,
        }

    def confirm_order(self, payment_method):
        """
        通过验证订单并处理支付来确认订单。

        参数：
            payment_method (PaymentMethod): 要使用的支付方式。

        返回：
            dict: 表示订单是否已确认以及成功时的订单 ID 的字典。
        """
        if not self.validate_order()["success"]:
            return {"success": False, "message": "Order validation failed"}

        # 使用给定的支付方式处理支付。
        payment_success = payment_method.process_payment(self.cart.calculate_total()["total"])

        if payment_success:
            # 订单确认成功时添加订单到用户订单列表
            self.user_profile.add_order(
                "ORD123456",  # 模拟订单 ID。
                self.cart.view_cart(),
                self.cart.calculate_total()["total"],
                "Confirmed",
                "2024-12-12"  # 假设当前日期
            )
            return {
                "success": True,
                "message": "Order confirmed",
                "order_id": "ORD123456",  # 模拟订单 ID。
                "estimated_delivery": "45 minutes"
            }
        return {"success": False, "message": "Payment failed"}


# 支付方式类
class PaymentMethod:
    """
    表示订单的支付方式。
    """

    def process_payment(self, amount):
        """
        处理给定金额的支付。

        参数：
            amount (float): 要支付的金额。

        返回：
            bool: 如果支付成功返回 True，否则返回 False。
        """
        if amount > 0:
            return True
        return False


# 用户资料类（模拟用户的详细信息）
class UserProfile:
    def __init__(self, delivery_address):
        self.delivery_address = delivery_address
        self.orders = []

    def add_order(self, order_id, items, total, status, date):
        order = {
            "order_id": order_id,
            "items": items,
            "total": total,
            "status": status,
            "date": date
        }
        self.orders.append(order)

    def view_order_history(self):
        return self.orders

    def filter_order_history(self, status=None, date=None):
        filtered_orders = [o for o in self.orders
                           if (status is None or o['status'] == status) and
                           (date is None or o['date'] == date)]
        return filtered_orders

# 餐厅菜单类（模拟可用的菜单项）
class RestaurantMenu:
    """
    表示餐厅的菜单，包括可用的商品。

    属性：
        available_items (list): 餐厅菜单中可用的商品列表。
    """

    def __init__(self, available_items):
        """
        初始化 RestaurantMenu，设置可用商品列表。

        参数：
            available_items (list): 可用的菜单项列表。
        """
        self.available_items = available_items

    def is_item_available(self, item_name):
        """
        检查特定商品是否在餐厅菜单中可用。

        参数：
            item_name (str): 要检查的商品名称。

        返回：
            bool: 如果商品可用返回 True，否则返回 False。
        """
        return item_name in self.available_items


# OrderPlacement 类的单元测试
class TestOrderPlacement(unittest.TestCase):
    """
    OrderPlacement 类的单元测试，用于验证订单放置逻辑的正确性。
    """
    def setUp(self):
        """
        设置测试环境，创建必要的类的实例。
        - RestaurantMenu: 餐厅菜单实例，包含可用的商品列表。
        - UserProfile: 用户资料实例，包含用户的配送地址。
        - Cart: 购物车实例，用于存放用户选择的商品。
        - OrderPlacement: 订单放置实例，用于处理订单的验证、结账和确认。
        """
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.order = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

    def test_validate_order_empty_cart(self):
        """
        测试用例：验证空购物车的订单。
        - 预期结果：订单验证失败，返回消息“Cart is empty”。
        """
        result = self.order.validate_order()
        self.assertFalse(result["success"])  # 验证订单是否未成功
        self.assertEqual(result["message"], "Cart is empty")  # 验证返回消息是否正确

    def test_validate_order_item_not_available(self):
        """
        测试用例：验证包含不可用商品的订单。
        - 向购物车添加一个不在菜单中的商品“Pasta”。
        - 预期结果：订单验证失败，返回消息“Pasta is not available”。
        """
        self.cart.add_item("Pasta", 15.99, 1)
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Pasta is not available")

    def test_validate_order_success(self):
        """
        测试用例：成功验证订单。
        - 向购物车添加一个可用商品“Burger”。
        - 预期结果：订单验证成功，返回消息“Order is valid”。
        """
        self.cart.add_item("Burger", 8.99, 2)
        result = self.order.validate_order()
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order is valid")

    def test_confirm_order_success(self):
        """
        测试用例：成功确认订单。
        - 向购物车添加一个可用商品“Pizza”。
        - 使用 PaymentMethod 模拟支付过程。
        - 预期结果：订单确认成功，返回订单 ID“ORD123456”。
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()
        result = self.order.confirm_order(payment_method)
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")
        self.assertEqual(result["order_id"], "ORD123456")

    def test_confirm_order_failed_payment(self):
        """
        测试用例：支付失败时确认订单。
        - 向购物车添加一个可用商品“Pizza”。
        - 使用 unittest.mock.patch 模拟支付失败的情况。
        - 预期结果：订单确认失败，返回消息“Payment failed”。
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()

        # 使用 unittest.mock.patch 模拟支付失败
        with mock.patch.object(payment_method, 'process_payment', return_value=False):
            result = self.order.confirm_order(payment_method)
            self.assertFalse(result["success"])
            self.assertEqual(result["message"], "Payment failed")

    def test_calculate_total_multiple_items(self):
        """
        测试：购物车中有多个商品时，总价计算是否正确。
        """
        self.cart.add_item("Burger", 8.99, 2)  # 小计：8.99 * 2 = 17.98
        self.cart.add_item("Pizza", 12.99, 1)  # 小计：12.99 * 1 = 12.99
        self.cart.add_item("Salad", 5.99, 3)  # 小计：5.99 * 3 = 17.97

        total_info = self.cart.calculate_total()

        expected_subtotal = 17.98 + 12.99 + 17.97  # 48.94
        expected_tax = expected_subtotal * 0.10  # 4.894
        expected_delivery_fee = 5.00  # 固定配送费
        expected_total = expected_subtotal + expected_tax + expected_delivery_fee  # 58.834

        self.assertEqual(total_info["subtotal"], expected_subtotal)
        self.assertEqual(total_info["tax"], expected_tax)
        self.assertEqual(total_info["delivery_fee"], expected_delivery_fee)
        self.assertEqual(total_info["total"], expected_total)

    def test_remove_item(self):
        """
        测试：从购物车中移除商品。
        """
        self.cart.add_item("Burger", 8.99, 2)
        self.cart.add_item("Pizza", 12.99, 1)

        # 确认购物车有两个商品
        self.assertEqual(len(self.cart.items), 2)

        # 移除 Burger
        result = self.cart.remove_item("Burger")
        self.assertEqual(result, "Removed Burger from cart")

        # 确认购物车只剩下一个商品
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].name, "Pizza")

    def test_update_item_quantity(self):
        """
        测试：更新购物车中商品的数量。
        """
        self.cart.add_item("Burger", 8.99, 2)  # 初始数量为 2
        self.cart.add_item("Pizza", 12.99, 1)  # 初始数量为 1

        # 更新 Burger 的数量为 3
        result = self.cart.update_item_quantity("Burger", 3)
        self.assertEqual(result, "Updated Burger quantity to 3")

        # 确认 Burger 的数量已更新为 3
        self.assertEqual(self.cart.items[0].quantity, 3)

        # 确认更新后的小计正确
        expected_subtotal_burger = 8.99 * 3  # 8.99 * 3 = 26.97
        self.assertEqual(self.cart.items[0].get_subtotal(), expected_subtotal_burger)

        # 更新 Pizza 的数量为 2
        result = self.cart.update_item_quantity("Pizza", 2)
        self.assertEqual(result, "Updated Pizza quantity to 2")

        # 确认 Pizza 的数量已更新为 2
        self.assertEqual(self.cart.items[1].quantity, 2)

        # 确认更新后的小计正确
        expected_subtotal_pizza = 12.99 * 2  # 12.99 * 2 = 25.98
        self.assertEqual(self.cart.items[1].get_subtotal(), expected_subtotal_pizza)

    def test_calculate_total_empty_cart(self):
        """
        测试：购物车为空时，总价是否正确返回 0。
        """
        total_info = self.cart.calculate_total()

        self.assertEqual(total_info["subtotal"], 0.00)
        self.assertEqual(total_info["tax"], 0.00)
        self.assertEqual(total_info["delivery_fee"], 5.00)  # 固定配送费
        self.assertEqual(total_info["total"], 5.00)  # 只有配送费

    def test_validate_order_incomplete_user_info(self):
        """
        测试：如果用户的配送信息不完整，订单验证失败。
        """
        # 创建一个没有完整配送地址的用户
        incomplete_user_profile = UserProfile(delivery_address="")  # 空地址

        # 创建订单对象
        order_with_incomplete_info = OrderPlacement(self.cart, incomplete_user_profile, self.restaurant_menu)

        # 尝试进行订单验证
        result = order_with_incomplete_info.validate_order()

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "User profile is incomplete or address is missing")

    def test_validate_order_item_not_in_menu(self):
        """
        测试：添加一个不在餐厅菜单中的商品，订单验证失败。
        """
        # 添加一个不在菜单中的商品
        self.cart.add_item("Sushi", 20.99, 1)  # Sushi 不在菜单中

        result = self.order.validate_order()

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Sushi is not available")

    def test_update_item_price(self):
        """
        测试：更新购物车中商品的价格，验证小计和总价是否更新。
        """
        self.cart.add_item("Burger", 8.99, 2)
        self.cart.add_item("Pizza", 12.99, 1)

        # 更新 Burger 的价格
        self.cart.items[0].price = 10.99  # 更新价格为 10.99

        # 验证 Burger 的小计是否更新
        expected_subtotal_burger = 10.99 * 2  # 10.99 * 2 = 21.98
        self.assertEqual(self.cart.items[0].get_subtotal(), expected_subtotal_burger)

        # 重新计算总价
        total_info = self.cart.calculate_total()

        expected_subtotal = 21.98 + 12.99  # 21.98 + 12.99 = 34.97
        expected_tax = expected_subtotal * 0.10  # 10% 税费
        expected_total = expected_subtotal + expected_tax + 5.00  # 小计 + 税费 + 配送费

        self.assertEqual(total_info["subtotal"], expected_subtotal)
        self.assertEqual(total_info["tax"], expected_tax)
        self.assertEqual(total_info["total"], expected_total)

    def test_confirm_order_payment_failed_due_to_insufficient_balance(self):
        """
        测试：模拟余额不足导致支付失败的情况。
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()

        # 模拟余额不足的支付失败
        with mock.patch.object(payment_method, 'process_payment', return_value=False):
            result = self.order.confirm_order(payment_method)

            self.assertFalse(result["success"])
            self.assertEqual(result["message"], "Payment failed")

# 作为用户查找先前的订单
    def test_view_order_history_with_orders(self):
        user = UserProfile(delivery_address="123 Main St")
        user.add_order("Order001", "Pizza", 25.00, "Delivered", "2023-09-15")
        order_history = user.view_order_history()
        self.assertEqual(len(order_history), 1)
        self.assertEqual(order_history[0]['order_id'], 'Order001')
    def test_view_order_history_empty(self):
        user = UserProfile(delivery_address="123 Main St")
        order_history = user.view_order_history()
        self.assertEqual(len(order_history), 0)  # 假设初始时用户没有订单历史
    def test_view_order_history_with_multiple_orders(self):
        user = UserProfile(delivery_address="123 Main St")
        user.add_order("Order001", "Pizza", 25.00, "Delivered", "2023-09-15")
        user.add_order("Order002", "Burger", 15.00, "Delivered", "2023-09-16")
        order_history = user.view_order_history()
        self.assertEqual(len(order_history), 2)
        self.assertEqual(order_history[0]['order_id'], 'Order001')
        self.assertEqual(order_history[1]['order_id'], 'Order002')
    def test_filter_order_history_by_date(self):
        user = UserProfile(delivery_address="123 Main St")
        user.add_order("Order001", "Pizza", 25.00, "Delivered", "2023-09-15")
        user.add_order("Order002", "Burger", 15.00, "Delivered", "2023-09-16")
        filtered_history = user.filter_order_history(date="2023-09-15")  # 假设添加了按日期筛选的方法
        self.assertEqual(len(filtered_history), 1)
        self.assertEqual(filtered_history[0]['order_id'], 'Order001')
    def test_filter_order_history_by_status(self):
        user = UserProfile(delivery_address="123 Main St")
        user.add_order("Order001", "Pizza", 25.00, "Delivered", "2023-09-15")
        user.add_order("Order002", "Burger", 15.00, "Pending", "2023-09-16")
        filtered_history = user.filter_order_history(status="Delivered")  # 假设添加了按状态筛选的方法
        self.assertEqual(len(filtered_history), 1)
        self.assertEqual(filtered_history[0]['order_id'], 'Order001')
    def test_order_confirmation_updates_order_history(self):
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()
        result = self.order.confirm_order(payment_method)
        self.assertTrue(result["success"])
        order_history = self.user_profile.view_order_history()
        self.assertEqual(len(order_history), 1)
        self.assertEqual(order_history[0]['order_id'], 'ORD123456')
#红绿测试
class TestUserOrderHistory(unittest.TestCase):
    def setUp(self):
        # 每个测试用例前都初始化一个 User 实例
        self.user = User()
    def test_view_order_history_with_discounted_orders(self):
        self.user.add_order("Order003", "Salad", 10.00, "Delivered", "2023-09-17")
        self.user.add_order("Order004", "Soda", 2.00, "Delivered", "2023-09-18")
        # 假设对订单进行折扣操作
        self.user.orders[0]["price"] = 8.00
        order_history = self.user.view_order_history()
        self.assertEqual(len(order_history), 2)
        self.assertEqual(order_history[0]["price"], 8.00)
        self.assertEqual(order_history[1]["price"], 2.00)
    def test_view_order_history_with_different_addresses(self):
        self.user.add_order("Order008", "Cake", 20.00, "Delivered", "2023-09-22")
        # 假设更新用户地址
        self.user.delivery_address = "789 Oak St"
        self.user.add_order("Order009", "Chocolate", 18.00, "Delivered", "2023-09-23")
        order_history = self.user.view_order_history()
        self.assertEqual(len(order_history), 2)
        self.assertEqual(self.user.delivery_address, "789 Oak St")
    def test_view_order_history_with_address_change_midway(self):
        self.user.add_order("Order101", "Steak", 30.00, "Delivered", "2023-10-01")
        # 假设更新用户地址
        self.user.delivery_address = "456 Elm St"
        self.user.add_order("Order102", "Sushi", 25.00, "Delivered", "2023-10-02")
        order_history = self.user.view_order_history()
        self.assertEqual(len(order_history), 2)
        self.assertEqual(order_history[0]['delivery_address'], "123 Main St")
        self.assertEqual(order_history[1]['delivery_address'], "456 Elm St")
    def test_view_order_history_with_null_address(self):
        self.user.add_order("Order106", "Bread", 5.00, "Delivered", "2023-10-06")
        # 假设更新用户地址为 None
        self.user.delivery_address = None
        self.user.add_order("Order107", "Butter", 3.00, "Delivered", "2023-10-07")
        order_history = self.user.view_order_history()
        self.assertEqual(len(order_history), 2)
        self.assertIsNone(order_history[1]['delivery_address'])
    def test_clear_order_history(self):
        self.user.add_order("Order005", "Ice Cream", 5.00, "Pending", "2023-09-19")
        self.user.clear_order_history()  # 假设添加了清空订单历史的方法
        order_history = self.user.view_order_history()
        self.assertEqual(len(order_history), 0)

# 如果直接运行脚本，可以执行测试
if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()