import os
import sys

PYTHON_PATH = sys.executable
file_path = os.path.join(sys.path[0], 'server.py')
os.system(f"{PYTHON_PATH} {file_path}")
