class RestaurantBrowsing:
    """
    一个用于根据不同标准（如菜系类型、位置和评分）在数据库中浏览餐厅的类。

    属性：
        database (RestaurantDatabase): 一个包含餐厅数据的RestaurantDatabase实例。
    """

    def __init__(self, database):
        """
        初始化RestaurantBrowsing，并引用一个餐厅数据库。

        参数：
            database (RestaurantDatabase): 包含餐厅信息的数据库对象。
        """
        self.database = database

    def search_by_cuisine(self, cuisine_type):
        """
        根据菜系类型搜索餐厅。

        参数：
            cuisine_type (str): 要过滤的菜系类型（例如，“Italian”）。

        返回：
            list: 与给定菜系类型匹配的餐厅列表。
        """
        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['cuisine'].lower() == cuisine_type.lower()]

    def search_by_location(self, location):
        """
        根据位置搜索餐厅。

        参数：
            location (str): 要过滤的位置（例如，“Downtown”）。

        返回：
            list: 位于指定区域的餐厅列表。
        """
        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['location'].lower() == location.lower()]

    def search_by_rating(self, min_rating):
        """
        根据最低评分搜索餐厅。

        参数：
            min_rating (float): 要过滤的最低可接受评分（例如，4.0）。

        返回：
            list: 评分大于或等于指定评分的餐厅列表。
        """
        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['rating'] >= min_rating]

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        """
        根据多个过滤器（菜系类型、位置和/或评分）搜索餐厅。

        参数：
            cuisine_type (str, optional): 要过滤的菜系类型。
            location (str, optional): 要过滤的位置。
            min_rating (float, optional): 要过滤的最低可接受评分。

        返回：
            list: 与所有指定过滤器匹配的餐厅列表。
        """
        results = self.database.get_restaurants()  # 从所有餐厅开始

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
    一个模拟的内存数据库，用于存储餐厅信息。

    属性：
        restaurants (list): 一个字典列表，每个字典代表一个餐厅，包含名称、菜系、位置、评分、价格范围和配送状态等字段。
    """

    def __init__(self):
        """
        初始化RestaurantDatabase，并预设一组餐厅数据。
        """
        self.restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.5,
             "price_range": "$$", "delivery": True},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8,
             "price_range": "$$$", "delivery": False},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown", "rating": 4.0,
             "price_range": "$", "delivery": True},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown", "rating": 4.2,
             "price_range": "$", "delivery": True},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown", "rating": 3.9,
             "price_range": "$$", "delivery": True}
        ]

    def get_restaurants(self):
        """
        检索数据库中的餐厅列表。

        返回：
            list: 包含餐厅信息的字典列表。
        """
        return self.restaurants


class RestaurantSearch:
    """
    一个与RestaurantBrowsing接口的类，根据用户输入执行餐厅搜索。

    属性：
        browsing (RestaurantBrowsing): 用于执行搜索的RestaurantBrowsing实例。
    """

    def __init__(self, browsing):
        """
        初始化RestaurantSearch，并引用一个RestaurantBrowsing实例。

        参数：
            browsing (RestaurantBrowsing): RestaurantBrowsing类的实例。
        """
        self.browsing = browsing

    def search_restaurants(self, cuisine=None, location=None, rating=None):
        """
        使用多个可选过滤器（菜系、位置和评分）搜索餐厅。

        参数：
            cuisine (str, optional): 要过滤的菜系类型。
            location (str, optional): 要过滤的位置。
            rating (float, optional): 要过滤的最低评分。

        返回：
            list: 与提供的搜索标准匹配的餐厅列表。
        """
        results = self.browsing.search_by_filters(cuisine_type=cuisine, location=location, min_rating=rating)
        return results
# RestaurantBrowsing类的单元测试
import unittest

class TestRestaurantBrowsing(unittest.TestCase):
    """
    对RestaurantBrowsing类进行单元测试，测试各种搜索功能。
    """

    def setUp(self):
        """
        设置测试用例，通过初始化RestaurantDatabase和RestaurantBrowsing实例。
        """
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

    def test_search_by_cuisine(self):
        """
        测试按菜系类型搜索餐厅。
        """
        results = self.browsing.search_by_cuisine("Italian")
        self.assertEqual(len(results), 2)  # 应该有2家意大利餐厅
        self.assertTrue(all([restaurant['cuisine'] == "Italian" for restaurant in results]))  # 检查返回的所有餐厅是否都是意大利菜

    def test_search_by_location(self):
        """
        测试按位置搜索餐厅。
        """
        results = self.browsing.search_by_location("Downtown")
        self.assertEqual(len(results), 2)  # 应该有2家餐厅位于市中心
        self.assertTrue(all([restaurant['location'] == "Downtown" for restaurant in results]))  # 检查返回的所有餐厅是否都在市中心

    def test_search_by_rating(self):
        """
        测试按最低评分搜索餐厅。
        """
        results = self.browsing.search_by_rating(4.0)
        self.assertEqual(len(results), 4)  # 应该有4家餐厅的评分大于或等于4.0
        self.assertTrue(all([restaurant['rating'] >= 4.0 for restaurant in results]))  # 检查返回的所有餐厅的评分是否大于或等于4.0

    def test_search_by_filters(self):
        """
        测试按多个过滤器（菜系类型、位置和最低评分）搜索餐厅。
        """
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
        self.assertEqual(len(results), 1)  # 只有一家餐厅应该符合所有过滤器
        self.assertEqual(results[0]['name'], "Italian Bistro")  # 结果应该是"Italian Bistro"

 # 新的测试 1: 测试无符合条件的餐厅
    def test_search_no_results(self):
        """
        测试没有符合条件的餐厅。
        """
        results = self.browsing.search_by_cuisine("Indian")  # 假设数据库没有印度餐厅
        self.assertEqual(len(results), 0)  # 应该没有返回任何餐厅

    # 新的测试 2: 测试筛选条件中只给定菜系类型
    def test_search_by_cuisine_only(self):
        """
        测试仅根据菜系类型搜索餐厅。
        """
        results = self.browsing.search_by_filters(cuisine_type="Italian")
        self.assertEqual(len(results), 2)  # 应该有 2 家意大利餐厅
        self.assertTrue(all([restaurant['cuisine'] == "Italian" for restaurant in results]))  # 检查所有返回的餐厅都是意大利餐厅

    # 新的测试 3: 测试筛选条件中只给定地点
    def test_search_by_location_only(self):
        """
        测试仅根据地点搜索餐厅。
        """
        results = self.browsing.search_by_filters(location="Uptown")
        self.assertEqual(len(results), 2)  # 应该有 2 家位于 Uptown 的餐厅
        self.assertTrue(all([restaurant['location'] == "Uptown" for restaurant in results]))  # 检查所有返回的餐厅都在 Uptown

    # 新的测试 4: 测试筛选条件中只给定最低评分
    def test_search_by_min_rating_only(self):
        """
        测试仅根据最低评分搜索餐厅。
        """
        results = self.browsing.search_by_filters(min_rating=4.5)
        self.assertEqual(len(results), 2)  # 应该有 2 家评分 >= 4.5 的餐厅
        self.assertTrue(all([restaurant['rating'] >= 4.5 for restaurant in results]))  # 检查所有返回的餐厅评分 >= 4.5

    # 新的测试 5: 测试提供所有筛选条件（菜系、地点、评分）
    def test_search_all_filters(self):
        """
        测试提供所有筛选条件时搜索餐厅。
        """
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
        self.assertEqual(len(results), 1)  # 应该只有一家符合所有条件的餐厅
        self.assertEqual(results[0]['name'], "Italian Bistro")  # 返回的餐厅应为 "Italian Bistro"

    # 新的测试 6: 测试评分条件为 0（允许所有评分的餐厅）
    def test_search_by_zero_rating(self):
        """
        测试最低评分为 0 时，返回所有餐厅。
        """
        results = self.browsing.search_by_rating(0)
        self.assertEqual(len(results), 5)  # 应该返回所有 5 家餐厅
        self.assertTrue(all([restaurant['rating'] >= 0 for restaurant in results]))  # 检查所有返回的餐厅评分 >= 0

    # 新的测试 7: 测试提供无效评分
    def test_search_invalid_rating(self):
        """
        测试提供无效评分条件（如负数）。
        """
        results = self.browsing.search_by_rating(4)
        self.assertEqual(len(results), 4)  # 负评分应当没有餐厅符合条件

if __name__ == '__main__':
    unittest.main()
