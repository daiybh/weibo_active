"""使用独立Chrome配置文件获取Cookie - 使用CDP协议"""
import time, sys, os
import subprocess
import json

def get_chrome_cookies():
    print("使用独立Chrome配置文件获取Cookie...")

    # 安装依赖
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
    except:
        os.system(f'{sys.executable} -m pip install selenium -q')
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

    # 配置
    debug_port = 9222
    user_data_dir = r"C:\my-profile"
    
    # 查找Chrome路径
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
    ]
    
    chrome_path = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_path = path
            break
    
    if not chrome_path:
        print("❌ 未找到Chrome浏览器")
        return ""
    
    print(f"Chrome路径: {chrome_path}")
    print(f"用户数据目录: {user_data_dir}")
    
    # 创建用户数据目录（如果不存在）
    if not os.path.exists(user_data_dir):
        print(f"创建用户数据目录: {user_data_dir}")
        os.makedirs(user_data_dir, exist_ok=True)
    
    # 关闭占用调试端口的进程
    print("检查调试端口...")
    os.system(f'netstat -ano | findstr :{debug_port} >nul 2>&1')
    
    # 启动带远程调试的Chrome（使用独立用户目录）
    print(f"\n启动Chrome（调试端口: {debug_port}）...")
    cmd = f'"{chrome_path}" --remote-debugging-port={debug_port} --user-data-dir="{user_data_dir}" --no-first-run --no-default-browser-check'
    print(f"命令: {cmd}\n")
    
    subprocess.Popen(cmd, shell=True)
    
    print("等待Chrome启动...")
    time.sleep(5)
    
    # 连接到Chrome
    try:
        options = Options()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
        
        driver = webdriver.Chrome(options=options)
        print("✓ 成功连接到Chrome！")
        
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        print("\n💡 请检查：")
        print(f"1. Chrome是否已成功启动")
        print(f"2. 是否有其他程序占用了端口 {debug_port}")
        print(f"3. 尝试手动运行: {cmd}")
        return ""

    print("\n正在访问weibo.com...")
    driver.get("https://weibo.com")

    # 等待页面加载
    print("等待页面加载...")
    time.sleep(3)
    
    # 缓慢滚动页面10秒钟
    print("开始缓慢滚动页面（10秒）...")
    scroll_duration = 10  # 滚动总时长（秒）
    scroll_steps = 100    # 滚动步数
    step_delay = scroll_duration / scroll_steps  # 每步延迟
    scroll_distance = 50  # 每步滚动距离（像素）
    
    for i in range(scroll_steps):
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(step_delay)
        
        # 每2秒显示一次进度
        if (i + 1) % int(scroll_steps / 5) == 0:
            progress = int((i + 1) / scroll_steps * 100)
            print(f"   滚动进度: {progress}%")
    
    print("✓ 页面滚动完成")
    
    # 检查是否已登录
    current_url = driver.current_url
    print(f"\n当前URL: {current_url}")
    print(f"页面标题: {driver.title}")

    if 'login' in current_url.lower():
        print("\n⚠️ 检测到仍未登录")
        print("请手动在浏览器中完成登录，然后按回车键继续...")
        input()
        
        # 重新加载微博页面
        driver.get("https://weibo.com")
        time.sleep(3)
    else:
        print("✓ 已检测到登录状态")

    # 获取cookies
    print("\n正在获取Cookies...")
    cookies = driver.get_cookies()
    print(f"获取到 {len(cookies)} 个cookies")
    
    cookie_str = ""
    if cookies:
        cookie_str = '; '.join([f'{c["name"]}={c["value"]}' for c in cookies])
        
        # 保存到.env文件
        try:
            import dotenv
            dotenv.set_key(".env", "WEIBO_COOKIE", cookie_str)
            print(f"\n✓ 成功获取 {len(cookies)} 个cookies")
            print("✓ 已保存到 .env 文件")
            print(f"\nCookie预览:")
            print(cookie_str[:100] + "..." if len(cookie_str) > 100 else cookie_str)
        except Exception as e:
            print(f"⚠️ 保存.env文件失败: {e}")
            print(f"\nCookie字符串:")
            print(cookie_str)
    else:
        print("\n✗ 未获取到cookies")

    print("\n5秒后关闭Chrome浏览器...")
    time.sleep(5)
    
    # 使用CDP命令优雅关闭浏览器
    try:
        print("正在通过CDP命令关闭Chrome...")
        driver.execute_cdp_cmd('Browser.close', {})
        print("✓ Chrome已通过CDP命令关闭")
    except Exception as e:
        print(f"⚠️ CDP关闭失败: {e}，尝试强制关闭...")
        # 如果CDP关闭失败，才使用强制方式
        os.system('taskkill /F /IM chrome.exe >nul 2>&1')
    
    # 断开webdriver连接
    driver.quit()
    time.sleep(1)
    
    print("✓ 完成！Chrome浏览器已关闭")
    
    return cookie_str


if __name__ == "__main__":
    result = get_chrome_cookies()
    if result:
        print(f"\n🎉 Cookie获取成功！长度: {len(result)}")
    else:
        print("\n❌ Cookie获取失败")