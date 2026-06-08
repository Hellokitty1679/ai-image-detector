import gradio as gr
import io
import base64
from PIL import Image
import random

from pixel_mapping import FixedPixelMapping, RandomPixelMapping


def generate_mapping_visualization(pixel_value=128):
    visualizations = []
    
    fixed_mapping = FixedPixelMapping()
    mapping_table = fixed_mapping.fixed_mapping.numpy()
    
    test_values = list(range(0, 256, 16))
    original_values = []
    mapped_values = []
    
    for v in test_values:
        mapped = mapping_table[v]
        original_values.append(v)
        mapped_values.append(mapped)
    
    html_content = f"""
    <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
        <h3 style="margin-top: 0;">🎯 像素级映射演示</h3>
        
        <p style="font-size: 0.95em; line-height: 1.6;">
            本系统使用论文提出的 <strong>像素级映射技术</strong>（Pixel-Level Mapping）来检测AI生成的图像。
        </p>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
            <h4 style="margin-top: 0;">📐 映射公式</h4>
            <code style="background: rgba(0,0,0,0.3); padding: 5px 10px; border-radius: 5px;">
                φ_f(v) = v - round(v/256, 2) × 256
            </code>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
            <h4 style="margin-top: 0;">🔍 核心原理</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li>✅ 破坏图像的语义线索</li>
                <li>✅ 将低频信息转换为高频</li>
                <li>✅ 保留像素间的相关性</li>
                <li>✅ 迫使模型关注生成痕迹</li>
            </ul>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <h4 style="margin-top: 0;">📊 示例映射（像素值 {pixel_value}）</h4>
            <p style="font-family: monospace; font-size: 1.1em;">
                原始值: <strong>{pixel_value}</strong> → 
                映射后: <strong>{mapping_table[pixel_value]:.4f}</strong>
            </p>
            <p style="font-size: 0.85em; opacity: 0.8;">
                范围: [{mapping_table.min():.2f}, {mapping_table.max():.2f}]
            </p>
        </div>
    </div>
    """
    
    return html_content


def predict_image(image):
    if image is None:
        return None, "📷 请上传图片进行检测"
    
    random.seed(hash(str(image.size)))
    is_fake = random.random() > 0.5
    confidence = random.uniform(60, 95)
    
    if is_fake:
        fake_prob = confidence
        real_prob = 100 - confidence
        result_label = "🚨 AI生成图像"
        result_color = "red"
    else:
        real_prob = confidence
        fake_prob = 100 - confidence
        result_label = "✅ 真实图像"
        result_color = "green"
    
    result_text = f"""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: {result_color}; margin-bottom: 20px;">{result_label}</h2>
        
        <div style="display: flex; justify-content: space-around; margin: 30px 0;">
            <div style="text-align: center;">
                <div style="font-size: 2.5em; color: #10b981;">{real_prob:.1f}%</div>
                <div style="color: #666;">真实图像</div>
                <div style="width: 100px; height: 10px; background: #e5e7eb; border-radius: 5px; margin-top: 10px; overflow: hidden;">
                    <div style="width: {real_prob}%; height: 100%; background: linear-gradient(90deg, #10b981, #059669); border-radius: 5px;"></div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <div style="font-size: 2.5em; color: #ef4444;">{fake_prob:.1f}%</div>
                <div style="color: #666;">AI生成</div>
                <div style="width: 100px; height: 10px; background: #e5e7eb; border-radius: 5px; margin-top: 10px; overflow: hidden;">
                    <div style="width: {fake_prob}%; height: 100%; background: linear-gradient(90deg, #ef4444, #dc2626); border-radius: 5px;"></div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; border-radius: 10px; background: #f8f9fa;">
            <div style="font-weight: bold; margin-bottom: 10px;">🎯 置信度</div>
            <div style="font-size: 1.2em;">{confidence:.1f}%</div>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; border-radius: 10px; background: #fff3cd; color: #856404;">
            ⚠️ <strong>演示模式</strong><br>
            此结果为随机生成，用于演示界面功能。<br>
            要获得真实检测结果，请训练模型后部署。
        </div>
    </div>
    """
    
    return result_text, None


with gr.Blocks(
    title="AI生成图像检测系统",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    """
) as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown(
                """
                # 🤖 AI生成图像检测
                
                ### 基于像素级映射的AI图像检测系统
                
                上传图片，检测是否为AI生成
                """
            )
            
            image_input = gr.Image(
                type="pil",
                label="上传图片",
                height=400,
                elem_id="image_upload"
            )
            
            with gr.Row():
                detect_btn = gr.Button("🔍 开始检测", variant="primary", scale=2)
                clear_btn = gr.Button("🗑️ 清空", variant="secondary", scale=1)
        
        with gr.Column(scale=1):
            result_output = gr.HTML(label="检测结果")
            mapping_info = gr.HTML(
                value=generate_mapping_visualization(),
                label="技术原理"
            )
    
    pixel_slider = gr.Slider(
        minimum=0,
        maximum=255,
        value=128,
        step=1,
        label="调整像素值查看映射效果"
    )
    
    pixel_slider.change(
        fn=generate_mapping_visualization,
        inputs=[pixel_slider],
        outputs=[mapping_info]
    )
    
    detect_btn.click(
        fn=predict_image,
        inputs=[image_input],
        outputs=[result_output]
    )
    
    clear_btn.click(
        fn=lambda: (None, None),
        inputs=[],
        outputs=[image_input, result_output]
    )
    
    gr.Markdown(
        """
        ---
        
        ## 📖 使用说明
        
        1. **上传图片**: 点击上传区域选择图片，或直接拖拽图片
        2. **开始检测**: 点击"开始检测"按钮
        3. **查看结果**: 系统会显示检测结果和概率分析
        
        ---
        
        ## 🧠 技术原理
        
        本系统基于论文 **"Beyond Semantic Features: Pixel-level Mapping for Generalized AI-Generated Image Detection"**
        (arXiv: 2512.17350, AAAI 2026)
        
        ### 核心思想
        
        传统的AI图像检测器容易过度依赖语义线索，导致对未知生成模型泛化能力差。
        
        本方法通过**像素级映射**：
        - 破坏图像的语义结构
        - 保留像素间的相关性
        - 迫使模型关注生成过程中的高频痕迹
        
        ### 检测能力
        
        - ✅ GAN生成图像（StyleGAN, ProGAN, BigGAN等）
        - ✅ 扩散模型图像（Stable Diffusion, MidJourney等）
        - ✅ 跨模型泛化检测
        
        ---
        
        ## 🔗 相关链接
        
        - 📄 论文: https://arxiv.org/abs/2512.17350
        - 💻 代码: https://github.com/（待更新）
        
        ---
        
        ⚠️ **注意**: 当前为演示模式，使用随机预测。请训练真实模型以获得准确结果。
        """
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )
