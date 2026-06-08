import torch
import torch.nn as nn
import torchvision.models as models
from pixel_mapping import build_pixel_mapping


class Detector(nn.Module):
    def __init__(self, backbone='resnet50', mapping_type='fixed', pretrained=False, num_classes=2):
        super(Detector, self).__init__()
        
        self.mapping = build_pixel_mapping(mapping_type)
        self.backbone_name = backbone
        
        if backbone == 'resnet50':
            self.backbone = models.resnet50(pretrained=pretrained)
            num_features = self.backbone.fc.in_features
            self.backbone.fc = nn.Identity()
        elif backbone == 'resnet18':
            self.backbone = models.resnet18(pretrained=pretrained)
            num_features = self.backbone.fc.in_features
            self.backbone.fc = nn.Identity()
        else:
            raise ValueError(f"Unknown backbone: {backbone}")
        
        self.classifier = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x, return_features=False):
        x = self.mapping(x)
        
        features = self.backbone(x)
        
        logits = self.classifier(features)
        
        if return_features:
            return logits, features
        return logits
    
    def extract_features(self, x):
        x = self.mapping(x)
        features = self.backbone(x)
        return features


def build_detector(backbone='resnet50', mapping_type='fixed', pretrained=False):
    return Detector(backbone=backbone, mapping_type=mapping_type, pretrained=pretrained)
