import unittest

# 导入单元测试和集成测试的测试用例
from tests.test_UserRegistration import UserRegistration
from tests.test_OrderPlacement import Cart, OrderPlacement
from tests.test_PaymentProcessing import PaymentProcessing
from tests.test_RestaurantBrowsing import RestaurantBrowsing, RestaurantDatabase

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # # 初始化测试环境，设置必要的组件
        self.registration = UserRegistration()
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)
        self.cart = Cart()
        self.payment = PaymentProcessing()

    def test_order_process_flow(self):
        # 测试整个订单处理流程
        # 用户注册
        reg_result = self.registration.register(
            "user@example.com", "Password123", "Password123"
        )
        self.assertTrue(reg_result['success'])
        # 用户登录（假设有登录方法）
        user_profile_dict= self.registration.login("user@example.com", "Password123")
        # 用户浏览餐厅并将商品加入购物车
        restaurants = self.browsing.search_by_cuisine(cuisine_type="Italian")
        self.assertGreaterEqual(len(restaurants), 1)
        # menu = restaurants[0]['menu']
        menu = [{"name": "Spaghetti Carbonara", "price": 12}, {"name": "Margherita Pizza", "price": 10}]
        self.cart.add_item(menu[0]['name'], menu[0]['price'], 1)
        # 将第一个菜单项加入购物车
        # 用户下订单
        order = OrderPlacement(self.cart, user_profile_dict, menu)
        # 创建PaymentProcessing实例
        payment_processor = PaymentProcessing()

        # 用户进行支付
        payment_details = {
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123"
        }
        # 获取订单总金额
        order_total = self.cart.calculate_total()["total"]
        # 调用PaymentProcessing的process_payment方法
        payment_result = payment_processor.process_payment({"total_amount": order_total}, "credit_card",
                                                           payment_details)
        self.assertEqual(payment_result, "Payment successful, Order confirmed")

# 定义load_tests函数，用于加载测试用例
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    # 加载集成测试
    suite.addTest(unittest.makeSuite(TestIntegration))
    # 发现并添加单元测试
    suite.addTest(loader.discover('tests'))
    return suite
# 运行测试
if __name__ == '__main__':
    unittest.main()