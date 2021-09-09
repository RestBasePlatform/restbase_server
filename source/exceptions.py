class InstallationNotFound(Exception):
    def __init__(self, name):
        super().__init__(f"Installation with name '{name}' not found")


class SubmoduleNotFound(Exception):
    def __init__(self, _id: str):
        super().__init__(f"Submodule with id '{_id}' not found")


class FunctionNotFound(Exception):
    def __init__(self):
        super().__init__()


class AlreadyExistsError(Exception):
    def __init__(self, entity: str, name: str):
        super().__init__(f"Entity: '{entity}' with name '{name}' already exists.")


class GroupNotFoundError(Exception):
    def __init__(self, identifier: str, identifier_value: str):
        super().__init__(f"Group with '{identifier}'='{identifier_value}' not found.")


class UserNotFoundError(Exception):
    def __init__(self, identifier: str, identifier_value: int):
        super().__init__(f"User with '{identifier}'='{identifier_value}' not found.")
