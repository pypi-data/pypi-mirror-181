import polars as pl
import rich
import os

from win32api import GetMonitorInfo, MonitorFromPoint
from typing import List, Tuple, Optional

from rcmdow.core.cmdow import cmdowDF, rawCmdow, cmdowActiveHandle

# left and top value are exceptionally negative for certain programs
# as well as the width and height values which need to be corrected by a % of the screen size

sizeExceptions = {
    "WindowsTerminal": (-7, -6, 0.00846354166666667, 0.0156626506024096),
    "chrome": (0, 0, 0.00846354166666667, 0.0156815440289505),
}
"""A typical entry is a tuple of (left_offset, top_offset, width_multiplicative_ratio, height_multiplicative_ratio).

The left and top offsets are the number of pixels to offset the window from the left and top of the screen.
The width and height multiplicative ratios are the number of pixels to add to the width and height of the window.
"""

def getWorkSpaceSize() -> Tuple[int, int]:
    monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
    wkInfo = monitor_info.get("Work")
    wkWidth, wkHeight = wkInfo[2], wkInfo[3]
    return wkWidth, wkHeight

def check_open(cmdowDF: pl.DataFrame, window: str) -> bool:
    """Checks if a window is open.

    Args:
        window (str): the name of the window to check.

    Returns:
        bool: whether or not the window is open.
    """
    df = cmdowDF
    return len(df.filter(pl.col("Image").str.to_lowercase().str.contains(window))) > 0

def check_all_open(cmdowDF: pl.DataFrame, windows: List[str]) -> bool:
    """Checks if all windows are open.

    This function only works as expected if `cmdowDF` is the DataFrame constructed with `taskbar=True`.
    
    Args:
        windows (List[str]): the names of the windows to check.

    Returns:
        bool: whether or not all windows are open.
    """
    df = cmdowDF
    for window in windows:
        if not len(df.filter(pl.col("Image").str.to_lowercase().str.contains(window))) > 0:
            return False
    return True

def horizontalLayout(
    left_window: str,
    right_window: str,
    open_if_closed: Optional[bool] = False,
    ):
    """Horizontally splits the screen between two windows.

    Args:
        left_window (str): the name of the window to be placed on the left side of the screen.
        right_window (str): the name of the window to be placed on the right side of the screen.
        open_if_closed (bool, optional): whether or not to open the window if it is closed. Defaults to False.
    """
    windows = [left_window, right_window]
    # check if the windows are open
    df = cmdowDF(rawCmdow(taskbar=True))
    if not check_all_open(df, windows):
        if open_if_closed:
            for w in windows:
                if not check_open(df, w):
                    os.system(f"start {w}")
        else:
            raise ValueError(f"One of {windows} are not open. Cannot split screen. Set `open_if_closed` to True to open the windows.")
    else:
        # get the screen size without the taskbar
        width, height = getWorkSpaceSize()

        # get the window handles
        left_handle = df.filter(pl.col("Image").str.to_lowercase().str.contains(left_window.lower())).select("Handle").row(0)[0]
        right_handle = df.filter(pl.col("Image").str.to_lowercase().str.contains(right_window)).select("Handle").row(0)[0]
        left_name = df.filter(pl.col("Image").str.to_lowercase().str.contains(left_window.lower())).select("Image").row(0)[0]
        right_name = df.filter(pl.col("Image").str.to_lowercase().str.contains(right_window)).select("Image").row(0)[0]
        # check for size exceptions
        lw_left = 0 if left_name not in sizeExceptions else sizeExceptions[left_name][0]
        lw_top = 0 if left_name not in sizeExceptions else sizeExceptions[left_name][1]
        lw_width = width//2 if left_name not in sizeExceptions else width//2 + int(width*sizeExceptions[left_name][2])
        lw_height = (
            height if left_name not in sizeExceptions
            else height + int((height - sizeExceptions[left_name][1]) * sizeExceptions[left_name][3])
        )
        rw_left = width//2
        rw_top = 0 if right_name not in sizeExceptions else sizeExceptions[right_name][1]
        rw_width = width//2 if right_name not in sizeExceptions else width//2 + int(width*sizeExceptions[right_name][2])
        rw_height = (
            height if right_name not in sizeExceptions else
            height + int((height - sizeExceptions[right_name][1]) * sizeExceptions[right_name][3])
        )
        # get the current active window
        active_handle = cmdowActiveHandle()
        # move the windows after minimizing all other windows
        os.system("cmdow /ma")
        os.system(f"cmdow {left_handle} /res")
        os.system(f"cmdow {left_handle} /mov {lw_left} {lw_top} /siz {lw_width} {lw_height}")
        os.system(f"cmdow {right_handle} /res")
        os.system(f"cmdow {right_handle} /mov {rw_left} {rw_top} /siz {rw_width} {rw_height}")
        # restore the active window
        os.system(f"cmdow {active_handle} /act")


def verticalLayout(
    upper_window: str,
    lower_window: str,
    open_if_closed: Optional[bool] = False,
    ):
    """Horizontally splits the screen between two windows.

    Args:
        upper_window (str): the name of the window to be placed on the upper side of the screen.
        lower_window (str): the name of the window to be placed on the lower side of the screen.
        open_if_closed (bool, optional): whether or not to open the window if it is closed. Defaults to False.
    """
    windows = [upper_window, lower_window]
    # check if the windows are open
    df = cmdowDF(rawCmdow(taskbar=True))
    if not check_all_open(df, windows):
        if open_if_closed:
            for w in windows:
                if not check_open(df, w):
                    os.system(f"start {w}")
        else:
            raise ValueError(f"One of {windows} are not open. Cannot split screen. Set `open_if_closed` to True to open the windows.")
    else:
        # get the screen size without the taskbar
        width, height = getWorkSpaceSize()

        # get the window handles
        upper_handle = df.filter(pl.col("Image").str.to_lowercase().str.contains(upper_window.lower())).select("Handle").row(0)[0]
        lower_handle = df.filter(pl.col("Image").str.to_lowercase().str.contains(lower_window)).select("Handle").row(0)[0]
        upper_name = df.filter(pl.col("Image").str.to_lowercase().str.contains(upper_window.lower())).select("Image").row(0)[0]
        lower_name = df.filter(pl.col("Image").str.to_lowercase().str.contains(lower_window)).select("Image").row(0)[0]
        # check for size exceptions
        uw_left = 0 if upper_name not in sizeExceptions else sizeExceptions[upper_name][0]
        uw_top = 0 if upper_name not in sizeExceptions else sizeExceptions[upper_name][1]
        uw_width = width
        uw_height = height//2

        lw_left = 0
        lw_top = height//2
        lw_width = width
        lw_height = height//2
        # get the current active window
        active_handle = cmdowActiveHandle()
        # move the windows after minimizing all other windows
        os.system("cmdow /ma")
        os.system(f"cmdow {upper_handle} /res")
        os.system(f"cmdow {upper_handle} /mov {uw_left} {uw_top} /siz {uw_width} {uw_height}")
        os.system(f"cmdow {lower_handle} /res")
        os.system(f"cmdow {lower_handle} /mov {lw_left} {lw_top} /siz {lw_width} {lw_height}")
        # restore the active window
        os.system(f"cmdow {active_handle} /act")


if __name__ == "__main__":
    df = cmdowDF(rawCmdow(taskbar=True))
    rich.print(df)
    