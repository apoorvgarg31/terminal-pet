"""
terminal-pet: A tamagotchi that lives in your terminal and feeds on your git commits 🐣
"""

__version__ = "0.1.0"
__author__ = "Apoorv Garg"

from .pet import Pet, PetState, PetType
from .tracker import GitTracker

__all__ = ["Pet", "PetState", "PetType", "GitTracker"]
