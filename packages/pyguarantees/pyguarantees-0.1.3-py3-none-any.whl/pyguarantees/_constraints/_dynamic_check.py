from dataclasses import dataclass


@dataclass
class _DynamicCheck:
    check: callable
    callback: callable = None
    description: str = ""
