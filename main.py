import os
import sys
from src import engine

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

# This file is the entry point to start the game
if __name__ == "__main__":
    engine.run()
 