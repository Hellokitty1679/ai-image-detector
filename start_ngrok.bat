@echo off
chcp 65001 >nul
title ngrok - AI生成图像检测公网链接

echo ========================================
echo   启动 ngrok 公网隧道
echo ========================================
echo.
echo [信息] 正在连接 ngrok 服务器...
echo [信息] 请等待几秒钟...
echo.
echo ========================================
echo   使用说明:
echo   1. 复制 "Forwarding" 后面的 HTTPS 链接
echo   2. 分享给您的朋友
echo   3. 保持此窗口打开
echo ========================================
echo.

D:\ngrok\ngrok.exe http 5000

pause
