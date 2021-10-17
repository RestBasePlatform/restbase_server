import json
from typing import Union


def load_static_json(json_path: str, convert_to_dict: bool = True) -> Union[dict, str]:
    with open(json_path) as f:
        return json.load(f) if convert_to_dict else f.read()
