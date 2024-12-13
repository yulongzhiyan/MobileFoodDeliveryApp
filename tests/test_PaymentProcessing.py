import unittest
from unittest import mock  # 导入mock模块，用于模拟支付网关的响应。


# 支付处理类
class PaymentProcessing:
    """
    支付处理类负责使用不同的支付方法进行支付的验证和处理。

    属性：
        available_gateways (list): 支持的支付网关列表，如 'credit_card' 和 'paypal'。
    """

    def __init__(self):
        """
        初始化支付处理类，设置可用的支付网关。
        """
        self.available_gateways = ["credit_card", "paypal"]

    def validate_payment_method(self, payment_method, payment_details):
        """
        验证选定的支付方法及其相关详情。

        参数：
            payment_method (str): 选定的支付方法（例如 'credit_card', 'paypal'）。
            payment_details (dict): 支付方法所需的详情（例如卡号、有效期）。

        返回：
            bool: 如果支付方法和详情有效，返回 True，否则引发 ValueError。

        引发：
            ValueError: 如果支付方法不支持或支付详情无效。
        """
        # 检查支付方法是否受支持。
        if payment_method not in self.available_gateways:
            raise ValueError("Invalid payment method")

        # 如果选定方法是 'credit_card'，则验证信用卡详情。
        if payment_method == "credit_card":
            if not self.validate_credit_card(payment_details):
                raise ValueError("Invalid credit card details")

        # 验证通过。
        return True

    def validate_credit_card(self, details):
        """
        验证信用卡详情（例如卡号、有效期、CVV）。

        参数：
            details (dict): 包含 'card_number', 'expiry_date', 和 'cvv' 的字典。

        返回：
            bool: 如果卡详情有效，返回 True，否则返回 False。
        """
        card_number = details.get("card_number", "")
        expiry_date = details.get("expiry_date", "")
        cvv = details.get("cvv", "")

        # 基本验证：检查卡号是否为16位，CVV是否为3位。
        if len(card_number) != 16 or len(cvv) != 3 :
            return False

        # 可以在这里添加更高级的验证，如Luhn算法用于卡号验证。
        return True

    def process_payment(self, order, payment_method, payment_details):
        """
        处理订单的支付，验证支付方法并与支付网关交互。

        参数：
            order (dict): 订单详情，包括总金额。
            payment_method (str): 选定的支付方法。
            payment_details (dict): 支付方法所需的详情。

        返回：
            str: 消息，指示支付是否成功或失败。
        """
        try:
            # 验证支付方法和详情。
            self.validate_payment_method(payment_method, payment_details)

            # 模拟与支付网关的交互。
            payment_response = self.mock_payment_gateway(payment_method, payment_details, order["total_amount"])

            # 根据支付网关的响应返回适当的消息。
            if payment_response["status"] == "success":
                return "Payment successful, Order confirmed"
            else:
                return "Payment failed, please try again"

        except Exception as e:
            # 捕获并返回任何验证或处理错误。
            return f"Error: {str(e)}"

    def mock_payment_gateway(self, method, details, amount):
        """
        模拟与支付网关的交互以处理支付。

        参数：
            method (str): 支付方法（例如 'credit_card'）。
            details (dict): 支付详情（例如卡号）。
            amount (float): 要收取的金额。

        返回：
            dict: 模拟的支付网关响应，指示成功或失败。
        """
        # 模拟特定卡号的卡片拒绝。
        if method == "credit_card" and details["card_number"] == "1111222233334444":
            return {"status": "failure", "message": "Card declined"}

        # 模拟成功的交易。
        return {"status": "success", "transaction_id": "abc123"}


