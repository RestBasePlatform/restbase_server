from exceptions import FunctionNotFound


def function_not_found(*args, **kwargs):
    """"""
    raise FunctionNotFound()


# MODULE TestModule1_5

from modules.TestModule1_5 import create_user as TestModule1_5_user_create

from modules.TestModule1_5 import delete_user as TestModule1_5_user_delete

# ENDMODULE TestModule1_5

# MODULE TestModule0_1

from modules.TestModule0_1 import create_user as TestModule0_1_user_create

from modules.TestModule0_1 import delete_user as TestModule0_1_user_delete

from modules.TestModule0_1 import read_table_data as TestModule0_1_common_get_table_data

# ENDMODULE TestModule0_1
