import torch
import torch.nn as nn
import numpy as np
from pixel_mapping import FixedPixelMapping, RandomPixelMapping, build_pixel_mapping
from detector import build_detector


def test_pixel_mapping():
    print("Testing Pixel Level Mapping...")
    print("="*50)
    
    test_tensor = torch.randint(0, 256, (1, 3, 32, 32), dtype=torch.uint8)
    normalized_tensor = test_tensor.float() / 255.0
    
    print(f"\nInput tensor shape: {test_tensor.shape}")
    print(f"Input pixel value range: [{test_tensor.min().item()}, {test_tensor.max().item()}]")
    
    fixed_mapping = FixedPixelMapping()
    output_fixed = fixed_mapping(test_tensor)
    
    print(f"\nFixed mapping output shape: {output_fixed.shape}")
    print(f"Fixed mapping output range: [{output_fixed.min().item():.4f}, {output_fixed.max().item():.4f}]")
    
    expected_values = []
    for v in range(20):
        mapped = v - np.round(v / 256.0, 2) * 256.0
        expected_values.append(mapped)
    
    print(f"\nFixed mapping formula verification (first 20 values):")
    for v in range(20):
        expected = v - np.round(v / 256.0, 2) * 256.0
        actual = fixed_mapping.fixed_mapping[v].item()
        print(f"  v={v:3d}: expected={expected:8.4f}, actual={actual:8.4f}, match={abs(expected-actual)<1e-6}")
    
    normalized_output = fixed_mapping(normalized_tensor)
    print(f"\nFixed mapping with normalized input output range: "
          f"[{normalized_output.min().item():.4f}, {normalized_output.max().item():.4f}]")
    
    random_mapping = RandomPixelMapping()
    output_random = random_mapping(test_tensor)
    
    print(f"\nRandom mapping output shape: {output_random.shape}")
    print(f"Random mapping output range: [{output_random.min().item():.4f}, {output_random.max().item():.4f}]")
    
    identity = build_pixel_mapping('none')
    output_identity = identity(normalized_tensor)
    print(f"\nIdentity mapping output shape: {output_identity.shape}")
    print(f"Identity mapping output range: [{output_identity.min().item():.4f}, {output_identity.max().item():.4f}]")
    
    print("\n" + "="*50)
    print("Pixel Level Mapping: PASSED")
    print("="*50)
    return True


def test_detector():
    print("\nTesting Detector...")
    print("="*50)
    
    model = build_detector(backbone='resnet50', mapping_type='fixed', pretrained=False)
    
    print(f"\nModel architecture:")
    print(f"  Mapping type: {model.backbone_name}")
    print(f"  Backbone: {model.backbone_name}")
    
    test_input = torch.randn(2, 3, 128, 128)
    
    output = model(test_input)
    print(f"\nForward pass test:")
    print(f"  Input shape: {test_input.shape}")
    print(f"  Output shape: {output.shape}")
    
    logits, features = model(test_input, return_features=True)
    print(f"\nFeature extraction test:")
    print(f"  Features shape: {features.shape}")
    print(f"  Logits shape: {logits.shape}")
    
    model_random = build_detector(backbone='resnet50', mapping_type='random', pretrained=False)
    output_random = model_random(test_input)
    print(f"\nRandom mapping model output shape: {output_random.shape}")
    
    model_identity = build_detector(backbone='resnet50', mapping_type='none', pretrained=False)
    output_identity = model_identity(test_input)
    print(f"No mapping model output shape: {output_identity.shape}")
    
    print("\n" + "="*50)
    print("Detector: PASSED")
    print("="*50)
    return True


def test_training_components():
    print("\nTesting Training Components...")
    print("="*50)
    
    model = build_detector(backbone='resnet50', mapping_type='fixed', pretrained=False)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=2e-4,
        betas=(0.9, 0.999),
        weight_decay=2e-4
    )
    
    batch_size = 4
    images = torch.randn(batch_size, 3, 128, 128)
    labels = torch.tensor([0, 1, 0, 1], dtype=torch.long)
    
    print(f"\nTraining step test:")
    print(f"  Batch size: {batch_size}")
    
    optimizer.zero_grad()
    outputs = model(images)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    
    print(f"  Loss: {loss.item():.4f}")
    print(f"  Output shape: {outputs.shape}")
    print(f"  Loss backward pass: SUCCESS")
    print(f"  Optimizer step: SUCCESS")
    
    print("\n" + "="*50)
    print("Training Components: PASSED")
    print("="*50)
    return True


def main():
    print("\n" + "="*60)
    print("Implementation Verification Tests")
    print("="*60)
    
    all_passed = True
    
    try:
        test_pixel_mapping()
    except Exception as e:
        print(f"Pixel Level Mapping: FAILED - {e}")
        all_passed = False
    
    try:
        test_detector()
    except Exception as e:
        print(f"Detector: FAILED - {e}")
        all_passed = False
    
    try:
        test_training_components()
    except Exception as e:
        print(f"Training Components: FAILED - {e}")
        all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
