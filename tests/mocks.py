import json


def submodule_request_mock(url: str, request_type: str):
    get_url_response_path_dict = {
        "https://api.github.com/orgs/RestBasePlatform/repos": "tests/submodule/static/get_repos_list.json",
        "https://api.github.com/repos/RestBaseApi/TestModule/releases": "tests/submodule/static/test_module_get_request.json",  # noqa: E501
    }

    if request_type == "get":
        with open(get_url_response_path_dict[url]) as f:
            return json.load(f)
