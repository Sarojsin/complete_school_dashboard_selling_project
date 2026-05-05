import importlib
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load backup models
backup_models = importlib.import_module('backup.models.college')

# Get all model classes
model_classes = []
for name in dir(backup_models):
    obj = getattr(backup_models, name)
    if hasattr(obj, '__tablename__') and hasattr(obj, '__table__'):
        model_classes.append((name, obj))

print("Backup model table names:")
for cls_name, cls in sorted(model_classes, key=lambda x: x[1].__tablename__):
    print(f"  {cls_name} -> {cls.__tablename__}")
