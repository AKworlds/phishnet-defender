import os

model_dir = "models"
print("🔍 Files in models/:")
for f in sorted(os.listdir(model_dir)):
    print(" -", f)
