"""
File: ccw.py
Author: ILoveScratch2
Date Modified: 2024/12/21 13:00:00
Description: This is a script to sign in to CCW website using playwright. 这是使用Playwright登录CCW网站的脚本。
Requirements:
- Python 3.7 or higher
- playwright 1.48.0 or higher
- chromium installed
- toml installed

"""
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import toml


# Enter your CCW Account Details here
# 在这里输入您的CCW账号信息
# 如果没有输入，会从accounts.toml中读取
ACCOUNT_ID = "<YOUR_ACCOUNT_ID>"
PASSWORD = "<YOUR_PASSWORD>"

# 无头模式，默认为True，即不打开浏览器窗口
# 设置为False时，会打开浏览器窗口，可以查看每一步，仅适用于调试
# 设置为True时，不会打开浏览器窗口，可以在PC，服务器或VPS上运行，不会弹出窗口
HEADLESS = False


def run(playwright: Playwright):

    global ACCOUNT_ID, PASSWORD, HEADLESS
    if ACCOUNT_ID == "" or PASSWORD == "" or ACCOUNT_ID == "<YOUR_ACCOUNT_ID>" or PASSWORD == "<YOUR_PASSWORD>":
        # 从accounts.toml中读取账号信息
        print("No Account Details provided.")
        print("Reading Account Details from accounts.toml...")
        file = toml.load("accounts.toml")
        ACCOUNT_ID = file["ccw"]["account_id"]
        PASSWORD = file["ccw"]["password"]
        ENABLE = file["ccw"]["enabled"]
        if not ENABLE:
            print("CCW Account is disabled in accounts.toml. Exiting...")
            exit()
        print("Account Details Read.")




    browser = playwright.chromium.launch(headless=HEADLESS)
    context = browser.new_context()
    page = context.new_page()
    print("Navigating to CCW Website...")
    # 访问CCW网站
    page.goto("https://www.ccw.site/")
    print("Finding Login Button...")
    # 点击登录按钮
    page.get_by_role("button", name="登录/注册").click()
    # 因为不使用手机号登录，所以需要切换到密码登录
    # 切换到密码登录
    page.get_by_role("button", name="切换密码登录").click()
    page.locator(".input-wrapper-2C3zV").first.click()
    print("Entering Account Details...")
    # 输入账号密码
    page.get_by_placeholder("共创世界 ID").click()
    page.get_by_placeholder("共创世界 ID").fill(ACCOUNT_ID)
    page.get_by_placeholder("请输入密码").click()
    page.get_by_placeholder("请输入密码").fill(PASSWORD)
    # 点击登录按钮
    page.get_by_role("button", name="登录", exact=True).click()
    print("Logging into CCW Account...")


    # 没有实名认证的账户每次登录都会弹出窗口，需要关闭
    # 已经实名认证的账户不会弹出窗口，可以注释掉下面1行
    # 关闭弹窗
    page.get_by_role("img", name="close").click()

    # 点击金币按钮
    print("Finding Coins Button...")
    page.locator("div").filter(has_text=re.compile(r"^金币$")).first.click()
    # 点击签到按钮
    print("Finding Sign In Button...")
    page.get_by_role("button", name="立即签到").click()
    page.locator(".closeBtn-30jhg").click()
    # 退出浏览器
    page.close()
    print("Signed in Successfully!")

    context.close()
    browser.close()


if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(playwright)
