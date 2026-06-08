import os
import urllib.request
import zipfile
import io

print("="*60)
print("  下载并安装 ngrok 到 D 盘")
print("="*60)

download_dir = r"D:\ngrok"
os.makedirs(download_dir, exist_ok=True)

download_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
zip_path = os.path.join(download_dir, "ngrok.zip")
exe_path = os.path.join(download_dir, "ngrok.exe")

if os.path.exists(exe_path):
    print(f"\n✅ ngrok 已经存在: {exe_path}")
else:
    print(f"\n📥 正在下载 ngrok...")
    print(f"   目标目录: {download_dir}")
    
    try:
        with urllib.request.urlopen(download_url, timeout=60) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            block_size = 8192
            
            with open(zip_path, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    f.write(buffer)
                    downloaded += len(buffer)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"   下载进度: {percent:.1f}%", end='\r')
        
        print(f"\n✅ 下载完成: {zip_path}")
        
        print(f"\n📦 正在解压...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
        
        print(f"✅ 解压完成: {exe_path}")
        
        os.remove(zip_path)
        print(f"🗑️  删除临时文件: {zip_path}")
        
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        print("\n请手动下载:")
        print(f"   下载地址: {download_url}")
        print(f"   解压到: {download_dir}")
        exit(1)

print("\n" + "="*60)
print("  ngrok 安装完成！")
print("="*60)
print(f"\n📂 安装路径: {download_dir}")
print(f"🚀 可执行文件: {exe_path}")
print("\n使用方法:")
print("  1. 打开命令行，运行:")
print(f"     {exe_path} http 5000")
print("")
print("  2. 或者进入目录后运行:")
print(f"     cd {download_dir}")
print(f"     ngrok http 5000")
print("")
print("  3. 复制生成的 HTTPS 链接分享给朋友！")
print("\n" + "="*60)

print("\n是否要我帮您创建一个快捷启动脚本？(y/n)")
