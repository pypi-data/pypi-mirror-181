from importlib.resources import files
from string import Template

from yapygen.meta import Meta


def load_template(name: str) -> Template:
    root = files("yapygen.gen").joinpath("templates")
    content = root.joinpath(name).read_text(encoding="utf-8")
    return Template(content)


def render(name: str, meta: Meta, /, **kwargs: str) -> str:
    param = meta._asdict()
    param.update(kwargs)
    return load_template(name).safe_substitute(param)
