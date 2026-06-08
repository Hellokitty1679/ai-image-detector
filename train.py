import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import numpy as np
from sklearn.metrics import average_precision_score

from detector import build_detector
from datasets import build_dataloader


def parse_args():
    parser = argparse.ArgumentParser(description='Train AI-generated image detector')
    
    parser.add_argument('--train_real_dir', type=str, required=True, help='Directory of real training images')
    parser.add_argument('--train_fake_dir', type=str, required=True, help='Directory of fake training images')
    parser.add_argument('--test_real_dir', type=str, default=None, help='Directory of real test images')
    parser.add_argument('--test_fake_dir', type=str, default=None, help='Directory of fake test images')
    
    parser.add_argument('--backbone', type=str, default='resnet50', choices=['resnet18', 'resnet50'], help='Backbone network')
    parser.add_argument('--mapping_type', type=str, default='fixed', choices=['fixed', 'random', 'none'], help='Pixel mapping type')
    
    parser.add_argument('--batch_size', type=int, default=128, help='Batch size')
    parser.add_argument('--crop_size', type=int, default=128, help='Crop size')
    parser.add_argument('--epochs', type=int, default=200, help='Number of epochs')
    parser.add_argument('--lr', type=float, default=2e-4, help='Learning rate')
    parser.add_argument('--weight_decay', type=float, default=2e-4, help='Weight decay')
    parser.add_argument('--beta1', type=float, default=0.9, help='Adam beta1')
    parser.add_argument('--beta2', type=float, default=0.999, help='Adam beta2')
    
    parser.add_argument('--output_dir', type=str, default='./output', help='Output directory')
    parser.add_argument('--save_freq', type=int, default=50, help='Save frequency')
    parser.add_argument('--num_workers', type=int, default=4, help='Number of workers')
    
    parser.add_argument('--use_pretrained', action='store_true', help='Use pretrained backbone')
    
    return parser.parse_args()


def train_epoch(model, dataloader, criterion, optimizer, device, epoch):
    model.train()
    
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    all_scores = []
    
    pbar = tqdm(dataloader, desc=f'Epoch {epoch+1} [Train]')
    for images, labels in pbar:
        images = images.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
        
        probs = torch.softmax(outputs, dim=1)
        scores = probs[:, 1].detach().cpu().numpy()
        preds = torch.argmax(outputs, dim=1)
        
        total += labels.size(0)
        correct += (preds == labels).sum().item()
        
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        all_scores.extend(scores)
        
        pbar.set_postfix({
            'loss': f'{loss.item():.4f}',
            'acc': f'{100 * correct / total:.2f}%'
        })
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    epoch_ap = average_precision_score(all_labels, all_scores)
    
    return epoch_loss, epoch_acc, epoch_ap


def evaluate(model, dataloader, criterion, device, epoch=0, phase='Test'):
    model.eval()
    
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    all_scores = []
    
    with torch.no_grad():
        pbar = tqdm(dataloader, desc=f'Epoch {epoch+1} [{phase}]')
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
            correct += (preds == labels).sum().item()
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_scores.extend(scores)
            
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100 * correct / total:.2f}%'
            })
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    epoch_ap = average_precision_score(all_labels, all_scores) if len(np.unique(all_labels)) > 1 else 0.0
    
    return epoch_loss, epoch_acc, epoch_ap


def main():
    args = parse_args()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    os.makedirs(args.output_dir, exist_ok=True)
    log_dir = os.path.join(args.output_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    writer = SummaryWriter(log_dir)
    
    print("Building dataloaders...")
    train_loader = build_dataloader(
        real_dir=args.train_real_dir,
        fake_dir=args.train_fake_dir,
        batch_size=args.batch_size,
        crop_size=args.crop_size,
        is_train=True,
        num_workers=args.num_workers
    )
    
    if train_loader is None:
        print("Error: Training dataset is empty!")
        return
    
    test_loader = None
    if args.test_real_dir and args.test_fake_dir:
        test_loader = build_dataloader(
            real_dir=args.test_real_dir,
            fake_dir=args.test_fake_dir,
            batch_size=args.batch_size,
            crop_size=args.crop_size,
            is_train=False,
            num_workers=args.num_workers
        )
    
    print(f"Building model: {args.backbone} with {args.mapping_type} mapping...")
    model = build_detector(
        backbone=args.backbone,
        mapping_type=args.mapping_type,
        pretrained=args.use_pretrained
    )
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(
        model.parameters(),
        lr=args.lr,
        betas=(args.beta1, args.beta2),
        weight_decay=args.weight_decay
    )
    
    best_acc = 0.0
    best_ap = 0.0
    
    print(f"Starting training for {args.epochs} epochs...")
    for epoch in range(args.epochs):
        train_loss, train_acc, train_ap = train_epoch(
            model, train_loader, criterion, optimizer, device, epoch
        )
        
        print(f"Train - Loss: {train_loss:.4f}, Acc: {train_acc:.4f}, AP: {train_ap:.4f}")
        
        writer.add_scalar('Loss/train', train_loss, epoch)
        writer.add_scalar('Accuracy/train', train_acc, epoch)
        writer.add_scalar('AP/train', train_ap, epoch)
        
        if test_loader is not None:
            test_loss, test_acc, test_ap = evaluate(
                model, test_loader, criterion, device, epoch
            )
            
            print(f"Test  - Loss: {test_loss:.4f}, Acc: {test_acc:.4f}, AP: {test_ap:.4f}")
            
            writer.add_scalar('Loss/test', test_loss, epoch)
            writer.add_scalar('Accuracy/test', test_acc, epoch)
            writer.add_scalar('AP/test', test_ap, epoch)
            
            if test_acc > best_acc:
                best_acc = test_acc
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'acc': test_acc,
                    'ap': test_ap,
                }, os.path.join(args.output_dir, 'best_model.pth'))
                print(f"Best model saved with accuracy: {best_acc:.4f}")
            
            if test_ap > best_ap:
                best_ap = test_ap
        
        if (epoch + 1) % args.save_freq == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
            }, os.path.join(args.output_dir, f'checkpoint_epoch_{epoch+1}.pth'))
    
    torch.save({
        'epoch': args.epochs,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, os.path.join(args.output_dir, 'final_model.pth'))
    
    print("Training completed!")
    if test_loader is not None:
        print(f"Best test accuracy: {best_acc:.4f}")
        print(f"Best test AP: {best_ap:.4f}")
    
    writer.close()


if __name__ == '__main__':
    main()
