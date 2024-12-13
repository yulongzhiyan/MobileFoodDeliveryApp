class RestaurantBrowsing:
    """
    A class for browsing restaurants in a database based on various criteria like cuisine type, location, and rating.
    
    Attributes:
        database (RestaurantDatabase): An instance of RestaurantDatabase that holds restaurant data.
    """

    def __init__(self, database):
        """
        Initialize RestaurantBrowsing with a reference to a restaurant database.
        
        Args:
            database (RestaurantDatabase): The database object containing restaurant information.
        """
        self.database = database

    def search_by_cuisine(self, cuisine_type):
        """
        Search for restaurants based on their cuisine type.
        
        Args:
            cuisine_type (str): The type of cuisine to filter by (e.g., "Italian").
        
        Returns:
            list: A list of restaurants that match the given cuisine type.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['cuisine'].lower() == cuisine_type.lower()]

    def search_by_location(self, location):
        """
        Search for restaurants based on their location.
        
        Args:
            location (str): The location to filter by (e.g., "Downtown").
        
        Returns:
            list: A list of restaurants that are located in the specified area.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['location'].lower() == location.lower()]

    def search_by_rating(self, min_rating):
        """
        Search for restaurants based on their minimum rating.
        
        Args:
            min_rating (float): The minimum acceptable rating to filter by (e.g., 4.0).
        
        Returns:
            list: A list of restaurants that have a rating greater than or equal to the specified rating.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['rating'] >= min_rating]

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        """
        Search for restaurants based on multiple filters: cuisine type, location, and/or rating.
        
        Args:
            cuisine_type (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            min_rating (float, optional): The minimum acceptable rating to filter by.
        
        Returns:
            list: A list of restaurants that match all specified filters.
        """
        results = self.database.get_restaurants()  # Start with all restaurants

        if cuisine_type:
            results = [restaurant for restaurant in results 
                       if restaurant['cuisine'].lower() == cuisine_type.lower()]

        if location:
            results = [restaurant for restaurant in results 
                       if restaurant['location'].lower() == location.lower()]

        if min_rating:
            results = [restaurant for restaurant in results 
                       if restaurant['rating'] >= min_rating]

        return results


class RestaurantDatabase:
    """
    A simulated in-memory database that stores restaurant information.
    
    Attributes:
        restaurants (list): A list of dictionaries, where each dictionary represents a restaurant with
                            fields like name, cuisine, location, rating, price range, and delivery status.
    """

    def __init__(self):
        """
        Initialize the RestaurantDatabase with a predefined set of restaurant data.
        """
        self.restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.5, 
             "price_range": "$$", "delivery": True,
             "menu": [{"name": "Spaghetti Carbonara", "price": 12}, {"name": "Margherita Pizza", "price": 10}]},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8, 
             "price_range": "$$$", "delivery": False,
             "menu": [{"name": "Sushi Platter", "price": 15},{"name": "Miso Soup", "price": 5}]},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown", "rating": 4.0, 
             "price_range": "$", "delivery": True,
             "menu": [{"name": "Whopper", "price": 6},{"name": "Fries", "price": 2}]},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown", "rating": 4.2, 
             "price_range": "$", "delivery": True,
             "menu": [{"name": "Chicken Taco", "price": 3},{"name": "Nachos", "price": 5}]},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown", "rating": 3.9, 
             "price_range": "$$", "delivery": True,
             "menu": [{"name": "Pepperoni Pizza", "price": 12},{"name": "Garlic Bread", "price": 4}]}
        ]

    def get_restaurants(self):
        """
        Retrieve the list of restaurants in the database.
        
        Returns:
            list: A list of dictionaries, where each dictionary contains restaurant information.
        """
        return self.restaurants


class RestaurantSearch:
    """
    A class that interfaces with RestaurantBrowsing to perform restaurant searches based on user input.
    
    Attributes:
        browsing (RestaurantBrowsing): An instance of RestaurantBrowsing used to perform searches.
    """

    def __init__(self, browsing):
        """
        Initialize the RestaurantSearch with a reference to a RestaurantBrowsing instance.
        
        Args:
            browsing (RestaurantBrowsing): An instance of the RestaurantBrowsing class.
        """
        self.browsing = browsing

    def search_restaurants(self, cuisine=None, location=None, rating=None):
        """
        Search for restaurants using multiple optional filters: cuisine, location, and rating.
        
        Args:
            cuisine (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            rating (float, optional): The minimum rating to filter by.
        
        Returns:
            list: A list of restaurants that match the provided search criteria.
        """
        results = self.browsing.search_by_filters(cuisine_type=cuisine, location=location, min_rating=rating)
        return results


# Unit tests for RestaurantBrowsing class
import unittest

class TestRestaurantBrowsing(unittest.TestCase):
    """
    Unit tests for the RestaurantBrowsing class, testing various search functionalities.
    """

    def setUp(self):
        """
        Set up the test case by initializing a RestaurantDatabase and RestaurantBrowsing instance.
        """
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

    def test_search_by_cuisine(self):
        """
        Test searching for restaurants by cuisine type.
        """
        results = self.browsing.search_by_cuisine("Italian")
        self.assertEqual(len(results), 2)  # There should be 2 Italian restaurants
        self.assertTrue(all([restaurant['cuisine'] == "Italian" for restaurant in results]))  # Check if all returned restaurants are Italian

    def test_search_by_location(self):
        """
        Test searching for restaurants by location.
        """
        results = self.browsing.search_by_location("Downtown")
        self.assertEqual(len(results), 2)  # There should be 2 restaurants located Downtown
        self.assertTrue(all([restaurant['location'] == "Downtown" for restaurant in results]))  # Check if all returned restaurants are in Downtown

    def test_search_by_rating(self):
        """
        Test searching for restaurants by minimum rating.
        """
        results = self.browsing.search_by_rating(4.0)
        self.assertEqual(len(results), 4)  # There should be 4 restaurants with a rating >= 4.0
        self.assertTrue(all([restaurant['rating'] >= 4.0 for restaurant in results]))  # Check if all returned restaurants have a rating >= 4.0

    def test_search_by_filters(self):
        """
        Test searching for restaurants by multiple filters (cuisine type, location, and minimum rating).
        """
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
        self.assertEqual(len(results), 1)  # Only one restaurant should match all the filters
        self.assertEqual(results[0]['name'], "Italian Bistro")  # The result should be "Italian Bistro"


if __name__ == '__main__':
    unittest.main()
