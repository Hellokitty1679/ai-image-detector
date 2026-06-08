@echo off
chcp 65001 >nul
title 上传代码到 GitHub

echo ========================================
echo   上传代码到 GitHub
echo ========================================
echo.

echo [1/6] 检查 Git 是否安装...
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未安装 Git
    echo.
    echo 请先安装 Git:
    echo   下载地址: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo [OK] Git 已安装
echo.

echo [2/6] 初始化 Git 仓库...
if not exist ".git" (
    git init
    echo [OK] Git 仓库初始化完成
) else (
    echo [OK] Git 仓库已存在
)
echo.

echo [3/6] 创建 .gitignore 文件...
if not exist ".gitignore" (
    echo # Python > .gitignore
    echo __pycache__/ >> .gitignore
    echo *.py[cod] >> .gitignore
    echo. >> .gitignore
    echo # Virtual environments >> .gitignore
    echo venv/ >> .gitignore
    echo. >> .gitignore
    echo # Output >> .gitignore
    echo output/ >> .gitignore
    echo. >> .gitignore
    echo # Models >> .gitignore
    echo *.pth >> .gitignore
    echo. >> .gitignore
    echo # IDE >> .gitignore
    echo .idea/ >> .gitignore
    echo .vscode/ >> .gitignore
    echo [OK] .gitignore 创建完成
) else (
    echo [OK] .gitignore 已存在
)
echo.

echo [4/6] 添加所有文件...
git add .
echo [OK] 文件已添加到暂存区
echo.

echo [5/6] 提交代码...
git commit -m "Initial commit: AI图像检测系统 - 基于像素级映射技术" 2>nul
if errorlevel 1 (
    echo [提示] 没有新的修改需要提交
) else (
    echo [OK] 代码提交完成
)
echo.

echo [6/6] 推送到 GitHub...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo ========================================
    echo   请先在 GitHub 创建仓库
    echo ========================================
    echo.
    echo 步骤:
    echo 1. 访问: https://github.com/new
    echo 2. 仓库名: ai-image-detector
    echo 3. 不要勾选 "Add a README file"
    echo 4. 点击 "Create repository"
    echo.
    echo 创建完成后，请输入您的 GitHub 用户名:
    set /p username=用户名: 
    echo.
    echo 添加远程仓库...
    git remote add origin https://github.com/%username%/ai-image-detector.git
)

echo.
echo 正在推送到 GitHub...
echo.

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo [错误] 推送失败
    echo.
    echo 可能的原因:
    echo 1. 远程仓库名称不正确
    echo 2. 需要先登录 GitHub
    echo 3. 网络问题
    echo.
    echo 请检查后重试，或手动运行:
    echo   git push -u origin main
    echo.
) else (
    echo.
    echo ========================================
    echo   ✅ 代码上传成功！
    echo ========================================
    echo.
    echo 访问地址: https://github.com/您的用户名/ai-image-detector
    echo.
)

pause
