import re

from InquirerPy.base.control import Choice
from InquirerPy.prompts.input import InputPrompt
from InquirerPy.prompts.list import ListPrompt

from yapygen.meta.meta import Meta

name = InputPrompt(
    message="Project name:",
    default="demo",
    validate=lambda x: re.match(
        r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", x, re.IGNORECASE
    )
    is not None,
    transformer=lambda x: re.sub(r"[-_.]+", "-", x).lower(),
    filter=lambda x: re.sub(r"[-_.]+", "-", x).lower(),
    long_instruction=" A valid name consists only of "
    "ASCII letters and numbers, "
    "period, underscore and hyphen. "
    "It must start and end with a letter or number.",
)

description = InputPrompt(
    message="Project description:", default="a simple python project"
)

min_py = ListPrompt(
    message="minimum python version:",
    choices=["3.7", "3.8", "3.9", "3.10"],
    default="3.9",
)

license = ListPrompt(
    message="license:",
    choices=[
        Choice("MIT", name="MIT License"),
        Choice("GPLv3", name="GNU GPLv3"),
        Choice("LGPLv3", name="GNU LGPLv3"),
        Choice("Mozilla", name="Mozilla Public License 2.0"),
        Choice("Apache", name="Apache License 2.0"),
    ],
    default=Choice("MIT", name="MIT License"),
)

author_name = InputPrompt(message="Author name:", default="Author Placeholder")

author_email = InputPrompt(
    message="Author email:", default="email@placeholder.com"
)

package = InputPrompt(
    message="Top level package name:",
    default="demo",
    validate=lambda x: re.match(
        r"^([A-Z]|[A-Z][A-Z_]*[A-Z])$", x, re.IGNORECASE
    )
    is not None,
)


def get_meta() -> Meta:
    return Meta(
        name=name.execute(),
        description=description.execute(),
        minimum_python=min_py.execute(),
        license=license.execute(),
        author_name=author_name.execute(),
        author_email=author_email.execute(),
        package=package.execute(),
    )
