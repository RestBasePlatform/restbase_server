"""Default setup after running"""
import requests


LATEST_TEST_MODULE_VERSION = ""
platform_url = "http://0.0.0.0:8000/"


requests.post(platform_url + "/v1/submodule/update_module_list??full_update=true")
requests.post(
    platform_url + "/v1/installation/create",
    json={
        "installation_name": "test-5",
        "submodule_name": "TestModule",
        "submodule_version": "0.4",
        "username": "string",
        "password": "string",
        "host": "string",
        "port": "string",
    },
)


a = requests.post(
    platform_url + "v1/user/",
    json={
        "username": "123123",
        "password": "string",
        "comment": "123",
        "group_list": [],
    },
)
print(a.status_code)
