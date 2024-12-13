Feature: User Registration
Scenario: Successful Registration
Given the app is running
When I register with "test@example.com" and "Password123"
Then I should see a "Registration successful" message