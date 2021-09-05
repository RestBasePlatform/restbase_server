from .sqlite_credentials import SQLiteController


def get_credentials_controller():
    return SQLiteController()
