import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

from UserRegistration import UserRegistration
from OrderPlacement import Cart, OrderPlacement, UserProfile, RestaurantMenu, PaymentMethod
from PaymentProcessing import PaymentProcessing
from RestaurantBrowsing import RestaurantDatabase, RestaurantBrowsing

# 用户数据存储的工具函数
USERS_FILE = "users.json"

def load_users():
    # 从文件加载用户数据
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    # 将用户数据保存到文件
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mobile Food Delivery App")
        self.geometry("600x400") # 设置应用大小

        # 从文件加载用户注册数据
        self.user_data = load_users()

        # 初始化核心类
        self.registration = UserRegistration()
        self.registration.users = self.user_data  # 将现有用户加载到注册系统中

        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

        # 最初没有用户登录
        self.logged_in_email = None

        # 创建初始框架
        self.current_frame = None
        self.show_startup_frame()

    def show_startup_frame(self):
        # 显示启动框架
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = StartupFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register_frame(self):
        # 显示注册框架
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegisterFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        # 显示登录框架
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def login_user(self, email):
        # 用户登录
        self.logged_in_email = email
        # After login, show main app frame
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainAppFrame(self, email)
        self.current_frame.pack(fill="both", expand=True)

# 以下是各个框架的类定义，每个框架对应应用的不同页面
class StartupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Welcome to the Mobile Food Delivery App", font=("Arial", 16)).pack(pady=30)

        tk.Button(self, text="Register", command=self.go_to_register, width=20).pack(pady=10)
        tk.Button(self, text="Login", command=self.go_to_login, width=20).pack(pady=10)

    def go_to_register(self):
        self.master.show_register_frame()

    def go_to_login(self):
        self.master.show_login_frame()


class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Register New User", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")
        self.conf_pass_entry = self.create_entry("Confirm Password:", show="*")

        tk.Button(self, text="Register", command=self.register_user).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()
    # 创建输入框的通用函数
    def create_entry(self, label_text, show=None):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry
    # 注册用户
    def register_user(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        confirm_password = self.conf_pass_entry.get()

        result = self.master.registration.register(email, password, confirm_password)
        if result["success"]:
            # 保存更新后的用户数据到文件
            save_users(self.master.registration.users)
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.show_login_frame()
        else:
            messagebox.showerror("Error", result["error"])

    def go_back(self):
        self.master.show_startup_frame()


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="User Login", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()

    def create_entry(self, label_text, show=None):
        # 创建输入框的通用函数
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry

    def login(self):
        # 用户登录验证
        email = self.email_entry.get()
        password = self.pass_entry.get()
        # 验证登录
        users = self.master.registration.users
        if email in users and users[email]["password"] == password:
            self.master.login_user(email)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def go_back(self):
        self.master.show_startup_frame()


class MainAppFrame(tk.Frame):
    def __init__(self, master, user_email):
        super().__init__(master)
        tk.Label(self, text=f"Welcome, {user_email}", font=("Arial", 14)).pack(pady=10)

        self.user_email = user_email
        self.database = master.database
        self.browsing = master.browsing

        # 创建用户档案和购物车
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

        # 搜索框架
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Cuisine:").pack(side="left")
        self.cuisine_var = tk.Entry(search_frame)
        self.cuisine_var.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_restaurants).pack(side="left")

        # 结果树状视图
        self.results_tree = ttk.Treeview(self, columns=("cuisine", "location", "rating"), show="headings")
        self.results_tree.heading("cuisine", text="Cuisine")
        self.results_tree.heading("location", text="Location")
        self.results_tree.heading("rating", text="Rating")
        self.results_tree.pack(pady=10, fill="x")

        # 操作按钮
        action_frame = tk.Frame(self)
        action_frame.pack(pady=5)
        tk.Button(action_frame, text="View All Restaurants", command=self.view_all_restaurants).pack(side="left", padx=5)
        tk.Button(action_frame, text="Add Item to Cart", command=self.add_item_to_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="View Cart", command=self.view_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="Checkout", command=self.checkout).pack(side="left", padx=5)

    def search_restaurants(self):
        # 搜索餐厅
        self.results_tree.delete(*self.results_tree.get_children())
        cuisine = self.cuisine_var.get().strip()
        results = self.browsing.search_by_filters(cuisine_type=cuisine if cuisine else None)
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def view_all_restaurants(self):
        # 查看所有餐厅
        self.results_tree.delete(*self.results_tree.get_children())
        results = self.database.get_restaurants()
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def add_item_to_cart(self):
        # 添加商品到购物车
        # 一个更复杂的方法：让用户从菜单项中选择,我们将显示一个小的弹出窗口来选择项目。
        menu_popup = AddItemPopup(self, self.restaurant_menu, self.cart)
        self.wait_window(menu_popup)

    def view_cart(self):
        cart_view = CartViewPopup(self, self.cart)
        self.wait_window(cart_view)

    def checkout(self):
        # 验证订单，如果有则继续
        validation = self.order_placement.validate_order()
        if not validation["success"]:
            messagebox.showerror("Error", validation["message"])
            return

        # 显示结帐弹出
        checkout_popup = CheckoutPopup(self, self.order_placement)
        self.wait_window(checkout_popup)


