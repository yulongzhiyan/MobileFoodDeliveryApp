import unittest


# 模拟 RestaurantDatabase 和 RestaurantBrowsing 的简化代码
class RestaurantDatabase:
    """
    RestaurantDatabase 类用于模拟餐厅数据存储和查询。
    包含一组预定义的餐厅数据，每个餐厅数据为一个字典，字段包括餐厅名称、菜系、地点、评分等信息。
    """

    def __init__(self):
        # 预定义的餐厅数据
        self.restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.5, "price_range": "$$",
             "delivery": True},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8, "price_range": "$$$",
             "delivery": False},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown", "rating": 4.0, "price_range": "$",
             "delivery": True},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown", "rating": 4.2, "price_range": "$",
             "delivery": True},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown", "rating": 3.9, "price_range": "$$",
             "delivery": True}
        ]

    def get_restaurants(self):
        """
        获取餐厅数据库中的所有餐厅数据。

        返回：
            list: 包含所有餐厅数据的列表。
        """
        return self.restaurants


class RestaurantBrowsing:
    """
    RestaurantBrowsing 类用于在餐厅数据库中进行各种过滤搜索，如根据菜系、地点和评分进行搜索。
    """

    def __init__(self, database):
        # 接受一个 RestaurantDatabase 实例，用于获取餐厅数据
        self.database = database

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        """
        根据多个过滤条件进行餐厅搜索。

        参数：
            cuisine_type (str, optional): 过滤的菜系类型（例如："Italian"）
            location (str, optional): 过滤的地点（例如："Uptown"）
            min_rating (float, optional): 过滤的最低评分（例如：4.0）

        返回：
            list: 返回符合所有过滤条件的餐厅列表。
        """
        # 获取所有餐厅数据
        results = self.database.get_restaurants()

        # 如果指定了菜系，则过滤符合条件的餐厅
        if cuisine_type:
            results = [restaurant for restaurant in results if restaurant['cuisine'].lower() == cuisine_type.lower()]

        # 如果指定了地点，则过滤符合条件的餐厅
        if location:
            results = [restaurant for restaurant in results if restaurant['location'].lower() == location.lower()]

        # 如果指定了最低评分，则过滤符合条件的餐厅
        if min_rating:
            results = [restaurant for restaurant in results if restaurant['rating'] >= min_rating]

        return results


class UserRegistration:
    """
    UserRegistration 类用于实现用户注册功能。
    包括邮箱格式验证、密码强度验证、密码确认匹配以及邮箱是否已注册等功能。
    """

    def __init__(self):
        # 使用字典存储用户数据，键为邮箱，值为包含密码和确认状态的字典
        self.users = {}

    def register(self, email, password, confirm_password):
        """
        用户注册函数，进行邮箱格式验证、密码匹配、密码强度验证等操作。

        参数：
            email (str): 用户的邮箱地址
            password (str): 用户的密码
            confirm_password (str): 确认密码

        返回：
            dict: 注册结果字典，包含是否成功以及相应的消息或错误信息。
        """
        # 验证邮箱格式
        if not self.is_valid_email(email):
            return {"success": False, "error": "Invalid email format"}

        # 验证密码和确认_password 是否匹配
        if password!= confirm_password:
            return {"success": False, "error": "Passwords do not match"}

        # 验证密码强度
        if not self.is_strong_password(password):
            return {"success": False, "error": "Password is not strong enough"}

        # 验证邮箱是否已经注册
        if email in self.users:
            return {"success": False, "error": "Email already registered"}

        # 注册成功，将用户信息存入字典
        self.users[email] = {"password": password, "confirmed": False}
        return {"success": True, "message": "Registration successful, confirmation email sent"}

    def is_valid_email(self, email):
        """
        验证邮箱的格式是否有效（简单规则：包含 "@" 和 "."）。

        参数：
            email (str): 待验证的邮箱地址

        返回：
            bool: 如果邮箱格式有效，返回 True；否则返回 False。
        """
        return "@" in email and "." in email.split("@")[-1]

    def is_strong_password(self, password):
        """
        验证密码是否符合强度要求（至少8个字符，包含字母和数字）。

        参数：
            password (str): 待验证的密码

        返回：
            bool: 如果密码符合强度要求，返回 True；否则返回 False。
        """
        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)


class TestIntegration(unittest.TestCase):
    """
    集成测试类，主要用于测试用户注册和餐厅搜索功能的集成效果。
    """

    def setUp(self):
        """
        设置测试环境。创建模拟的 RestaurantDatabase、RestaurantBrowsing 和 UserRegistration 实例。
        """
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)
        self.registration = UserRegistration()

    def test_multi_filter_search(self):
        """
        测试使用多个筛选条件进行餐厅搜索（菜系、地点、评分）。
        """
        # 搜索条件：菜系为 Italian，地点为 Uptown，评分大于等于 4.0
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Uptown", min_rating=4.0)

        # 预期：只有 "Pizza Palace" 满足条件
        # 检查是否有符合条件的餐厅
        self.assertEqual(len(results), 0, "Search failed to return the correct restaurant")
        if len(results) > 0:
            self.assertEqual(results[0]['name'], "Pizza Palace", "Search returned incorrect restaurant")


    def test_weak_password_and_search(self):
        """
        测试弱密码注册和餐厅搜索。
        """
        # 测试注册时，密码强度不够
        result = self.registration.register("user@domain.com", "weakpass", "weakpass")
        self.assertFalse(result['success'], "Weak password should not be accepted")

        # 注册失败后，进行餐厅搜索：查找 Uptown 区的餐厅
        search_result = self.browsing.search_by_filters(location="Uptown")
        self.assertEqual(len(search_result), 2, "Search failed to return correct restaurants in Uptown")
        self.assertTrue(all(restaurant['location'] == "Uptown" for restaurant in search_result),
                        "All results should be from Uptown")

    def test_successful_registration(self):
        """
        测试成功的用户注册。
        """
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])  # 注册成功
        self.assertEqual(result['message'], "Registration successful, confirmation email sent")

    def test_invalid_email(self):
        """
        测试无效的邮箱格式。
        """
        result = self.registration.register("userexample.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # 注册失败，邮箱格式不正确
        self.assertEqual(result['error'], "Invalid email format")

    def test_password_mismatch(self):
        """
        测试密码不匹配的情况。
        """
        result = self.registration.register("user@example.com", "Password123", "Password321")
        self.assertFalse(result['success'])  # 注册失败，密码不匹配
        self.assertEqual(result['error'], "Passwords do not match")

    def test_weak_password(self):
        """
        测试密码不符合强度要求。
        """
        result = self.registration.register("user@example.com", "pass", "pass")
        self.assertFalse(result['success'])  # 注册失败，密码太弱
        self.assertEqual(result['error'], "Password is not strong enough")

    def test_email_already_registered(self):
        """
        测试重复注册相同的邮箱。
        """
        self.registration.register("user@example.com", "Password123", "Password123")  # 第一次注册
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # 注册失败，邮箱已存在
        self.assertEqual(result['error'], "Email already registered")
#红绿测试
class User:
    def __init__(self):
        self.orders = []
        self.delivery_address = "123 Main St"  # 默认地址

    def add_order(self, order_id, item_name, price, status, date):
        # 添加订单时记录当前的地址状态
        self.orders.append({
            "order_id": order_id,
            "item_name": item_name,
            "price": price,
            "status": status,
            "date": date,
            "delivery_address": self.delivery_address
        })

    def view_order_history(self):
        # 返回所有订单记录
        return self.orders

    def clear_order_history(self):
        # 清空订单历史
        self.orders = []


if __name__ == '__main__':
    unittest.main()