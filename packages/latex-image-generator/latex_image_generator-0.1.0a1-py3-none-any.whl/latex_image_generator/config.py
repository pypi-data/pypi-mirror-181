"""Configuration of this tool."""

import copy
import dataclasses
import typing

DEFAULT_LATEX_OPTIONS = [
    "-halt-on-error",
    "-file-line-error",
]  #: Default options of latex command.


DEFAULT_PDFTOCAIRO_OPTIONS = [
    "-transp",
    "-r",
    "1500",
]


@dataclasses.dataclass
class Config:
    """Class of configurations."""

    latex_executable: str = "platex"  #: Path of latex command.
    latex_options: typing.List[str] = dataclasses.field(
        default_factory=lambda: copy.deepcopy(DEFAULT_LATEX_OPTIONS)
    )  #: Options of latex command. Default value is :py:data:`DEFAULT_LATEX_OPTIONS`.

    dvipdf_executable: str = "dvipdfmx"  #: Path of dvipdf command.
    dvipdf_options: typing.List[str] = dataclasses.field(
        default_factory=list
    )  #: Options for dvipdf command. Default value is ``[]``.

    pdfcrop_executable: str = "pdfcrop"  #: Path of pdfcrop command.
    pdfcrop_options: typing.List[str] = dataclasses.field(
        default_factory=list
    )  #: Options for pdfcrop command. Default value is ``[]``.

    pdftocairo_executable: str = "pdftocairo"  #: Path of pdftocairo command.
    pdftocairo_options: typing.List[str] = dataclasses.field(
        default_factory=lambda: copy.deepcopy(DEFAULT_PDFTOCAIRO_OPTIONS)
    )  #: Options for pdftocairo command. Default value if :py:data:`DEFAULT_PDFTOCAIRO_OPTIONS`.
