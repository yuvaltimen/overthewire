from json import dumps

from typing_extensions import Any


def pprint(obj: Any) -> None:
    print(dumps(obj, indent=2))
    