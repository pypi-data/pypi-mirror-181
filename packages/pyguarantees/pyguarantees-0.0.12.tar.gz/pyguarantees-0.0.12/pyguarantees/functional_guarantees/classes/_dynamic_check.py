from dataclasses import dataclass


@dataclass
class DynamicCheck:
    check: callable
    callback: callable = None
    description: str = ""
