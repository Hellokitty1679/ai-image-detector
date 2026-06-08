import os
import random
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms


class FakeImageDataset(Dataset):
    def __init__(self, real_dir, fake_dir, transform=None, crop_size=128, is_train=True):
        self.real_dir = real_dir
        self.fake_dir = fake_dir
        self.transform = transform
        self.crop_size = crop_size
        self.is_train = is_train
        
        self.real_paths = self._get_image_paths(real_dir)
        self.fake_paths = self._get_image_paths(fake_dir)
        
        self.all_paths = [(p, 0) for p in self.real_paths] + [(p, 1) for p in self.fake_paths]
        
        if is_train:
            random.shuffle(self.all_paths)
        
        print(f"Dataset initialized: {len(self.real_paths)} real, {len(self.fake_paths)} fake images")
    
    def _get_image_paths(self, directory):
        if not os.path.exists(directory):
            return []
        
        image_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    image_paths.append(os.path.join(root, file))
        return sorted(image_paths)
    
    def __len__(self):
        return len(self.all_paths)
    
    def __getitem__(self, idx):
        img_path, label = self.all_paths[idx]
        
        img = Image.open(img_path).convert('RGB')
        
        if self.transform is not None:
            img = self.transform(img)
        else:
            img = transforms.ToTensor()(img)
        
        return img, torch.tensor(label, dtype=torch.long)


def get_train_transforms(crop_size=128):
    return transforms.Compose([
        transforms.RandomCrop(crop_size),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ToTensor(),
    ])


def get_test_transforms(crop_size=128):
    return transforms.Compose([
        transforms.CenterCrop(crop_size),
        transforms.ToTensor(),
    ])


def build_dataloader(real_dir, fake_dir, batch_size=32, crop_size=128, is_train=True, num_workers=4):
    if is_train:
        transform = get_train_transforms(crop_size)
        shuffle = True
    else:
        transform = get_test_transforms(crop_size)
        shuffle = False
    
    dataset = FakeImageDataset(
        real_dir=real_dir,
        fake_dir=fake_dir,
        transform=transform,
        crop_size=crop_size,
        is_train=is_train
    )
    
    if len(dataset) == 0:
        return None
    
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return dataloader
