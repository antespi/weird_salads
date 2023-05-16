# Add this project in the module search path
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import *
from dependencies import *
from main import *
