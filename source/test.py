from inspect import getmembers
from inspect import isfunction


print(getattr(__import__("modules"), "foo")())
