# 部署到 Hugging Face Spaces

Hugging Face Spaces 提供免费的 GPU 资源，适合展示演示。

## 🚀 快速部署

### 步骤1: 准备文件

在项目根目录创建以下文件：

#### 1. requirements.txt
```txt
torch>=1.10.0
torchvision>=0.11.0
numpy>=1.21.0
Pillow>=8.0.0
Flask>=2.0.0
werkzeug>=2.0.0
gradio>=4.0.0
```

#### 2. app_gradio.py
```python
import gradio as gr
import torch
import torch.nn.functional as F
from PIL import Image
import os

from detector import build_detector
from pixel_mapping import build_pixel_mapping

# 加载模型
def load_model():
    # 这里可以加载预训练模型
    # 如果没有预训练模型，可以使用演示模式
    return None

# 预测函数
def predict(image):
    if image is None:
        return "请上传图片", None
    
    # 演示模式 - 随机预测
    import random
    is_fake = random.random() > 0.5
    confidence = random.uniform(60, 95)
    
    if is_fake:
        fake_prob = confidence
        real_prob = 100 - confidence
        result = "🚨 AI生成图像"
    else:
        real_prob = confidence
        fake_prob = 100 - confidence
        result = "✅ 真实图像"
    
    result_text = f"""
    检测结果: {result}
    
    📊 概率分析:
    • 真实图像: {real_prob:.2f}%
    • AI生成: {fake_prob:.2f}%
    • 置信度: {confidence:.2f}%
    
    ⚠️ 演示模式: 使用随机预测
    """
    
    return result_text

# 创建界面
with gr.Blocks(title="AI生成图像检测") as demo:
    gr.Markdown(
        """
        # 🤖 AI生成图像检测
        
        基于像素级映射技术的AI生成图像检测系统
        
        上传图片进行检测，支持拖拽上传！
        """
    )
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="上传图片")
            detect_btn = gr.Button("🔍 开始检测", variant="primary")
        
        with gr.Column():
            result_output = gr.Textbox(label="检测结果", lines=10)
    
    detect_btn.click(
        fn=predict,
        inputs=[image_input],
        outputs=[result_output]
    )
    
    gr.Markdown(
        """
        ## 📖 使用说明
        
        1. 点击上传区域选择图片，或直接拖拽图片
        2. 点击"开始检测"按钮
        3. 查看检测结果
        
        ## ℹ️ 关于
        
        本系统基于论文 "Beyond Semantic Features: Pixel-level Mapping for Generalized AI-Generated Image Detection"
        
        技术特点:
        - 像素级映射技术
        - 支持GAN和扩散模型检测
        - 本地处理，隐私保护
        """
    )

if __name__ == "__main__":
    demo.launch()
```

#### 3. README.md
```markdown
# AI生成图像检测

基于像素级映射技术的AI生成图像检测演示。

## 使用方法

1. 上传图片
2. 点击"开始检测"
3. 查看结果

## 技术原理

使用像素级映射（Pixel-Level Mapping）破坏图像语义线索，
迫使模型关注生成过程中的高频痕迹。

## 参考文献

论文: https://arxiv.org/abs/2512.17350
```

### 步骤2: 注册 Hugging Face

1. 访问 https://huggingface.co/
2. 注册账号（免费）
3. 验证邮箱

### 步骤3: 创建 Space

1. 登录后点击右上角头像 → "New Space"
2. 填写信息：
   - Space name: ai-image-detector
   - License: MIT
   - Space SDK: Gradio
   - Space hardware: CPU basic（免费）
3. 点击 "Create Space"

### 步骤4: 上传文件

有两种方式：

**方式A: 直接上传**
1. 在 Space 页面点击 "Files" 标签
2. 点击 "+ Add file"
3. 上传以下文件：
   - app_gradio.py
   - requirements.txt
   - README.md

**方式B: Git 上传**
```bash
# 克隆仓库
git clone https://huggingface.co/spaces/你的用户名/ai-image-detector

# 复制文件
cp app_gradio.py ai-image-detector/
cp requirements.txt ai-image-detector/
cp README.md ai-image-detector/

# 提交
cd ai-image-detector
git add .
git commit -m "Initial commit"
git push
```

### 步骤5: 等待部署

- 上传后，Hugging Face 会自动构建
- 构建需要几分钟
- 完成后会显示 "Running" 状态

### 步骤6: 分享链接

部署成功后，您可以分享类似这样的链接：
```
https://huggingface.co/spaces/你的用户名/ai-image-detector
```

## 🎯 进阶：添加真实模型

如果您有训练好的模型，可以：

1. 将模型文件（.pth）上传到 Space
2. 修改 app_gradio.py 中的 load_model 函数：

```python
def load_model():
    model = build_detector(
        backbone='resnet50',
        mapping_type='fixed',
        pretrained=False
    )
    
    # 加载预训练权重
    checkpoint = torch.load('best_model.pth', map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    return model
```

## 💰 费用

- **免费层**: 足够演示使用
- **升级层**: 如果需要 GPU 或更高性能

## 🔗 其他平台

- **Replit**: https://replit.com
- **Glitch**: https://glitch.com
- **Render**: https://render.com

这些平台也提供免费部署选项。
