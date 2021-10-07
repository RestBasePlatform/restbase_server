from models.server import ServerCredentials


def present_server_credential_data(obj: ServerCredentials) -> dict:
    return {
        "id": obj.id,
        "username": obj.username,
        "password": "***" if obj.password else "No password",
        "ssh_key": "***" if obj.ssh_key else "Not defined",
    }
