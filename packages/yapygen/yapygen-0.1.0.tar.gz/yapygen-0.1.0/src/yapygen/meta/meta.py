from typing import Literal, NamedTuple


class Meta(NamedTuple):
    name: str
    description: str
    minimum_python: Literal["3.7", "3.8", "3.9", "3.10"]
    license: Literal["MIT", "GPLv3", "LGPLv3", "Mozilla", "Apache"]
    author_name: str
    author_email: str
    package: str

    @property
    def license_name(self) -> Literal["LICENSE", "COPYING", "COPYING.LESSER"]:
        if self.license == "GPLv3":
            return "COPYING"
        elif self.license == "LGPLv3":
            return "COPYING.LESSER"
        else:
            return "LICENSE"