class AddItemPopup(tk.Toplevel):
    # 弹出窗口，用于将商品添加到购物车
    def __init__(self, master, menu, cart):
        super().__init__(master) # 调用父类构造函数
        self.title("Add Item to Cart")
        self.menu = menu
        self.cart = cart

        tk.Label(self, text="Select an item to add to cart:").pack(pady=10) # 提示标签
        # 创建一个下拉菜单，用于选择要添加的商品
        self.item_var = tk.StringVar()
        self.item_var.set(self.menu.available_items[0] if self.menu.available_items else "")
        tk.OptionMenu(self, self.item_var, *self.menu.available_items).pack(pady=5)

        tk.Label(self, text="Quantity:").pack()
        self.qty_entry = tk.Entry(self)
        self.qty_entry.insert(0, "1")# 默认数量为1
        self.qty_entry.pack(pady=5)
        # 添加到购物车的按钮
        tk.Button(self, text="Add to Cart", command=self.add_to_cart).pack(pady=10)

    def add_to_cart(self):
        # 将商品添加到购物车的方法
        item = self.item_var.get() # 获取选中的商品
        qty = int(self.qty_entry.get())
        price = 10.0  # Static price for simplicity
        msg = self.cart.add_item(item, price, qty) # 将商品添加到购物车，并获取返回信息
        messagebox.showinfo("Cart", msg)
        self.destroy() # 关闭弹出窗口


class CartViewPopup(tk.Toplevel):
    # 弹出窗口，用于查看购物车中的商品
    def __init__(self, master, cart):
        super().__init__(master)
        self.title("Cart Items")

        items = cart.view_cart()
        if not items: # 如果购物车为空
            tk.Label(self, text="Your cart is empty").pack(pady=20)
        else:
            for i in items: # 如果购物车不为空，显示每一项商品
                tk.Label(self, text=f"{i['name']} x{i['quantity']} = ${i['subtotal']:.2f}").pack()


class CheckoutPopup(tk.Toplevel):
    # 弹出窗口，用于结账
    def __init__(self, master, order_placement):
        super().__init__(master)
        self.title("Checkout")
        self.order_placement = order_placement # 订单处理对象

        order_data = order_placement.proceed_to_checkout()
        tk.Label(self, text="Review your order:", font=("Arial", 12)).pack(pady=10)
        # 订单回顾提示
        # 显示订单中的商品
        for item in order_data["items"]:
            tk.Label(self, text=f"{item['name']} x{item['quantity']} = ${item['subtotal']:.2f}").pack()

        total = order_data["total_info"]
        tk.Label(self, text=f"Subtotal: ${total['subtotal']:.2f}").pack()
        tk.Label(self, text=f"Tax: ${total['tax']:.2f}").pack()
        tk.Label(self, text=f"Delivery Fee: ${total['delivery_fee']:.2f}").pack()
        tk.Label(self, text=f"Total: ${total['total']:.2f}").pack()
        # 显示总计
        tk.Label(self, text=f"Delivery Address: {order_data['delivery_address']}").pack(pady=5)
        # 显示送货地址
        # 选择支付方式
        tk.Label(self, text="Payment Method:").pack(pady=5)
        self.payment_method = tk.StringVar()
        self.payment_method.set("credit_card")
        tk.Radiobutton(self, text="Credit Card", variable=self.payment_method, value="credit_card").pack()
        tk.Radiobutton(self, text="Paypal", variable=self.payment_method, value="paypal").pack()

        tk.Label(self, text="For credit card enter a 16-digit card number:").pack(pady=5)
        self.card_entry = tk.Entry(self)
        self.card_entry.insert(0, "1234567812345678")
        self.card_entry.pack(pady=5)

        tk.Button(self, text="Confirm Order", command=self.confirm_order).pack(pady=10)

    # 确认订单的方法
    def confirm_order(self):
        # 使用给定的付款方式处理订单确认
        payment_method_obj = PaymentMethod()  # 模拟付款方式处理在旧的代码，有PaymentProcessing类。只使用PaymentMethod。
        # 如果想使用PaymentProcessing，也可以通过集成它来实现，通过检查是否总> 0来处理付款，以类似的方式集成PaymentProcessing。

        # 确认订单
        result = self.order_placement.confirm_order(payment_method_obj)
        if result["success"]:
            messagebox.showinfo("Order Confirmed", f"Order ID: {result['order_id']}\nEstimated Delivery: {result['estimated_delivery']}")
            self.destroy()
        else:
            messagebox.showerror("Error", result["message"])


if __name__ == "__main__":
    app = Application() # 创建应用实例
    app.mainloop() # 启动应用
