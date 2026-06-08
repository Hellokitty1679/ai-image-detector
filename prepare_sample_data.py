import os
import random
import argparse
from pathlib import Path


def create_directory_structure(base_dir):
    dirs = [
        'data/train/real',
        'data/train/fake',
        'data/test/real',
        'data/test/fake',
    ]
    
    for d in dirs:
        path = os.path.join(base_dir, d)
        Path(path).mkdir(parents=True, exist_ok=True)
        print(f"Created: {path}")


def generate_data_structure_info():
    info = """
Dataset Structure:
===================

Expected directory structure:
data/
├── train/
│   ├── real/          # Real images for training
│   │   ├── img_001.png
│   │   ├── img_002.png
│   │   └── ...
│   └── fake/          # AI-generated images for training
│       ├── img_001.png
│       ├── img_002.png
│       └── ...
└── test/
    ├── real/            # Real images for testing
    │   ├── img_001.png
    │   ├── img_002.png
    │   └── ...
    └── fake/            # AI-generated images for testing
        ├── img_001.png
        ├── img_002.png
        └── ...

Supported image formats: .png, .jpg, .jpeg, .bmp, .tiff
"""
    return info


def create_placeholder_images():
    placeholder = """
To use this project, you need to:
===============================

1. Prepare Real Images:
   - Collect real photographs (e.g., from LSUN, ImageNet, COCO, or your own photos)
   - Place them in data/train/real/ and data/test/real/

2. Prepare Fake Images:
   - Generate or collect AI-generated images
   - Using models: StyleGAN, ProGAN, Stable Diffusion, etc.
   - Place them in data/train/fake/ and data/test/fake/

3. Recommended Dataset Sizes:
   - Training: 10,000+ images (5,000 real + 5,000 fake)
   - Testing: 2,000+ images (1,000 real + 1,000 fake)

4. Example Datasets You Can Use:
   - ForenSynths (GAN-generated images)
   - GenImage (diffusion-generated images)
   - ImageNet (real images)
   - LSUN (real images)
   - COCO (real images)
"""
    return placeholder


def main():
    parser = argparse.ArgumentParser(description='Prepare sample dataset structure')
    parser.add_argument('--base_dir', type=str, default='.', help='Base directory')
    args = parser.parse_args()
    
    print("="*60)
    print("Creating Sample Dataset Structure")
    print("="*60)
    
    create_directory_structure(args.base_dir)
    
    print("\n" + "="*60)
    print("Directory Structure Created!")
    print("="*60)
    
    print(generate_data_structure_info())
    print(create_placeholder_images())
    
    info_path = os.path.join(args.base_dir, 'data', 'README.txt')
    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(generate_data_structure_info())
        f.write(create_placeholder_images())
    
    print(f"\nDetailed instructions saved to: {info_path}")
    
    print("\n" + "="*60)
    print("Quick Start Training:")
    print("="*60)
    print("""
Once you have prepared your data, run:

python train.py \\
    --train_real_dir ./data/train/real \\
    --train_fake_dir ./data/train/fake \\
    --test_real_dir ./data/test/real \\
    --test_fake_dir ./data/test/fake \\
    --mapping_type fixed \\
    --epochs 200 \\
    --batch_size 32
""")


if __name__ == '__main__':
    main()
