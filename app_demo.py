import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']


def predict_image_demo(image):
    random.seed(hash(str(image.size)))
    is_fake = random.random() > 0.5
    confidence = random.uniform(60, 95)
    
    if is_fake:
        fake_prob = confidence
        real_prob = 100 - confidence
    else:
        real_prob = confidence
        fake_prob = 100 - confidence
    
    result = {
        'prediction': 'AI-Generated' if is_fake else 'Real',
        'real_probability': round(real_prob, 2),
        'fake_probability': round(fake_prob, 2),
        'confidence': round(confidence, 2),
        'is_fake': is_fake,
        'demo_mode': True
    }
    
    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return jsonify({'error': f'Unsupported file type: {file_ext}. Supported: {app.config["UPLOAD_EXTENSIONS"]}'}), 400
        
        image = Image.open(io.BytesIO(file.read()))
        
        buffered = io.BytesIO()
        image.save(buffered, format='PNG')
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        result = predict_image_demo(image)
        result['image_base64'] = img_base64
        result['warning'] = '⚠️ 演示模式：使用随机预测。请训练真实模型以获得准确结果。'
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect', methods=['POST'])
def api_detect():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        image = Image.open(io.BytesIO(file.read()))
        
        result = predict_image_demo(image)
        
        return jsonify({
            'success': True,
            'result': result,
            'demo_mode': True
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def create_directories():
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)


if __name__ == '__main__':
    create_directories()
    
    import argparse
    parser = argparse.ArgumentParser(description='AI-Generated Image Detection Web App (Demo Mode)')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("  🎨 AI生成图像检测 Web应用 (演示模式)")
    print("="*70)
    print("")
    print("  ⚠️  注意：这是演示模式，使用随机预测")
    print("  📊 要获得真实检测结果，请：")
    print("     1. 准备数据集（真实图像和AI生成图像）")
    print("     2. 运行 train.py 训练模型")
    print("     3. 使用 app.py 加载训练好的模型")
    print("")
    print(f"  🌐 访问地址: http://localhost:{args.port}")
    print("  📱 局域网访问: http://<你的IP>:{args.port}")
    print("")
    print("="*70 + "\n")
    
    app.run(host=args.host, port=args.port, debug=False)
