import os
import io
import torch
import torch.nn.functional as F
from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64
from werkzeug.utils import secure_filename

from detector import build_detector
from pixel_mapping import build_pixel_mapping

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

model = None
device = None


def load_model(checkpoint_path=None, mapping_type='fixed', backbone='resnet50'):
    global model, device
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    print(f"Loading model with mapping_type={mapping_type}, backbone={backbone}")
    model = build_detector(
        backbone=backbone,
        mapping_type=mapping_type,
        pretrained=False
    )
    
    if checkpoint_path and os.path.exists(checkpoint_path):
        print(f"Loading checkpoint from {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
    
    model = model.to(device)
    model.eval()
    
    print("Model loaded successfully!")
    return model


def preprocess_image(image, target_size=256, crop_size=128):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    from torchvision import transforms
    
    transform = transforms.Compose([
        transforms.Resize(target_size),
        transforms.CenterCrop(crop_size),
        transforms.ToTensor(),
    ])
    
    img_tensor = transform(image)
    img_tensor = img_tensor.unsqueeze(0)
    
    return img_tensor


def predict_image(image):
    if model is None:
        raise RuntimeError("Model not loaded. Please load a model first.")
    
    img_tensor = preprocess_image(image)
    img_tensor = img_tensor.to(device)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)
        
        real_prob = probs[0, 0].item()
        fake_prob = probs[0, 1].item()
        
        predicted_class = 1 if fake_prob > 0.5 else 0
        confidence = max(real_prob, fake_prob)
    
    result = {
        'prediction': 'AI-Generated' if predicted_class == 1 else 'Real',
        'real_probability': round(real_prob * 100, 2),
        'fake_probability': round(fake_prob * 100, 2),
        'confidence': round(confidence * 100, 2),
        'is_fake': predicted_class == 1,
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
        
        if model is None:
            return jsonify({
                'error': 'Model not loaded. Please check the model path in app.py',
                'model_status': 'not_loaded'
            }), 500
        
        result = predict_image(image)
        result['image_base64'] = img_base64
        
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
        
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded'
            }), 500
        
        result = predict_image(image)
        
        return jsonify({
            'success': True,
            'result': result
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
    parser = argparse.ArgumentParser(description='AI-Generated Image Detection Web App')
    parser.add_argument('--checkpoint', type=str, default=None, help='Path to model checkpoint')
    parser.add_argument('--mapping_type', type=str, default='fixed', choices=['fixed', 'random', 'none'], help='Pixel mapping type')
    parser.add_argument('--backbone', type=str, default='resnet50', choices=['resnet18', 'resnet50'], help='Backbone network')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
    
    args = parser.parse_args()
    
    try:
        load_model(
            checkpoint_path=args.checkpoint,
            mapping_type=args.mapping_type,
            backbone=args.backbone
        )
    except Exception as e:
        print(f"Warning: Could not load model: {e}")
        print("Running in demo mode. Please provide a valid checkpoint path.")
    
    print("\n" + "="*60)
    print("AI-Generated Image Detection Web App")
    print("="*60)
    print(f"Access the web interface at: http://localhost:{args.port}")
    print(f"Model status: {'Loaded' if model is not None else 'Not Loaded (Demo Mode)'}")
    print("="*60 + "\n")
    
    app.run(host=args.host, port=args.port, debug=False)
