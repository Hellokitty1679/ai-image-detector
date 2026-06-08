
# 🚀 快速获取公网分享链接

## 当前状态

✅ Flask 应用正在运行: http://localhost:5000
✅ ngrok 已安装: D:\ngrok\ngrok.exe

---

## 🎯 3 步获取公网链接

### 第 1 步：打开新的命令行窗口

按 `Win + R`，输入 `cmd`，按回车。

### 第 2 步：运行 ngrok

复制并粘贴以下命令，按回车：

```
D:\ngrok\ngrok.exe http 5000
```

### 第 3 步：复制链接

在 ngrok 窗口中，找到类似这样的行：

```
Forwarding  https://abc123-def456.ngrok-free.app -> http://localhost:5000
```

**复制 `https://` 开头的链接**，发送给您的朋友！

---

## 📋 预期的 ngrok 界面

```
ngrok by @inconshreveable

Session Status                online
Account                       (Plan: Free)
Version                       3.0.0
Region                        United States (us)
Latency                       50ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://a1b2-c3d4-e5f6.ngrok-free.app -> http://localhost:5000
Forwarding                    http://a1b2-c3d4-e5f6.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**您需要的是**: `https://a1b2-c3d4-e5f6.ngrok-free.app`

---

## 📱 分享给朋友

发送链接给朋友，他们就可以在浏览器中打开并测试了！

示例消息：
```
🎉 我做了一个 AI 图像检测工具！
快来试试：https://你的链接.ngrok-free.app

上传图片，看看是不是 AI 生成的！
（注：这是演示版本，使用随机预测）
```

---

## ⚠️ 注意事项

1. **保持窗口打开**:
   - ❌ 不要关闭 Flask 应用窗口
   - ❌ 不要关闭 ngrok 窗口

2. **免费版限制**:
   - ⏰ 链接 7 小时后过期
   - 🔄 每次启动 ngrok 会生成新链接
   - 📊 每月 1GB 流量

3. **演示模式**:
   - 🎲 当前使用随机预测
   - 🎯 要获得真实检测，需要先训练模型

---

## 🔧 故障排除

### 如果 ngrok 显示错误：

**错误1: "connection refused"**
- 解决方案: 确保 Flask 应用还在运行（http://localhost:5000 应该能访问）

**错误2: "authentication failed"**
- 解决方案: 需要注册 ngrok 账号并配置 authtoken

**错误3: 链接打不开**
- 解决方案: 检查两个窗口是否都打开着

---

## 📞 需要帮助？

如果遇到问题，告诉我具体的错误信息，我来帮您解决！