# PaymentProcessing类的单元测试
class TestPaymentProcessing(unittest.TestCase):
    """
    PaymentProcessing类的单元测试，确保支付验证和处理工作正确。
    """
    def setUp(self):
        """
        初始化测试环境，创建PaymentProcessing类的实例。
        """
        self.payment_processing = PaymentProcessing()

    def test_validate_payment_method_success(self):
        """
        测试用例：成功验证有效的支付方法（'credit_card'）和有效详情。
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment_processing.validate_payment_method("credit_card", payment_details)
        self.assertTrue(result)  # 验证结果应为True

    def test_validate_payment_method_invalid_gateway(self):
        """
        测试用例：由于不支持的支付方法（'bitcoin'）导致验证失败。
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        with self.assertRaises(ValueError) as context:  # 预期会抛出ValueError异常
            self.payment_processing.validate_payment_method("bitcoin", payment_details)
        self.assertEqual(str(context.exception), "Invalid payment method")  # 验证异常信息是否正确

    def test_validate_credit_card_invalid_details(self):
        """
        测试用例：由于无效的信用卡详情（无效的卡号和CVV）导致验证失败。
        """
        payment_details = {"card_number": "1234", "expiry_date": "12/25", "cvv": "12"}  # 无效的卡号和CVV
        result = self.payment_processing.validate_credit_card(payment_details)
        self.assertFalse(result)  # 验证结果应为False

    def test_process_payment_success(self):
        """
        测试用例：使用有效的详情通过'credit_card'方法成功处理支付。
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # 使用mock模拟支付网关成功的支付响应。
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")  # 验证返回消息是否正确

    def test_process_payment_failure(self):
        """
        测试用例：由于信用卡被拒绝导致支付失败。
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1111222233334444", "expiry_date": "12/25", "cvv": "123"}  # 模拟被拒绝的卡

        # 使用mock模拟支付网关失败的支付响应。
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "failure"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment failed, please try again")  # 验证返回消息是否正确

    def test_process_payment_invalid_method(self):
        """
        测试用例：由于无效的支付方法（'bitcoin'）导致支付处理失败。
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # 不需要模拟，方法将直接抛出错误。
        result = self.payment_processing.process_payment(order, "bitcoin", payment_details)
        self.assertIn("Error: Invalid payment method", result)  # 验证返回消息中是否包含错误信息

    # 额外的测试 1: 测试缺少必需字段
    def test_validate_payment_method_missing_fields(self):
        """
        测试支付详情缺少必需字段时的验证失败（如缺少 card_number）。
        """
        payment_details = {"expiry_date": "12/25", "cvv": "123"}  # 缺少 card_number 字段
        with self.assertRaises(ValueError) as context:  # 应抛出 ValueError 异常
            self.payment_processing.validate_payment_method("credit_card", payment_details)
        self.assertEqual(str(context.exception), "Invalid credit card details")  # 异常信息应为 'Invalid credit card details'

    # 额外的测试 2: 测试 PayPal 支付成功
    def test_process_payment_paypal_success(self):
        """
        测试 PayPal 支付成功的情况。
        """
        order = {"total_amount": 50.00}  # 订单金额为 50.00
        payment_details = {"paypal_account": "user@example.com"}

        # 使用 mock 来模拟 PayPal 支付网关返回成功的响应
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "paypal", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")  # 期望返回支付成功的信息

    # 额外的测试 3: 测试 PayPal 支付失败
    def test_process_payment_paypal_failure(self):
        """
        测试 PayPal 支付失败的情况。
        """
        order = {"total_amount": 50.00}
        payment_details = {"paypal_account": "user@example.com"}

        # 使用 mock 来模拟 PayPal 支付网关返回失败的响应
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "failure"}):
            result = self.payment_processing.process_payment(order, "paypal", payment_details)
            self.assertEqual(result, "Payment failed, please try again")  # 期望返回支付失败的信息

    # 额外的测试 4: 测试支付金额为零
    def test_process_payment_zero_amount(self):
        """
        测试支付金额为零的情况。
        """
        order = {"total_amount": 0.00}  # 订单金额为 0.00
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # 使用 mock 来模拟支付网关返回成功的响应
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")  # 期望返回支付成功的信息
if __name__ == "__main__":
    unittest.main()  # Run the unit tests.
