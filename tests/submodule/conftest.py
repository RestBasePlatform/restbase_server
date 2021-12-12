import pytest


@pytest.fixture()
def add_submodule_by_github_url_success_body():
    with open("tests/submodule/static/add_submodule_github_url_body.json") as f:
        return f.read()
