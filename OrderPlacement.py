import unittest
from unittest import mock  # Import the mock module for simulating payment failures in tests.

# CartItem Class
class CartItem:
    """
    Represents an individual item in the shopping cart.
    
    Attributes:
        name (str): The name of the item.
        price (float): The price of the item.
        quantity (int): The quantity of the item in the cart.
    """
    def __init__(self, name, price, quantity):
        """
        Initializes a CartItem object with the given name, price, and quantity.
        
        Args:
            name (str): Name of the item.
            price (float): Price of the item.
            quantity (int): Quantity of the item in the cart.
        """
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, new_quantity):
        """
        Updates the quantity of the item in the cart.
        
        Args:
            new_quantity (int): The new quantity of the item.
        """
        self.quantity = new_quantity

    def get_subtotal(self):
        """
        Calculates the subtotal price for this item based on its price and quantity.
        
        Returns:
            float: The subtotal price for this item.
        """
        return self.price * self.quantity


# Cart Class
class Cart:
    """
    Represents a shopping cart that can contain multiple CartItem objects.
    
    Attributes:
        items (list): A list of CartItem objects in the cart.
    """
    def __init__(self):
        """
        Initializes an empty Cart with no items.
        """
        self.items = []

    def add_item(self, name, price, quantity):
        """
        Adds a new item to the cart or updates the quantity of an existing item.
        
        Args:
            name (str): Name of the item.
            price (float): Price of the item.
            quantity (int): Quantity to be added to the cart.
        
        Returns:
            str: A message indicating whether the item was added or updated.
        """
        for item in self.items:
            if item.name == name:
                # If the item is already in the cart, update its quantity.
                item.update_quantity(item.quantity + quantity)
                return f"Updated {name} quantity to {item.quantity}"
        
        # If the item is not in the cart, add it as a new item.
        new_item = CartItem(name, price, quantity)
        self.items.append(new_item)
        return f"Added {name} to cart"

    def remove_item(self, name):
        """
        Removes an item from the cart by its name.
        
        Args:
            name (str): Name of the item to be removed.
        
        Returns:
            str: A message indicating the item was removed.
        """
        self.items = [item for item in self.items if item.name != name]
        return f"Removed {name} from cart"

    def update_item_quantity(self, name, new_quantity):
        """
        Updates the quantity of an item in the cart by its name.
        
        Args:
            name (str): Name of the item.
            new_quantity (int): The new quantity for the item.
        
        Returns:
            str: A message indicating whether the item's quantity was updated or if the item was not found.
        """
        for item in self.items:
            if item.name == name:
                item.update_quantity(new_quantity)
                return f"Updated {name} quantity to {new_quantity}"
        return f"{name} not found in cart"

    def calculate_total(self):
        """
        Calculates the total cost of the items in the cart, including tax and delivery fee.
        
        Returns:
            dict: A dictionary containing the subtotal, tax, delivery fee, and total cost.
        """
        subtotal = sum(item.get_subtotal() for item in self.items)
        tax = subtotal * 0.10  # Assume 10% tax rate.
        delivery_fee = 5.00  # Flat delivery fee.
        total = subtotal + tax + delivery_fee
        return {"subtotal": subtotal, "tax": tax, "delivery_fee": delivery_fee, "total": total}

    def view_cart(self):
        """
        Provides a view of the items in the cart.
        
        Returns:
            list: A list of dictionaries with each item's name, quantity, and subtotal price.
        """
        return [{"name": item.name, "quantity": item.quantity, "subtotal": item.get_subtotal()} for item in self.items]



