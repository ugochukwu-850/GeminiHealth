"""Gemini's custom command line utility for tailored admin task"""
import os
import sys
import pathlib
from api.utils import populate_ingredients

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gemini.settings')
    if len(sys.argv) < 2:
        print("Usage: python controls.py [COMMAND]  [COMMAND VARIABLES]")
    
    COMMAND = sys.argv[1]
   
    
    if COMMAND == "ing":
        populate_ingredients()
        sys.exit(1)
    sys.exit(2)

if __name__ == '__main__':
    main()
