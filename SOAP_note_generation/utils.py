import sys
import os

def set_project_root():
    root_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
    if root_path not in sys.path:
        sys.path.insert(0, root_path)