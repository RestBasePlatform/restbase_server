import os


MODULES_PATH = "modules" if not os.getenv("TEST") else "./source/modules"
