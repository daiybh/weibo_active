
import logging
import builtins
logging.basicConfig(filename="weiBoActive.log",
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
def print_to_log(*args, **kwargs):
    """将 print 重定向到 logging.info"""
    message = ' '.join(str(arg) for arg in args)
    logging.info(message)

# 替换 print
builtins.print = print_to_log

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