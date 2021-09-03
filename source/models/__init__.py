from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .sublodules import *

__all__ = ["Submodule", "Installation"]

