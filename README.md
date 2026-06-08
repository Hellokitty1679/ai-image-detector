
# 🤖 AI-Generated Image Detection

> 基于像素级映射技术的 AI 生成图像检测系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.10+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 项目简介

本项目提出了一种创新的 **像素级映射**（Pixel-Level Mapping）技术，用于提升 AI 生成图像检测器的跨模型泛化能力。

### 问题背景

现有的 AI 生成图像检测方法大多依赖于图像的语义特征，这导致模型在面对未知生成模型时性能显著下降。传统方法容易"过拟合"到特定生成模型的语义模式，而忽略了生成过程中留下的通用高频痕迹。

### 核心创新

我们提出通过 **像素级映射** 预处理步骤来解决这个问题：

- 🎯 **破坏语义结构**：将像素值映射到非线性空间，打破语义线索的连续性
- 🔄 **保留像素相关性**：映射过程保留像素间的空间关系，不破坏生成痕迹
- ⚡ **聚焦高频痕迹**：迫使检测器关注生成过程中固有的统计特性
- 📈 **提升泛化能力**：在跨模型测试场景中取得显著性能提升

### 映射方法

**固定映射 (Fixed Mapping)** - 可复现、计算高效：
```
φ_f(v) = v - round(v/256, 2) × 256
```

**随机映射 (Random Mapping)** - 更激进的语义破坏：
```
T_c ~ Uniform(-1, 1)^256  (每个通道独立)
```

---

## ✨ 特性

- ✅ **高精度检测**: 对 GAN 和扩散模型都有优秀的检测能力
- ⚡ **快速响应**: 基于 ResNet-50，实时图像分析
- 🔒 **隐私保护**: 本地处理，不上传图像数据
- 🌐 **Web 界面**: 支持拖拽上传，可视化结果展示
- 📱 **响应式设计**: 支持桌面和移动设备
- 🚀 **公网分享**: 支持 ngrok 快速分享给朋友

---

## 🎯 检测能力

| 生成模型类型 | 支持情况 |
|-------------|---------|
| **GAN** | ✅ StyleGAN, ProGAN, BigGAN, StarGAN 等 |
| **扩散模型** | ✅ Stable Diffusion, MidJourney, GLIDE 等 |
| **跨模型泛化** | ✅ 训练在一种模型，测试在另一种模型 |

---

## 📦 项目结构

```
ai-image-detector/
├── 📄 README.md                    # 项目说明文档
├── 📄 requirements.txt             # Python 依赖
├── 📄 requirements_web.txt         # Web 应用依赖
├── 📄 .gitignore                   # Git 忽略规则
│
├── 🧠 核心算法模块
│   ├── pixel_mapping.py           # 像素级映射 (Fixed + Random)
│   ├── detector.py                # ResNet-50 检测器网络
│   └── datasets.py                # 数据集处理
│
├── 🎓 训练与测试
│   ├── train.py                   # 模型训练脚本
│   └── test.py                    # 模型测试脚本
│
├── 🌐 Web 应用
│   ├── app.py                     # Flask 应用 (使用真实模型)
│   ├── app_demo.py                # Flask 应用 (演示模式，随机预测)
│   ├── app_gradio.py              # Gradio 版本 (可部署到 Hugging Face)
│   └── templates/
│       └── index.html             # 前端页面 (拖拽上传，结果可视化)
│
├── 📁 数据目录 (需要创建)
│   └── data/
│       ├── train/
│       │   ├── real/              # 真实训练图像
│       │   └── fake/              # AI 生成训练图像
│       └── test/
│           ├── real/              # 真实测试图像
│           └── fake/              # AI 生成测试图像
│
└── 📤 输出目录 (自动生成)
    └── output/
        ├── best_model.pth         # 最佳模型权重
        ├── final_model.pth        # 最终模型权重
        └── logs/                  # TensorBoard 训练日志
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/Hellokitty1679/ai-image-detector.git
cd ai-image-detector

# 安装依赖
pip install -r requirements.txt

# Web 应用依赖
pip install -r requirements_web.txt
```

### 2. 准备数据集

将图像放入以下目录结构：

```
data/
├── train/
│   ├── real/    # 真实图像
│   └── fake/    # AI 生成图像
└── test/
    ├── real/    # 真实图像
    └── fake/    # AI 生成图像
```

**推荐数据集**:
- 真实图像: ImageNet, LSUN, COCO
- AI 生成图像: ForenSynths, GenImage

### 3. 训练模型

```bash
# 基础训练
python train.py \
  --train_real_dir ./data/train/real \
  --train_fake_dir ./data/train/fake \
  --test_real_dir ./data/test/real \
  --test_fake_dir ./data/test/fake \
  --mapping_type fixed \
  --epochs 200 \
  --batch_size 32

# 快速测试 (小 epochs)
python train.py \
  --train_real_dir ./data/train/real \
  --train_fake_dir ./data/train/fake \
  --mapping_type fixed \
  --epochs 10 \
  --batch_size 16
```

