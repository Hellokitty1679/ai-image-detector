import subprocess
import time
import sys
import os

print("="*70)
print("  🚀 启动 ngrok 公网隧道")
print("="*70)
print("")
print("[1/4] 检查 Flask 应用状态...")
print("      本地地址: http://localhost:5000")
print("")

ngrok_path = r"D:\ngrok\ngrok.exe"

if not os.path.exists(ngrok_path):
    print(f"❌ 错误: 找不到 ngrok.exe")
    print(f"   路径: {ngrok_path}")
    sys.exit(1)

print("[2/4] ngrok 路径确认: OK")
print(f"      路径: {ngrok_path}")
print("")

print("[3/4] 启动 ngrok 隧道...")
print("      正在连接 ngrok 服务器...")
print("")

try:
    process = subprocess.Popen(
        [ngrok_path, "http", "5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    print("[4/4] ngrok 已启动！")
    print("")
    print("="*70)
    print("  ✅ 公网隧道创建成功！")
    print("="*70)
    print("")
    print("📋 操作步骤:")
    print("")
    print("1️⃣  在新打开的 ngrok 窗口中，找到 'Forwarding' 行")
    print("2️⃣  复制 https:// 开头的链接")
    print("3️⃣  分享给您的朋友！")
    print("")
    print("🔗 链接格式示例:")
    print("   https://a1b2-c3d4-e5f6.ngrok-free.app")
    print("")
    print("⚠️  注意:")
    print("   - 不要关闭 Flask 应用窗口")
    print("   - 不要关闭 ngrok 窗口")
    print("   - 免费版链接 7 小时后会过期")
    print("   - 这是演示模式，使用随机预测")
    print("")
    print("="*70)
    print("")
    print("按 Ctrl+C 可停止此脚本（不影响 ngrok 和 Flask）")
    print("")
    
    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n用户中断，脚本退出。")
            print("ngrok 和 Flask 应用仍在运行中。")
            break
            
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("")
    print("请手动运行:")
    print(f"   {ngrok_path} http 5000")
