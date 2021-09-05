from .sqlite_credentials import SQLiteController


def get_credentials_controller():
    return SQLiteController()


__all__ = ["get_credentials_controller", "SQLiteController"]