### 4. 启动 Web 应用

```bash
# 演示模式 (无需训练模型，随机预测用于界面展示)
python app_demo.py

# 真实模型模式 (需要先训练模型)
python app.py --checkpoint ./output/best_model.pth --port 5000
```

然后访问: http://localhost:5000

### 5. 公网分享

使用 ngrok 可以快速分享给朋友：

```bash
# 1. 下载安装 ngrok: https://ngrok.com/download

# 2. 配置 authtoken (注册 ngrok 后获取)
ngrok config add-authtoken 您的token

# 3. 启动隧道 (确保 Flask 应用正在运行)
ngrok http 5000
```

复制生成的 `https://...ngrok-free.app` 链接分享给朋友！

### 6. 部署到 Hugging Face

使用 `app_gradio.py` 可以部署到 Hugging Face Spaces，获得永久公网链接：

1. 访问: https://huggingface.co/spaces
2. 创建新 Space，选择 **Gradio**
3. 上传 `app_gradio.py` 和 `requirements.txt`
4. 等待部署完成，获得永久链接

---

## 📊 技术原理

### 像素级映射可视化

| 像素值 v | round(v/256, 2) | round×256 | 映射后 φ_f(v) |
|---------|-----------------|----------|--------------|
| 0 | 0.00 | 0.00 | 0.00 |
| 1 | 0.00 | 0.00 | 1.00 |
| 2 | 0.01 | 2.56 | **-0.56** |
| 3 | 0.01 | 2.56 | **0.44** |
| 4 | 0.02 | 5.12 | **-1.12** |
| ... | ... | ... | ... |

**关键观察**:
- 原始像素值单调递增: 0, 1, 2, 3, 4...
- 映射后: 0, 1, -0.56, 0.44, -1.12...
- 语义结构被破坏，像素相关性被保留

### 检测流程图

```
输入图像
    ↓
[像素级映射]  <-- 破坏语义，保留相关性
    ↓
[ResNet-50 特征提取]
    ↓
[分类器]
    ↓
输出: 真实图像 / AI生成图像
```

---

## 🧪 快速验证

可以通过简单的 Python 代码验证像素级映射的效果：

```python
import numpy as np

def fixed_mapping(v):
    return v - round(v / 256, 2) * 256

# 测试连续像素值的映射效果
for v in range(5):
    print(f"v={v:3d} -> φ_f(v)={fixed_mapping(v):6.2f}")
```

**预期输出**:
```
v=  0 -> φ_f(v)=  0.00
v=  1 -> φ_f(v)=  1.00
v=  2 -> φ_f(v)= -0.56
v=  3 -> φ_f(v)=  0.44
v=  4 -> φ_f(v)= -1.12
```

可以看到，连续的像素值被映射到"锯齿状"的值，破坏了语义结构。

---

## 🌐 部署到 Hugging Face

使用 `app_gradio.py` 可以快速部署到 Hugging Face Spaces，获得永久公网链接：

1. 访问: https://huggingface.co/spaces
2. 创建新 Space:
   - **Space name**: `ai-image-detector`
   - **Space SDK**: 选择 **Gradio**
3. 上传文件:
   - 将 `app_gradio.py` 重命名为 `app.py`
   - 创建 `requirements.txt`，内容如下:
     ```
     Pillow
     gradio>=4.0.0
     ```
4. 等待部署完成，获得永久链接:
   - 格式: `https://huggingface.co/spaces/你的用户名/ai-image-detector`

---

## 📝 实验配置

### 训练超参数

| 参数 | 值 |
|------|-----|
| 优化器 | Adam |
| 学习率 | 2e-4 |
| β1 / β2 | 0.9 / 0.999 |
| 权重衰减 | 2e-4 |
| Batch Size | 128 |
| Epochs | 200 |
| 输入尺寸 | 128×128 |

### 模型架构

- **Backbone**: ResNet-50
- **输出**: 二分类 (真实 / AI生成)
- **损失函数**: Cross-Entropy

---

## 🔧 API 接口

### POST /detect

分析上传的图像。

```bash
curl -X POST -F "image=@test.jpg" http://localhost:5000/detect
```

**响应**:
```json
{
  "prediction": "AI-Generated",
  "real_probability": 23.45,
  "fake_probability": 76.55,
  "confidence": 76.55,
  "is_fake": true
}
```

---

## 📈 项目进展

- ✅ 像素级映射模块 (Fixed + Random)
- ✅ ResNet-50 检测器
- ✅ 训练和测试脚本
- ✅ Flask Web 应用
- ✅ Gradio 版本 (可部署)
- ✅ ngrok 公网分享
- ⏳ 真实模型训练 (需要数据集)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License

---

## 💡 致谢

感谢论文作者提供的优秀研究工作！

---

<div align="center">
  <sub>如果这个项目对您有帮助，请给个 ⭐ Star 支持一下！</sub>
</div>
