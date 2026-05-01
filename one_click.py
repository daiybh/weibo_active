#!/usr/bin/env python3
"""一键获取微博Cookie - 不需要预先登录"""
import time, sys, os

print("全自动获取微博Cookie")
print("=" * 50)

# 安装依赖
print("检查依赖...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except:
    print("安装selenium...")
    os.system(f'{sys.executable} -m pip install selenium webdriver-manager -q')
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

print("\n正在打开Chrome...")
print("请在浏览器中登录微博")
print("登录后，脚本会在10秒后自动获取cookies\n")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://weibo.com")

# 等待登录
for i in range(10, 0, -1):
    print(f"\r{ i }秒后自动获取cookies...", end="", flush=True)
    time.sleep(1)
print("\n\n正在获取cookies...")

cookies = driver.get_cookies()

if cookies:
    cookie_str = '; '.join([f'{c["name"]}={c["value"]}' for c in cookies])
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(f'WEIBO_COOKIE="{cookie_str}"\n')
    print(f"\n✓ 成功获取 {len(cookies)} 个cookies")
    print("✓ 已保存到 .env 文件")
    print(f"\nCookie列表: {[c['name'] for c in cookies]}")
else:
    print("\n✗ 未获取到cookies")

print("\n3秒后关闭浏览器...")
time.sleep(3)
driver.quit()
print("完成！")