# OrderPlacement Class
class OrderPlacement:
    """
    Represents the process of placing an order, including validation, checkout, and confirmation.
    
    Attributes:
        cart (Cart): The shopping cart containing the items for the order.
        user_profile (UserProfile): The user's profile, including delivery address.
        restaurant_menu (RestaurantMenu): The menu containing available restaurant items.
    """
    def __init__(self, cart, user_profile_dict, restaurant_menu):
        """
        Initializes an OrderPlacement object with the cart, user profile, and restaurant menu.
        
        Args:
            cart (Cart): The shopping cart.
             user_profile_dict (dict): The user's profile.
            restaurant_menu (RestaurantMenu): The restaurant menu with available items.
        """
        self.cart = cart
        # 从字典创建 UserProfile 对象
        self.user_profile = self._create_user_profile_from_dict(user_profile_dict)
        self.restaurant_menu = restaurant_menu

    def _create_user_profile_from_dict(self, user_dict):
        # 假设用户字典中至少包含 'delivery_address' 键
        delivery_address = user_dict.get('delivery_address', 'No address provided')
        return UserProfile(delivery_address)

    def validate_order(self):
        """
        Validates the order by checking if the cart is empty and if all items are available in the restaurant menu.
        
        Returns:
            dict: A dictionary indicating whether the order is valid and an accompanying message.
        """
        if not self.cart.items:
            return {"success": False, "message": "Cart is empty"}

        # Validate the availability of each item in the cart.
        for item in self.cart.items:
            if not self.restaurant_menu.is_item_available(item.name):
                return {"success": False, "message": f"{item.name} is not available"}
        return {"success": True, "message": "Order is valid"}

    def proceed_to_checkout(self):
        """
        Prepares the order for checkout by calculating the total and retrieving the delivery address.
        
        Returns:
            dict: A dictionary containing the cart items, total cost details, and delivery address.
        """
        total_info = self.cart.calculate_total()
        return {
            "items": self.cart.view_cart(),
            "total_info": total_info,
            "delivery_address": self.user_profile.delivery_address,
        }

    def confirm_order(self, payment_method):
        """
        Confirms the order by validating it and processing the payment.
        
        Args:
            payment_method (PaymentMethod): The method of payment to be used.
        
        Returns:
            dict: A dictionary indicating whether the order was confirmed and an order ID if successful.
        """
        if not self.validate_order()["success"]:
            return {"success": False, "message": "Order validation failed"}

        # Process payment using the given payment method.
        payment_success = payment_method.process_payment(self.cart.calculate_total()["total"])

        if payment_success:
            return {
                "success": True,
                "message": "Order confirmed",
                "order_id": "ORD123456",  # Simulate an order ID.
                "estimated_delivery": "45 minutes"
            }
        return {"success": False, "message": "Payment failed"}


# PaymentMethod Class
class PaymentMethod:
    """
    Represents the method of payment for an order.
    """
    def process_payment(self, amount):
        """
        Processes the payment for the given amount.
        
        Args:
            amount (float): The amount to be paid.
        
        Returns:
            bool: True if the payment is successful, False otherwise.
        """
        if amount > 0:
            return True
        return False


# UserProfile Class (for simulating the user's details)
class UserProfile:
    """
    Represents the user's profile, including delivery address.
    
    Attributes:
        delivery_address (str): The user's delivery address.
    """
    def __init__(self, delivery_address):
        """
        Initializes a UserProfile object with a delivery address.
        
        Args:
            delivery_address (str): The user's delivery address.
        """
        self.delivery_address = delivery_address


# RestaurantMenu Class (for simulating available menu items)
class RestaurantMenu:
    """
    Represents the restaurant's menu, including available items.
    
    Attributes:
        available_items (list): A list of items available on the restaurant's menu.
    """
    def __init__(self, available_items):
        """
        Initializes a RestaurantMenu with a list of available items.
        
        Args:
            available_items (list): A list of available menu items.
        """
        self.available_items = available_items

    def is_item_available(self, item_name):
        """
        Checks if a specific item is available in the restaurant's menu.
        
        Args:
            item_name (str): The name of the item to check.
        
        Returns:
            bool: True if the item is available, False otherwise.
        """
        return item_name in self.available_items


# Unit tests for OrderPlacement class
class TestOrderPlacement(unittest.TestCase):
    """
    Unit tests for the OrderPlacement class.
    """
    def setUp(self):
        """
        Sets up the test environment by creating instances of necessary classes.
        """
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.order = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

    def test_validate_order_empty_cart(self):
        """
        Test case for validating an order with an empty cart.
        """
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Cart is empty")

    def test_validate_order_item_not_available(self):
        """
        Test case for validating an order with an unavailable item.
        """
        self.cart.add_item("Pasta", 15.99, 1)
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Pasta is not available")

    def test_validate_order_success(self):
        """
        Test case for successfully validating an order.
        """
        self.cart.add_item("Burger", 8.99, 2)
        result = self.order.validate_order()
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order is valid")

    def test_confirm_order_success(self):
        """
        Test case for confirming an order with successful payment.
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()
        result = self.order.confirm_order(payment_method)
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")
        self.assertEqual(result["order_id"], "ORD123456")

    def test_confirm_order_failed_payment(self):
        """
        Test case for confirming an order with failed payment.
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()

        # Use unittest.mock.patch to simulate failed payment processing.
        with mock.patch.object(payment_method, 'process_payment', return_value=False):
            result = self.order.confirm_order(payment_method)
            self.assertFalse(result["success"])
            self.assertEqual(result["message"], "Payment failed")


if __name__ == "__main__":
    unittest.main()
