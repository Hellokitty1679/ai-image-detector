import subprocess
import sys
import os


def main():
    print("="*70)
    print("Example Training Script")
    print("="*70)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    configs = [
        {
            'name': 'Fixed Mapping (Recommended)',
            'args': [
                sys.executable, 'train.py',
                '--train_real_dir', os.path.join(base_dir, 'data', 'train', 'real'),
                '--train_fake_dir', os.path.join(base_dir, 'data', 'train', 'fake'),
                '--test_real_dir', os.path.join(base_dir, 'data', 'test', 'real'),
                '--test_fake_dir', os.path.join(base_dir, 'data', 'test', 'fake'),
                '--mapping_type', 'fixed',
                '--backbone', 'resnet50',
                '--epochs', '200',
                '--batch_size', '32',
                '--lr', '2e-4',
                '--output_dir', './output_fixed',
            ]
        },
        {
            'name': 'Random Mapping',
            'args': [
                sys.executable, 'train.py',
                '--train_real_dir', os.path.join(base_dir, 'data', 'train', 'real'),
                '--train_fake_dir', os.path.join(base_dir, 'data', 'train', 'fake'),
                '--test_real_dir', os.path.join(base_dir, 'data', 'test', 'real'),
                '--test_fake_dir', os.path.join(base_dir, 'data', 'test', 'fake'),
                '--mapping_type', 'random',
                '--backbone', 'resnet50',
                '--epochs', '200',
                '--batch_size', '32',
                '--lr', '2e-4',
                '--output_dir', './output_random',
            ]
        },
        {
            'name': 'Baseline (No Mapping)',
            'args': [
                sys.executable, 'train.py',
                '--train_real_dir', os.path.join(base_dir, 'data', 'train', 'real'),
                '--train_fake_dir', os.path.join(base_dir, 'data', 'train', 'fake'),
                '--test_real_dir', os.path.join(base_dir, 'data', 'test', 'real'),
                '--test_fake_dir', os.path.join(base_dir, 'data', 'test', 'fake'),
                '--mapping_type', 'none',
                '--backbone', 'resnet50',
                '--epochs', '200',
                '--batch_size', '32',
                '--lr', '2e-4',
                '--output_dir', './output_baseline',
            ]
        },
    ]
    
    print("\nAvailable Training Configurations:")
    print("-"*70)
    for i, config in enumerate(configs):
        print(f"\n[{i+1}] {config['name']}")
        print("    Command:")
        print("    " + ' '.join(config['args'][1:]))
    
    print("\n" + "="*70)
    print("Quick Commands:")
    print("="*70)
    
    print("\n1. Fixed Mapping (Recommended):")
    print(f"python train.py --train_real_dir ./data/train/real --train_fake_dir ./data/train/fake --test_real_dir ./data/test/real --test_fake_dir ./data/test/fake --mapping_type fixed --epochs 200 --batch_size 32")
    
    print("\n2. Random Mapping:")
    print(f"python train.py --train_real_dir ./data/train/real --train_fake_dir ./data/train/fake --test_real_dir ./data/test/real --test_fake_dir ./data/test/fake --mapping_type random --epochs 200 --batch_size 32")
    
    print("\n3. Quick Test (Small Epochs):")
    print(f"python train.py --train_real_dir ./data/train/real --train_fake_dir ./data/train/fake --test_real_dir ./data/test/real --test_fake_dir ./data/test/fake --mapping_type fixed --epochs 10 --batch_size 16")
    
    print("\n" + "="*70)
    print("Test Model:")
    print("="*70)
    print(f"\npython test.py --test_real_dir ./data/test/real --test_fake_dir ./data/test/fake --checkpoint_path ./output_fixed/best_model.pth --mapping_type fixed")
    
    print("\n" + "="*70)
    print("Note: Please ensure you have placed images in the data/ directories first!")
    print("="*70)


if __name__ == '__main__':
    main()
