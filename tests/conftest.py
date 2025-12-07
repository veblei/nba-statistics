import sys
from pathlib import Path

my_dir = Path(__file__).parent.parent.absolute()

# Ensure this dir is on sys.path
sys.path.insert(0, str(my_dir))