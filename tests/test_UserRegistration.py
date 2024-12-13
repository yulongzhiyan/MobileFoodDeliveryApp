class UserRegistration:
    def __init__(self):
        """
        初始化UserRegistration类，使用一个空字典来存储用户数据。
        字典中的每个条目将电子邮件映射到包含用户密码和确认状态的字典。
        """
        self.users = {}

    def register(self, email, password, confirm_password):
        """
        注册新用户。

        该函数接收电子邮件、密码和密码确认作为输入。它执行一系列检查以确保注册有效：
        - 验证电子邮件是否在有效格式。
        - 确保密码与确认密码匹配。
        - 验证密码是否符合强度要求。
        - 检查电子邮件是否已经注册。

        如果所有检查通过，用户将被注册，他们的电子邮件和密码将被存储在`users`字典中，确认状态设置为False（表示用户尚未确认）。返回成功消息。

        参数：
            email (str): 用户的电子邮件地址。
            password (str): 用户的密码。
            confirm_password (str): 用户密码的确认。

        返回：
            dict: 包含注册尝试结果的字典。
                  成功时，返回{"success": True, "message": "Registration successful, confirmation email sent"}。
                  失败时，返回{"success": False, "error": "具体错误消息"}。
        """
        if not self.is_valid_email(email):
            return {"success": False, "error": "Invalid email format"}  # 如果电子邮件格式无效，返回错误。
        if password != confirm_password:
            return {"success": False, "error": "Passwords do not match"}  # 如果密码不匹配，返回错误。
        if not self.is_strong_password(password):
            return {"success": False,
                    "error": "Password is not strong enough"}  # 如果密码不够强，返回错误。
        if email in self.users:
            return {"success": False,
                    "error": "Email already registered"}  # 如果电子邮件已经注册，返回错误。

        # 如果所有条件都满足，注册用户并返回成功消息。
        self.users[email] = {"password": password, "confirmed": False}
        return {"success": True, "message": "Registration successful, confirmation email sent"}

    def is_valid_email(self, email):
        """
        根据简单的验证规则检查提供的电子邮件是否有效。
        此规则仅检查电子邮件是否包含'@'符号，并在域名部分有一个'.'。

        参数：
            email (str): 要验证的电子邮件地址。

        返回：
            bool: 如果电子邮件有效，返回True，否则返回False。
        """
        return "@" in email and "." in email.split("@")[-1]

    def is_strong_password(self, password):
        """
        检查提供的密码是否符合强度要求。
        强密码定义为至少8个字符长，至少包含一个字母和至少一个数字的密码。

        参数：
            password (str): 要验证的密码。

        返回：
            bool: 如果密码强，返回True，否则返回False。
        """
        # c.isdigit判断是否为阿拉伯数字  c.isalpha判断是否为字母
        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password) and not any(c.isspace() for c in password)

    def login(self, email, password):
        """
        如果用户的电子邮件和密码与存储的凭据匹配，则登录用户。

        参数：
            email (str): 用户的电子邮件地址。
            password (str): 用户的密码。

        返回：
            dict: 如果登录成功，包含用户资料的字典，
                  如果登录失败，返回错误消息。
        """
        user = self.users.get(email)
        if user and user['password'] == password:
            return {"success": True, "profile": user}
        else:
            return {"success": False, "error": "Login failed: Incorrect email or password"}
# UserRegistration类的单元测试
import unittest

class TestUserRegistration(unittest.TestCase):
    """
    UserRegistration类的单元测试，测试用户注册的各种情况。
    """

    def setUp(self):
        """
        初始化测试环境，创建UserRegistration类的实例。
        这个实例将被用于所有的测试用例。
        """
        self.registration = UserRegistration()

    def test_successful_registration(self):
        """
        测试用例：成功注册用户。
        验证有效的电子邮件和匹配的强密码可以成功注册。
        """
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])  # 确保注册成功。
        self.assertEqual(result['message'],
                         "Registration successful, confirmation email sent")  # 检查成功消息。

    def test_invalid_email(self):
        """
        测试用例：无效的电子邮件格式。
        验证使用格式错误的电子邮件尝试注册会返回错误。
        """
        result = self.registration.register("userexample.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # 确保因电子邮件无效而注册失败。
        self.assertEqual(result['error'], "Invalid email format")  # 检查具体的错误消息。

    def test_password_mismatch(self):
        """
        测试用例：密码不匹配。
        验证当密码和确认密码不匹配时，注册失败。
        """
        result = self.registration.register("user@example.com", "Password123", "Password321")
        self.assertFalse(result['success'])  # 确保因密码不匹配而注册失败。
        self.assertEqual(result['error'], "Passwords do not match")  # 检查具体的错误消息。

    def test_weak_password(self):
        """
        测试用例：弱密码。
        验证不符合强度要求的密码会导致错误。
        """
        result = self.registration.register("user@example.com", "pass", "pass")
        self.assertFalse(result['success'])  # 确保因密码弱而注册失败。
        self.assertEqual(result['error'], "Password is not strong enough")  # 检查具体的错误消息。

    def test_email_already_registered(self):
        """
        测试用例：电子邮件已注册。
        验证尝试注册已存在的电子邮件会导致错误。
        """
        # 首先注册一个用户
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])
        # 然后尝试再次注册同一个电子邮件
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # 确保因电子邮件已注册而注册失败。
        self.assertEqual(result['error'], "Email already registered")  # 检查具体的错误消息。

    # 新的测试 1: 测试空白密码
    def test_blank_password(self):
        """
        测试用例：空白密码。
        验证尝试用空密码注册会导致错误。
        """
        result = self.registration.register("user@example.com", "", "")
        self.assertFalse(result['success'])  # 确保因密码为空而注册失败。
        self.assertEqual(result['error'],
                         "Password is not strong enough")  # 检查空白密码的错误消息。

    # 新的测试 2: 测试无效邮箱格式
    def test_invalid_email_format(self):
        """
        测试用例：无效的电子邮件格式（缺少'@'符号）。
        验证尝试用缺少'@'的电子邮件注册会导致错误。
        """
        result = self.registration.register("userexample.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # 确保因电子邮件格式无效而注册失败。
        self.assertEqual(result['error'], "Invalid email format")  # 检查缺少'@'的错误消息。

    # 新的测试 3: 测试密码只包含数字
    def test_password_with_only_numbers(self):
        """
        测试用例：密码只包含数字。
        验证包含只有数字的密码被认为是弱密码。
        """
        result = self.registration.register("user@example.com", "12345678", "12345678")
        self.assertFalse(result['success'])  # 确保因密码弱而注册失败。
        self.assertEqual(result['error'],
                         "Password is not strong enough")  # 检查只包含数字的密码的错误消息。

    # 新的测试 4: 测试邮箱包含特殊字符
    def test_email_with_special_characters(self):
        """
        测试用例：包含特殊字符的电子邮件。
        验证包含有效特殊字符的电子邮件被接受。
        """
        result = self.registration.register("user+123@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])  # 确保注册成功。
        self.assertEqual(result['message'],
                         "Registration successful, confirmation email sent")  # 检查成功消息。

    # 新的测试 5: 测试密码包含空格
    def test_password_with_spaces(self):
        """
        测试用例：密码包含空格。
        验证包含空格的密码被认为是弱密码。
        """
        result = self.registration.register("user@example.com", "Pass word123", "Pass word123")
        self.assertFalse(result['success'])  # 确保因密码包含空格而注册失败。
        self.assertEqual(result['error'],"Password is not strong enough")  # 检查包含空格的密码的错误消息。

if __name__ == '__main__':
    unittest.main()
