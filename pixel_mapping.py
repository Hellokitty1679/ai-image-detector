import torch
import torch.nn as nn
import numpy as np


class PixelLevelMapping(nn.Module):
    def __init__(self, mapping_type='fixed'):
        super(PixelLevelMapping, self).__init__()
        self.mapping_type = mapping_type
        
        if mapping_type == 'fixed':
            self._build_fixed_mapping()
        elif mapping_type == 'random':
            self._build_random_mapping()
        else:
            raise ValueError(f"Unknown mapping type: {mapping_type}")
    
    def _build_fixed_mapping(self):
        pixel_values = np.arange(256, dtype=np.float64)
        mapped = pixel_values - np.round(pixel_values / 256.0, 2) * 256.0
        
        fixed_mapping = torch.from_numpy(mapped).float()
        self.register_buffer('fixed_mapping', fixed_mapping)
    
    def _build_random_mapping(self):
        pass
    
    def forward(self, x):
        if x.dtype != torch.uint8:
            x = torch.clamp(x, 0, 1)
            x = (x * 255.0).round().to(torch.int64)
        else:
            x = x.long()
        
        if self.mapping_type == 'fixed':
            return self._apply_fixed_mapping(x)
        else:
            return self._apply_random_mapping(x)
    
    def _apply_fixed_mapping(self, x):
        batch_size, channels, height, width = x.shape
        x_flat = x.reshape(-1)
        
        mapped_flat = self.fixed_mapping[x_flat]
        
        mapped = mapped_flat.reshape(batch_size, channels, height, width)
        
        return mapped
    
    def _apply_random_mapping(self, x):
        batch_size, channels, height, width = x.shape
        
        result = torch.empty_like(x, dtype=torch.float32, device=x.device)
        
        for b in range(batch_size):
            for c in range(channels):
                random_mapping = torch.rand(256, device=x.device) * 2.0 - 1.0
                x_flat = x[b, c].reshape(-1)
                mapped_flat = random_mapping[x_flat]
                result[b, c] = mapped_flat.reshape(height, width)
        
        return result


class FixedPixelMapping(PixelLevelMapping):
    def __init__(self):
        super(FixedPixelMapping, self).__init__(mapping_type='fixed')


class RandomPixelMapping(PixelLevelMapping):
    def __init__(self):
        super(RandomPixelMapping, self).__init__(mapping_type='random')


def build_pixel_mapping(mapping_type='fixed'):
    if mapping_type == 'fixed':
        return FixedPixelMapping()
    elif mapping_type == 'random':
        return RandomPixelMapping()
    elif mapping_type == 'none':
        return nn.Identity()
    else:
        raise ValueError(f"Unknown mapping type: {mapping_type}")
