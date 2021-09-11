from exceptions import FunctionNotFound


def function_not_found(*args, **kwargs):
    """"""
    raise FunctionNotFound()

# MODULE TestModule0_4

from modules.TestModule0_4 import create_user as TestModule0_4_user_create

from modules.TestModule0_4 import delete_user as TestModule0_4_user_delete

from modules.TestModule0_4 import read_table_data as TestModule0_4_common_get_table_data

from modules.TestModule0_4 import healt_check as TestModule0_4_common_healtcheck

# ENDMODULE TestModule0_4
