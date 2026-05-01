@echo off
chcp 65001 >nul
title 微博Cookie获取工具

REM 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_script
) else (
    goto :request_admin
)

:request_admin
echo 正在请求管理员权限...
powershell -Command "Start-Process cmd -ArgumentList '/c cd /d ""%cd%"" && python get_chrome_cookies.py' -Verb RunAs"
exit /b

:run_script
cd /d "%~dp0"
echo 正在运行微博Cookie获取工具...
python get_chrome_cookies.py
pause
