from exceptions import FunctionNotFound


def function_not_found(*args, **kwargs):
    """"""
    raise FunctionNotFound("Func")


# MODULE TestModule1_5

from modules.TestModule1_5 import create_user as TestModule1_5_user_create

from modules.TestModule1_5 import delete_user as TestModule1_5_user_delete

# ENDMODULE TestModule1_5
