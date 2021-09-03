class InstallationNotFound(Exception):
    def __init__(self, name):
        super(InstallationNotFound, self).__init__(f"Installation with name '{name}' not found")


class SubmoduleNotFound(Exception):
    def __init__(self, _id: str):
        super(SubmoduleNotFound, self).__init__(f"Submodule with id '{_id}' not found")
