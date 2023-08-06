"""Image generation."""

import pathlib

from .config import Config
from .execute_command import execute_command


async def _execute_latex(*, source_filepath: pathlib.Path, config: Config) -> None:
    """Execute latex command.

    Args:
        source_filepath (pathlib.Path): Filepath of the source file.
        config (Config): Configuration.
    """
    command = (
        [config.latex_executable] + config.latex_options + [str(source_filepath.name)]
    )
    cwd = str(source_filepath.parent)
    await execute_command(command, cwd=cwd)


async def _execute_dvipdf(*, source_filepath: pathlib.Path, config: Config) -> None:
    """Execute dvipdf command.

    Args:
        source_filepath (pathlib.Path): Filepath of the source file.
        config (Config): Configuration.
    """
    stem = str(source_filepath.stem)
    command = (
        [config.dvipdf_executable]
        + config.dvipdf_options
        + ["-o", f"{stem}_with_margin.pdf", f"{stem}.dvi"]
    )
    cwd = str(source_filepath.parent)
    await execute_command(command, cwd=cwd)


async def _execute_pdfcrop(*, source_filepath: pathlib.Path, config: Config) -> None:
    """Execute pdfcrop command.

    Args:
        source_filepath (pathlib.Path): Filepath of the source file.
        config (Config): Configuration.
    """
    stem = str(source_filepath.stem)
    command = (
        [config.pdfcrop_executable]
        + config.pdfcrop_options
        + [f"{stem}_with_margin.pdf", f"{stem}.pdf"]
    )
    cwd = str(source_filepath.parent)
    await execute_command(command, cwd=cwd)


async def _execute_pdftocairo(*, source_filepath: pathlib.Path, config: Config) -> None:
    """Execute pdftocairo command.

    Args:
        source_filepath (pathlib.Path): Filepath of the source file.
        config (Config): Configuration.
    """
    stem = str(source_filepath.stem)
    command = (
        [config.pdftocairo_executable, "-png", "-singlefile"]
        + config.pdftocairo_options
        + [f"{stem}.pdf"]
    )
    cwd = str(source_filepath.parent)
    await execute_command(command, cwd=cwd)


async def generate_image(
    source_filepath_str: str, *, config: Config = Config()
) -> None:
    """Generate an image.

    Args:
        source_filepath_str (str): Filepath of the source file.
        config (Config, optional): Configuration. Defaults to Config().
    """
    source_filepath = pathlib.Path(source_filepath_str).absolute()
    await _execute_latex(source_filepath=source_filepath, config=config)
    await _execute_dvipdf(source_filepath=source_filepath, config=config)
    await _execute_pdfcrop(source_filepath=source_filepath, config=config)
    await _execute_pdftocairo(source_filepath=source_filepath, config=config)
