# AI生成图像检测 - Web前端

基于论文 "Beyond Semantic Features: Pixel-level Mapping for Generalized AI-Generated Image Detection" (arXiv: 2512.17350) 的Web应用。

## 🎯 功能特性

- **拖拽上传**: 支持拖拽或点击上传图片
- **实时分析**: 快速检测图像是否为AI生成
- **可视化结果**: 显示真实/AI生成的概率和置信度
- **响应式设计**: 支持桌面和移动设备
- **隐私保护**: 本地处理，不上传图像数据

## 🚀 快速开始

### 方式1: 直接启动（Windows）

```bash
# 双击运行
start_web.bat
```

### 方式2: 命令行启动

```bash
# 基本启动
python app.py

# 指定模型路径启动
python app.py --checkpoint ./output/best_model.pth

# 使用随机映射
python app.py --checkpoint ./output/best_model.pth --mapping_type random

# 指定端口
python app.py --checkpoint ./output/best_model.pth --port 8080
```

### 方式3: 完整命令行参数

```bash
python app.py \
  --checkpoint ./output_fixed/best_model.pth \
  --mapping_type fixed \
  --backbone resnet50 \
  --host 0.0.0.0 \
  --port 5000
```

## 📋 启动前准备

### 1. 安装依赖

```bash
pip install -r requirements_web.txt
```

或完整安装：

```bash
pip install torch torchvision numpy Pillow Flask werkzeug
```

### 2. 训练模型（如无预训练模型）

```bash
# 准备数据（放入data/目录）
# 然后运行训练
python train.py ^
  --train_real_dir ./data/train/real ^
  --train_fake_dir ./data/train/fake ^
  --test_real_dir ./data/test/real ^
  --test_fake_dir ./data/test/fake ^
  --mapping_type fixed ^
  --epochs 200 ^
  --batch_size 32
```

### 3. 启动Web应用

```bash
# 启动应用
python app.py --checkpoint ./output/best_model.pth

# 浏览器访问
http://localhost:5000
```

## 🖼️ 使用说明

1. **上传图片**: 点击上传区域或拖拽图片到上传区
2. **等待分析**: 系统会自动分析图像
3. **查看结果**:
   - 🚨 AI生成图像（红色显示）
   - ✅ 真实图像（绿色显示）
   - 概率柱状图和置信度显示

## 🔧 配置说明

### 支持的图片格式

- JPG/JPEG
- PNG
- BMP
- TIFF

### 文件大小限制

- 最大: 16MB

### 可用的映射类型

| 类型 | 说明 | 推荐 |
|------|------|------|
| `fixed` | 固定像素级映射 | ⭐ 推荐 |
| `random` | 随机像素级映射 | 性能相当 |
| `none` | 无映射（基线） | 用于对比 |

## 🌐 API接口

### POST /detect

分析上传的图像。

**请求**:
```
Content-Type: multipart/form-data
Body: image (file)
```

**响应**:
```json
{
  "prediction": "AI-Generated",
  "real_probability": 23.45,
  "fake_probability": 76.55,
  "confidence": 76.55,
  "is_fake": true,
  "image_base64": "..."
}
```

### POST /api/detect

JSON格式的API接口。

**响应**:
```json
{
  "success": true,
  "result": {
    "prediction": "AI-Generated",
    "real_probability": 23.45,
    "fake_probability": 76.55,
    "confidence": 76.55,
    "is_fake": true
  }
}
```

## 📁 项目结构

```
patch_shufffle/
├── app.py                  # Flask应用主文件
├── detector.py             # 检测器模型
├── pixel_mapping.py        # 像素级映射模块
├── datasets.py             # 数据集处理
├── train.py                # 训练脚本
├── test.py                 # 测试脚本
├── start_web.bat           # Windows启动脚本
├── requirements_web.txt    # Web应用依赖
├── requirements.txt        # 完整依赖
├── templates/
│   └── index.html          # 前端页面
├── data/                   # 数据集目录
│   ├── train/
│   │   ├── real/           # 真实训练图像
│   │   └── fake/           # AI生成训练图像
│   └── test/
│       ├── real/           # 真实测试图像
│       └── fake/           # AI生成测试图像
└── output/                 # 模型输出目录
```

## 🎓 技术原理

本应用基于论文提出的**像素级映射**技术：

### 核心思想

- 破坏图像的语义线索
- 将低频信息转换为高频
- 保留像素间的相关性
- 迫使模型关注生成过程中的高频痕迹

### 映射公式

**固定映射**:
```
φ_f(v) = v - round(v/256, 2) * 256
```

**随机映射**:
```
T_c ~ Uniform(-1, 1)^256  (每个通道独立)
```

## 📊 检测能力

- ✅ GAN生成图像（StyleGAN, ProGAN, BigGAN等）
- ✅ 扩散模型图像（Stable Diffusion, MidJourney等）
- ⚡ 实时处理
- 🔒 本地隐私保护

## 🛠️ 故障排除

### 问题1: "Model not loaded"

**原因**: 未找到预训练模型
**解决**: 
```bash
# 方法1: 先训练模型
python train.py ...

# 方法2: 指定正确的模型路径
python app.py --checkpoint /path/to/your/model.pth
```

### 问题2: 导入错误

**原因**: 缺少依赖
**解决**:
```bash
pip install -r requirements_web.txt
```

### 问题3: 端口被占用

**原因**: 5000端口已被使用
**解决**:
```bash
python app.py --port 5001
```

## 📝 开发说明

### 后端技术栈

- Python 3.8+
- Flask 2.0+
- PyTorch 1.10+
- Pillow (图像处理)

### 前端技术栈

- 原生HTML/CSS/JavaScript
- 响应式设计
- 无外部框架依赖

## 🎨 自定义

### 修改样式

编辑 `templates/index.html` 中的 `<style>` 部分。

### 修改配置

在 `app.py` 中修改：

```python
# 文件大小限制（16MB）
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 支持的格式
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
```

## 📚 参考文献

- 论文: https://arxiv.org/abs/2512.17350
- 会议: AAAI 2026

## 📄 License

学术研究用途。

---

🎉 享受使用AI生成图像检测系统！
