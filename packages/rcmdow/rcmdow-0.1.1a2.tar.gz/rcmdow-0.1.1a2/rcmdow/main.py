import polars as pl
import signal
import typer
import rich

from typing import Optional, Any

from rcmdow.core.display.plconfig import defaultConfig
from rcmdow.core.cmdow import rawCmdow, cmdowDF, cmdowLayout
from rcmdow.core.winresize import horizontalLayout, verticalLayout

console = rich.console.Console(record=True, force_interactive=True)

app = typer.Typer()

# def onresize(data: Any, console: rich.console.Console):
#     def handler(signum, frame):
#         console.print(data)
#     return signal.signal(signal.SIGWINCH, handler)

@app.command()
def raw():
    """Prints the raw output of cmdow's /p flag. Nothing fancy here."""
    rich.print(rawCmdow())

@app.command()
def ls(
    numrows: Optional[int] = typer.Argument(
        default = None,
        help="The maximum number of rows to display. Defaults to all rows."
        ),
    numcols: Optional[int] = typer.Argument(
        None,
        help="The maximum number of columns to display. Defaults to all columns."
        ),
    expr: Optional[str] = typer.Argument(
        None,
        help="A string to filter the DataFrame by. Defaults to None. See `rcmdow.core.cmdow.cmdowDF` for more information."
        ),
    ):
    """Rich equivalent of `cmdow /p` with optional filtering.

    Args:
        numrows (Optional[int], optional): The maximum number of rows to display. Defaults to all rows.
        numcols (Optional[int], optional): The maximum number of columns to display. Defaults to all columns.
        expr (Optional[str], optional): A string to filter the DataFrame by. Defaults to None. See `rcmdow.core.cmdow.cmdowDF` for more information.
    """
    
    df = cmdowDF(rawCmdow(), expr)
    # onresize(df, console)

    plcfg = defaultConfig(df, console.size, numrows)
    if numcols:
        plcfg.set_tbl_cols(numcols)

    console.print(df, overflow="ellipsis")

@app.command()
def lst(
    numcols: Optional[int] = typer.Argument(
        None,
        help="The maximum number of columns to display. Defaults to all columns."
        ),
    ):
    """Rich equivalent of `cmdow /p /t` with optional filtering.

    Args:
        numcols (Optional[int], optional): The maximum number of columns to display. Defaults to all columns.
    """
    df = cmdowDF(rawCmdow(taskbar=True))

    plcfg = defaultConfig(df, console.size)
    if numcols:
        plcfg.set_tbl_cols(numcols)

    console.print(df, overflow="ellipsis")

@app.command()
def layout(
    showtaskbar: bool = typer.Option(
        False,
        "--taskbar",
        "-t",
        help="Show the taskbar in the layout. Defaults to False."
        ),
    ):
    """Prints the current layout of the desktop.
    
    This is done by getting the current window list and filtering out the
    windows that are not visible (conditions: Left < 0 and Top < 0).
    """
    df = cmdowLayout(showtaskbar=showtaskbar)
    plcfg = defaultConfig(df, console.size)
    console.print(df, overflow="ellipsis")

@app.command()
def hzl(
    left_window: str = typer.Argument(..., help="The window you want to snap to the left of the screen."),
    right_window: str = typer.Argument(..., help="The window you want to snap to the right of the screen."),
    open_if_closed: Optional[bool] = typer.Option(
        False,
        "--open",
        "-o",
        help="Open the window if it is not currently open. Defaults to False."
        )
    ):
    """Snap two chosen windows horizontally.

    Args:
        left_window (str): The window you want to snap to the left of the screen.
        right_window (str): The window you want to snap to the right of the screen.
        open_if_closed (Optional[bool], optional): Open the window if it is not currently open. Defaults to False.
    """
    horizontalLayout(left_window, right_window, open_if_closed)

@app.command()
def vtl(
    upper_window: str = typer.Argument(..., help="The window you want to snap to the upper half of the screen."),
    lower_window: str = typer.Argument(..., help="The window you want to snap to the lower half of the screen."),
    open_if_closed: Optional[bool] = typer.Option(
        False,
        "--open",
        "-o",
        help="Open the window if it is not currently open. Defaults to False."
        )
    ):
    """Snap two chosen windows vertically.

    Args:
        upper_window (str): The window you want to snap to the upper half of the screen.
        lower_window (str): The window you want to snap to the lower half of the screen.
        open_if_closed (Optional[bool], optional): Open the window if it is not currently open. Defaults to False.
    """
    verticalLayout(upper_window, lower_window, open_if_closed)

