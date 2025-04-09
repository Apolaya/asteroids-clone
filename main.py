import os
import sys
from src import engine


"""Create temporary directory for build script."""
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

"""This file is the entry point to run the game engine."""
if __name__ == "__main__":
    engine.run()
 