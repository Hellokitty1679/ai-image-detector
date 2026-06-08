@echo off
chcp 65001 >nul
echo ========================================
echo   AI生成图像检测 Web应用启动脚本
echo ========================================
echo.

echo [1/3] 检查目录结构...
if not exist "templates" mkdir templates
if not exist "static" mkdir static
echo.

echo [2/3] 检查是否有已训练的模型...
if exist "output_fixed\best_model.pth" (
    echo 找到模型: output_fixed\best_model.pth
    echo 启动时将自动加载该模型
    set CHECKPOINT=--checkpoint output_fixed\best_model.pth
) else if exist "output\best_model.pth" (
    echo 找到模型: output\best_model.pth
    echo 启动时将自动加载该模型
    set CHECKPOINT=--checkpoint output\best_model.pth
) else (
    echo 未找到已训练的模型
    echo 将在演示模式下运行（需要先训练模型）
    set CHECKPOINT=
)
echo.

echo [3/3] 启动 Web 服务器...
echo 访问地址: http://localhost:5000
echo.
echo 提示:
echo   - 如需使用固定映射: --mapping_type fixed ^(默认^)
echo   - 如需使用随机映射: --mapping_type random
echo   - 如需使用基线模型: --mapping_type none
echo   - 如需指定模型路径: --checkpoint path\to\model.pth
echo.
echo ========================================
echo.

python app.py %CHECKPOINT% --mapping_type fixed --port 5000

pause
