

import use_system_chrome
r= use_system_chrome.get_chrome_cookies()
print(f"获取到的cookie: {r}")

if r!="":
    import weibo
    import dotenv
    dotenv.load_dotenv()
    import qinglong
    qinglong.update_env(r)
    weibo.main()