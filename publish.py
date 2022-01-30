"""
This file is used to automatically publish the project on PiPy
"""


import sys
import subprocess


subprocess.check_call([sys.executable, "setup.py", "bdist_wheel"])

subprocess.check_call([sys.executable, "-m", "pip", "install", "twine"])

subprocess.check_call([sys.executable, "-m", "twine", "upload", "dist/*"])