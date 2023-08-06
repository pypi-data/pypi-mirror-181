"""Command execution."""


import asyncio
import logging
import typing

LOGGER = logging.getLogger(__name__)


async def execute_command(
    command: typing.List[str],
    *,
    cwd: str = ".",
    cancel_timeout: float = 5.0,
) -> str:
    """Execute a command.

    Args:
        command (typing.List[str]): Command.
        cwd (str): Working directory.
        cancel_timeout (float): Timeout of cancellation of execution.

    Returns:
        str: Console output of the command.
    """
    LOGGER.debug("Execute command %s.", command)

    process = await asyncio.create_subprocess_exec(
        *command,
        stdin=None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=cwd,
    )

    try:
        output_bytes, _ = await process.communicate()
    except asyncio.CancelledError:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=cancel_timeout)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
        raise

    output = output_bytes.decode(encoding="utf8", errors="backslashreplace")
    exit_code = process.returncode
    assert exit_code is not None
    if exit_code != 0:
        message = f"Command {command} exited with code {exit_code}.\nOutput:\n{output}"
        LOGGER.error(message)
        raise RuntimeError(message)

    LOGGER.debug("Command %s finished successfully.\nOutput:\n%s", command, output)

    return output
