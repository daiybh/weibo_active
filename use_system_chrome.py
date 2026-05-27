#!/usr/bin/env python3
"""使用系统原有Chrome数据，无需重新登录"""
import time, sys, os

def get_chrome_cookies():
    print("使用系统原有Chrome数据获取Cookie...")

    # 安装依赖
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
    except:
        os.system(f'{sys.executable} -m pip install selenium webdriver-manager -q')
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

    print("打开Chrome（使用系统原有数据）...")

    options = Options()
    # 指定使用系统原有的Chrome用户数据目录
    user_data_dir = r"C:\Users\Daili\AppData\Local\Google\Chrome\User Data"
    user_data_dir= r"C:\my-profile"
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--profile-directory=Default')

    # 可选：不显示自动化提示
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print("正在访问weibo.com...")
    driver.get("https://weibo.com")

    # 等待页面加载（如果你的Chrome已登录，应该会自动登录）
    print("等待页面加载...")
    time.sleep(50)

    # 检查是否已登录（通过检测登录元素或URL变化）
    print(f"当前URL: {driver.current_url}")
    print(f"页面标题: {driver.title}")

    if 'login' in driver.current_url.lower():
        print("\n检测到未登录，请在浏览器中完成登录...")
        print("登录后，脚本会在10秒后自动获取cookies\n")
        for i in range(10, 0, -1):
            print(f"\r{i}秒后自动获取...", end="", flush=True)
            time.sleep(1)
        print()
    else:
        print("✓ 已检测到登录状态")

    # 获取cookies
    cookies = driver.get_cookies()
    print(f"\n获取到 {len(cookies)} 个cookies")
    cookie_str=""
    if cookies:
        cookie_str = '; '.join([f'{c["name"]}={c["value"]}' for c in cookies])
        import dotenv
        dotenv.set_key(".env", "WEIBO_COOKIE", cookie_str)
        print(f"\n✓ 成功获取 {len(cookies)} 个cookies")
        print("✓ 已保存到 .env 文件")
        print(f"\nCookie列表:")
        for c in cookies:
            print(f"  - {c['name']}")
        
    else:
        print("\n✗ 未获取到cookies")

    print("\n3秒后关闭浏览器...")
    time.sleep(3)
    driver.quit()
    print("完成！")
    return cookie_str


if __name__ == "__main__":
    get_chrome_cookies()