class UserRegistration:
    def __init__(self):
        """
        Initializes the UserRegistration class with an empty dictionary to store user data.
        Each entry in the dictionary will map an email to a dictionary containing the user's password and confirmation status.
        """
        self.users = {}

    def register(self, email, password, confirm_password):
        """
        Registers a new user.
        
        This function takes an email, password, and password confirmation as input. It performs a series of checks to ensure the registration 
        is valid:
        - Verifies that the email is in a valid format.
        - Ensures that the password matches the confirmation password.
        - Validates that the password meets the strength requirements.
        - Checks if the email is already registered.
        
        If all checks pass, the user is registered, and their email and password are stored in the `users` dictionary, along with a confirmation 
        status set to False (indicating the user is not yet confirmed). A success message is returned.

        Args:
            email (str): The user's email address.
            password (str): The user's password.
            confirm_password (str): Confirmation of the user's password.
        
        Returns:
            dict: A dictionary containing the result of the registration attempt. 
                  On success, it returns {"success": True, "message": "Registration successful, confirmation email sent"}.
                  On failure, it returns {"success": False, "error": "Specific error message"}.
        """
        if not self.is_valid_email(email):
            return {"success": False, "error": "Invalid email format"}  # If email format is invalid, return an error.
        if password != confirm_password:
            return {"success": False, "error": "Passwords do not match"}  # If passwords don't match, return an error.
        if not self.is_strong_password(password):
            return {"success": False, "error": "Password is not strong enough"}  # If password isn't strong, return an error.
        if email in self.users:
            return {"success": False, "error": "Email already registered"}  # If the email is already registered, return an error.

        # Register the user if all conditions are met and return a success message.
        self.users[email] = {"password": password, "confirmed": False}
        return {"success": True, "message": "Registration successful, confirmation email sent"}

    def is_valid_email(self, email):
        """
        Checks if the provided email is valid based on a simple validation rule.
        This rule only checks that the email contains an '@' symbol and has a '.' in the domain part.

        Args:
            email (str): The email address to be validated.
        
        Returns:
            bool: True if the email is valid, False otherwise.
        """
        return "@" in email and "." in email.split("@")[-1]

    def is_strong_password(self, password):
        """
        Checks if the provided password meets the strength requirements.
        A strong password is defined as one that is at least 8 characters long, contains at least one letter, and at least one number.

        Args:
            password (str): The password to be validated.
        
        Returns:
            bool: True if the password is strong, False otherwise.
        """
        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)

    def login(self, email, password):
        """
        Logs in a user if their email and password match the stored credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            dict: A dictionary containing the user profile if login is successful,
                  or an error message if login fails.
        """
        user = self.users.get(email)
        if user and user['password'] == password:
            return {"success": True, "profile": user}
        else:
            return {"success": False, "error": "Login failed: Incorrect email or password"}
# Unit tests for UserRegistration class
import unittest

class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by creating an instance of the UserRegistration class.
        This instance will be used across all test cases.
        """
        self.registration = UserRegistration()

    def test_successful_registration(self):
        """
        Test case for successful user registration.
        It verifies that a valid email and matching strong password results in successful registration.
        """
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])  # Ensures that registration is successful.
        self.assertEqual(result['message'], "Registration successful, confirmation email sent")  # Checks the success message.

    def test_invalid_email(self):
        """
        Test case for invalid email format.
        It verifies that attempting to register with an incorrectly formatted email results in an error.
        """
        result = self.registration.register("userexample.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to invalid email.
        self.assertEqual(result['error'], "Invalid email format")  # Checks the specific error message.

    def test_password_mismatch(self):
        """
        Test case for password mismatch.
        It verifies that when the password and confirmation password do not match, registration fails.
        """
        result = self.registration.register("user@example.com", "Password123", "Password321")
        self.assertFalse(result['success'])  # Ensures registration fails due to password mismatch.
        self.assertEqual(result['error'], "Passwords do not match")  # Checks the specific error message.

    def test_weak_password(self):
        """
        Test case for weak password.
        It verifies that a password not meeting the strength requirements results in an error.
        """
        result = self.registration.register("user@example.com", "pass", "pass")
        self.assertFalse(result['success'])  # Ensures registration fails due to a weak password.
        self.assertEqual(result['error'], "Password is not strong enough")  # Checks the specific error message.

    def test_email_already_registered(self):
        """
        Test case for duplicate email registration.
        It verifies that attempting to register an email that has already been registered results in an error.
        """
        self.registration.register("user@example.com", "Password123", "Password123")  # Register a user.
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to the email already being registered.
        self.assertEqual(result['error'], "Email already registered")  # Checks the specific error message.

if __name__ == '__main__':
    unittest.main()
