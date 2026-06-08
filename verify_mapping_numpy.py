import numpy as np


def verify_fixed_mapping_formula():
    print("Verifying Fixed Pixel-Level Mapping Formula")
    print("="*60)
    
    print("\nFormula: phi_f(v) = v - round(v/256, 2) * 256")
    print("Purpose: Amplify adjacent pixel differences while normalizing to ~[-1.28, 1.28]")
    
    test_values = list(range(20)) + [64, 128, 192, 255]
    
    print("\nPixel value mapping verification:")
    print("-"*60)
    print(f"{'v':>6} | {'round(v/256, 2)':>15} | {'round*256':>10} | {'phi_f(v)':>10}")
    print("-"*60)
    
    for v in test_values:
        round_val = np.round(v / 256.0, 2)
        mapped = v - round_val * 256.0
        print(f"{v:>6d} | {round_val:>15.4f} | {round_val*256:>10.2f} | {mapped:>10.4f}")
    
    all_values = np.arange(256)
    round_vals = np.round(all_values / 256.0, 2)
    mapped_values = all_values - round_vals * 256.0
    
    print("\n" + "="*60)
    print("Mapping Statistics:")
    print("="*60)
    print(f"Min mapped value: {mapped_values.min():.4f}")
    print(f"Max mapped value: {mapped_values.max():.4f}")
    print(f"Mean mapped value: {mapped_values.mean():.4f}")
    print(f"Unique values: {len(np.unique(mapped_values))}")
    
    print("\n" + "="*60)
    print("Adjacent Pixel Difference Analysis:")
    print("="*60)
    
    original_diffs = np.diff(all_values)
    mapped_diffs = np.diff(mapped_values)
    
    print(f"Original adjacent diffs:")
    print(f"  All diffs = 1 (as expected for consecutive pixel values)")
    
    print(f"\nMapped adjacent diffs:")
    print(f"  Min diff: {np.abs(mapped_diffs).min():.4f}")
    print(f"  Max diff: {np.abs(mapped_diffs).max():.4f}")
    print(f"  Mean abs diff: {np.abs(mapped_diffs).mean():.4f}")
    
    print("\n" + "="*60)
    print("Key Observations:")
    print("="*60)
    print("1. The mapping disrupts the monotonic increase of pixel values")
    print("2. Adjacent pixel differences are amplified (no longer always 1)")
    print("3. Values are normalized to approximately [-1.28, 1.28]")
    print("4. This converts low-frequency smooth regions to high-frequency")
    print("5. Semantic content is disrupted but pixel correlations are preserved")


def verify_random_mapping_concept():
    print("\n\nVerifying Random Pixel-Level Mapping Concept")
    print("="*60)
    
    print("\nFormula: T_c ~ Uniform(-1, 1)^256 for each channel c")
    print("Purpose: Even more aggressive semantic disruption")
    
    np.random.seed(42)
    
    print("\nGenerating 3 random mapping tables (for 3 RGB channels):")
    print("-"*60)
    
    for channel in range(3):
        mapping = np.random.uniform(-1, 1, 256)
        print(f"\nChannel {channel}:")
        print(f"  First 10 values: {mapping[:10]}")
        print(f"  Range: [{mapping.min():.4f}, {mapping.max():.4f}]")
        print(f"  All values unique: {len(np.unique(mapping)) == 256}")
    
    print("\n" + "="*60)
    print("Key Observations:")
    print("="*60)
    print("1. Each channel gets a different random mapping")
    print("2. Each sample can have different mappings (per-sample randomness)")
    print("3. Values are in [-1, 1] range")
    print("4. Even more aggressive semantic disruption than fixed mapping")
    print("5. Paper shows comparable performance to fixed mapping")


def compare_semantic_disruption():
    print("\n\nComparing Semantic Disruption Methods")
    print("="*60)
    
    print("\nMethods mentioned in the paper:")
    print("1. High-pass filtering - removes low-freq but semantic remains in edges")
    print("2. Patch shuffling - classifiers still learn semantics even with 2x2 patches")
    print("3. NPR (spectrum-based) - residual operations but retains semantic traces")
    print("4. Pixel-level mapping (Ours) - transforms pixel values, disrupts monotonicity")
    
    print("\n" + "="*60)
    print("Why Pixel-Level Mapping Works:")
    print("="*60)
    print("1. Converts low-frequency information to high-frequency")
    print("2. Forces detector to focus on generative artifacts (upsampling patterns, etc.)")
    print("3. Minimal information loss compared to filtering")
    print("4. Preserves pixel correlations while disrupting semantic structure")
    print("5. Simple to implement and computationally efficient")


if __name__ == '__main__':
    verify_fixed_mapping_formula()
    verify_random_mapping_concept()
    compare_semantic_disruption()
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)
