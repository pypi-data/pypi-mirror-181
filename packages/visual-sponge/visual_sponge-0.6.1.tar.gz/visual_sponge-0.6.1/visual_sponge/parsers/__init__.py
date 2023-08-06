from pathlib import Path
from importlib import import_module

__all__ = ["Parser"]

class Parser():
    formats = {}
    def __init_subclass__(cls, formats):
        if isinstance(formats, str):
            Parser.formats[formats] = cls
        else:
            Parser.formats.update({}.fromkeys(formats, cls))

    def __new__(cls, format_):
        return cls.formats[format_]

for file in Path(__file__).parent.rglob("*.py"):
    module_name = file.stem
    if module_name != "__init__":
        module = import_module(f"{__name__}.{module_name}")
