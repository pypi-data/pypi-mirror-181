import urllib.parse
from typing import Any


class Parser:
    def __init__(self):
        self.query_list = {}
        self.default = {}

    def __getattr__(self, name: str):
        if name in self.query_list:
            return self.query_list[name]

        elif name in self.default:
            return self.default[name]

        return None

    def check(self, query: str) -> bool:
        return query in self.query_list

    def add(self, query: str, default: Any = None) -> None:
        self.default[query] = default

    def parse(self, url: str) -> dict:
        split = url.split('?')
        self.query_list = {}

        if len(split) > 1:
            parameters = split[-1].split('&')

            for parameter in parameters:
                split = parameter.split('=', 1)
                name = split[0]
                value = (
                    None
                    if len(split) < 2
                    else urllib.parse.unquote(split[-1])
                )

                if value is None and name in self.default:
                    value = self.default[name]

                self.query_list[name] = value

        for parameter, value in self.default.items():
            if parameter not in self.query_list:
                self.query_list[parameter] = value

        return self.query_list
