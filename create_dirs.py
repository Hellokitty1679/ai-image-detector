import os

dirs = [
    'data/train/real',
    'data/train/fake',
    'data/test/real',
    'data/test/fake',
]

for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created: {d}")
    else:
        print(f"Exists: {d}")

print("\nDirectory structure created successfully!")
