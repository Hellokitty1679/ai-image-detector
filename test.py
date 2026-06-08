import os
import argparse
import torch
import torch.nn as nn
from tqdm import tqdm
import numpy as np
from sklearn.metrics import average_precision_score, accuracy_score, classification_report

from detector import build_detector
from datasets import build_dataloader


def parse_args():
    parser = argparse.ArgumentParser(description='Test AI-generated image detector')
    
    parser.add_argument('--test_real_dir', type=str, required=True, help='Directory of real test images')
    parser.add_argument('--test_fake_dir', type=str, required=True, help='Directory of fake test images')
    
    parser.add_argument('--checkpoint_path', type=str, required=True, help='Path to model checkpoint')
    
    parser.add_argument('--backbone', type=str, default='resnet50', choices=['resnet18', 'resnet50'], help='Backbone network')
    parser.add_argument('--mapping_type', type=str, default='fixed', choices=['fixed', 'random', 'none'], help='Pixel mapping type')
    
    parser.add_argument('--batch_size', type=int, default=128, help='Batch size')
    parser.add_argument('--crop_size', type=int, default=128, help='Crop size')
    parser.add_argument('--num_workers', type=int, default=4, help='Number of workers')
    
    return parser.parse_args()


def test(model, dataloader, criterion, device):
    model.eval()
    
    running_loss = 0.0
    total = 0
    all_preds = []
    all_labels = []
    all_scores = []
    
    with torch.no_grad():
        pbar = tqdm(dataloader, desc='Testing')
        for images, labels in pbar:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item() * images.size(0)
            
            probs = torch.softmax(outputs, dim=1)
            scores = probs[:, 1].cpu().numpy()
            preds = torch.argmax(outputs, dim=1)
            
            total += labels.size(0)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_scores.extend(scores)
    
    avg_loss = running_loss / total
    accuracy = accuracy_score(all_labels, all_preds)
    ap = average_precision_score(all_labels, all_scores) if len(np.unique(all_labels)) > 1 else 0.0
    
    print("\n" + "="*50)
    print("Classification Report:")
    print("="*50)
    print(classification_report(all_labels, all_preds, target_names=['Real', 'Fake']))
    
    print("\n" + "="*50)
    print("Summary:")
    print("="*50)
    print(f"Loss: {avg_loss:.4f}")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Average Precision (AP): {ap:.4f}")
    
    return avg_loss, accuracy, ap


def main():
    args = parse_args()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    print("Building test dataloader...")
    test_loader = build_dataloader(
        real_dir=args.test_real_dir,
        fake_dir=args.test_fake_dir,
        batch_size=args.batch_size,
        crop_size=args.crop_size,
        is_train=False,
        num_workers=args.num_workers
    )
    
    if test_loader is None:
        print("Error: Test dataset is empty!")
        return
    
    print(f"Building model: {args.backbone} with {args.mapping_type} mapping...")
    model = build_detector(
        backbone=args.backbone,
        mapping_type=args.mapping_type,
        pretrained=False
    )
    
    print(f"Loading checkpoint from {args.checkpoint_path}...")
    checkpoint = torch.load(args.checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    
    test(model, test_loader, criterion, device)


if __name__ == '__main__':
    main()
