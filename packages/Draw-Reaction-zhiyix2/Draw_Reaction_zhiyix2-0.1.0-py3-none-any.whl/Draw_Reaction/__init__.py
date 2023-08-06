# __init__.py

from importlib import resources
try:
    import tkinter
except ModuleNotFoundError:
    import tomli as tomllib

# Version of the Draw_Reaction package
__version__ = "0.1.0"

_cfg = tomllib.loads(resources.read_text("reader", "config.toml"))
URL = _cfg["feed"]["url"]