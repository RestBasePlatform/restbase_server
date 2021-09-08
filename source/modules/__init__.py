from exceptions import FunctionNotFound


def function_not_found(*args, **kwargs):
    """"""
    raise FunctionNotFound()


# MODULE TestModule0_3

from modules.TestModule0_3 import create_user as TestModule0_3_user_create

from modules.TestModule0_3 import delete_user as TestModule0_3_user_delete

from modules.TestModule0_3 import read_table_data as TestModule0_3_common_get_table_data

# ENDMODULE TestModule0_3
