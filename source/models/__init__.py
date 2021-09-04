from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .sublodules import *
from .secrets import *

__all__ = ["Submodule", "Installation", "Secrets"]

