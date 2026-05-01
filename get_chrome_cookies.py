#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Chrome Cookie 数据库读取并正确解密 weibo.com 的 cookies
"""

import os
import sqlite3
import shutil
import tempfile

def get_chrome_cookies():
    """读取并解密 Chrome cookies"""
    print("正在从 Chrome 读取 cookies...")
    
    cookie_path = r"C:\Users\Daili\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"
    
    if not os.path.exists(cookie_path):
        print(f"未找到 Cookie 文件")
        return None
    
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'chrome_cookies_temp.db')
    
    try:
        shutil.copy2(cookie_path, temp_path)
    except Exception as e:
        print(f"复制失败: {e}")
        return None
    
    try:
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        
        # Chrome 新版本：加密的值在 encrypted_value 字段
        cursor.execute("""
            SELECT name, value, encrypted_value, host_key
            FROM cookies
            WHERE host_key LIKE '%weibo.com%' OR host_key LIKE '%sina.com.cn%'
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if not rows:
            print("未找到 weibo 相关 cookies")
            return None
        
        cookies = []
        for name, value, encrypted_value, host in rows:
            cookie_value = None
            
            # 先尝试解密
            if encrypted_value:
                try:
                    import win32crypt
                    # DPAPI 解密
                    decrypted = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)
                    if decrypted and decrypted[1]:
                        cookie_value = decrypted[1].decode('utf-8', errors='ignore')
                except Exception as e:
                    pass
            
            # 如果解密失败，尝试使用明文 value
            if not cookie_value and value:
                try:
                    cookie_value = value.decode('utf-8', errors='ignore') if isinstance(value, bytes) else str(value)
                except:
                    pass
            
            if cookie_value:
                cookies.append(f"{name}={cookie_value}")
                print(f"  成功: {name}")
        
        if not cookies:
            print("无法获取有效的 cookie 值")
            return None
        
        cookie_str = '; '.join(cookies)
        print(f"\n成功获取 {len(cookies)} 个有效 cookies")
        return cookie_str
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def write_to_env(cookie_str):
    """将 cookies 写入 .env 文件"""
    env_path = r'C:\Users\Daili\Desktop\webActive\.env'
    
    # 确保是文本格式
    lines = []
    if os.path.exists(env_path) and os.path.getsize(env_path) < 100000:  # 不是二进制文件
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            lines = []
    
    new_lines = []
    cookie_written = False
    
    for line in lines:
        if line.startswith('WEIBO_COOKIE='):
            new_lines.append(f'WEIBO_COOKIE={cookie_str}\n')
            cookie_written = True
        else:
            new_lines.append(line)
    
    if not cookie_written:
        new_lines.append(f'WEIBO_COOKIE={cookie_str}\n')
    
    # 写入文本文件
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n已将 cookies 写入 {env_path}")

if __name__ == '__main__':
    print("微博 Cookie 获取工具（支持解密）")
    print("="*50)
    
    # 检查依赖
    try:
        import win32crypt
    except ImportError:
        print("正在安装 pywin32...")
        import subprocess
        subprocess.check_call(["pip", "install", "pywin32"])
        print("请重新运行脚本")
        exit(1)
    
    cookie_str = get_chrome_cookies()
    
    if cookie_str:
        write_to_env(cookie_str)
        print("\n完成！现在可以运行 main.py 测试了")
    else:
        print("\n获取失败")
        print("提示：请尝试以管理员身份运行此脚本")
