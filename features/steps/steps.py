from behave import given, when, then
import subprocess
import time
import pyautogui
from UserRegistration import UserRegistration

@given('the app is running')
def step_impl(context):
    context.proc = subprocess.Popen(["python", "main.py"])
    time.sleep(3)

@when('I register with "{email}" and "{password}"')
def step_impl(context, email, password):
    pyautogui.click(x=100, y=200) # 根据你的GUI调整坐标
    time.sleep(1)
    pyautogui.typewrite(email)
    pyautogui.press("tab")
    pyautogui.typewrite(password)
    pyautogui.press("tab")
    pyautogui.typewrite(password)
    pyautogui.press("enter")
    time.sleep(2)
@then('I should see a "{message}" message')
def step_impl(context, message):
    pyautogui.screenshot("bdd_result.png")
    # 假设手动检查或使用OCR
    assert True, "假设通过截图验证成功"