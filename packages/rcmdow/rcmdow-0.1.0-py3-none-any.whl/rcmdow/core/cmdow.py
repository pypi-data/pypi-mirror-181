import re
import rich
import psutil
import subprocess
import polars as pl
import tkinter as tk

from typing import List, Union, Dict, Optional, Any, Tuple

def autocast(value: str) -> Union[str, int, float]:
    """Attempts to cast a string to an int or float, and returns the original
    value if neither of those casts work.
    """
    intptrn = r"^-?\d+$"
    floatptrn = r"^-?\d+\.\d+$"
    if re.match(intptrn, value):
        return int(value)
    elif re.match(floatptrn, value):
        return float(value)
    else:
        return value

def getProcessListByName(name: str, info_cols: List[str] = ["pid", "name"]) -> list:
    """Returns a list of processes that match the given name.
    
    You can specify OR conditions by separating the names with a pipe (|).
    You can specify AND conditions by separating the names with an ampersand (&).
    
    Either OR or AND conditions can be used, but not both in the same name.
    """
    if "|" in name:
        name = name.split("|")
        condition = lambda proc: any([n.lower() in proc.info["name"].lower() for n in name])
    elif "&" in name:
        name = name.split("&")
        condition = lambda proc: all([n.lower() in proc.info["name"].lower() for n in name])
    else:
        condition = lambda proc: name.lower() in proc.info["name"].lower()

    return list(
        filter(
            condition,
            psutil.process_iter(["pid", "name"])
            )
        )

def cmdowHeader(raw: str) -> Dict[str,List[str]]:
    """Certain columns contain multiple words, which are separated by a space.
    This function does three things:
    1. It replaces the space with a hyphen in the column name.
    2. It returns a list of the column names.
    3. It returns a list of the column names that contain multiple words.

    Args:
        raw (str): the raw string from the first line of cmdow's  /p flag output

    Returns:
        Dict[str,List[str]]: a dictionary with two keys: "columns" and "multicolumns"
            - "columns" is a list of the column names
            - "multicolumns" is a list of the column names that contain multiple words
    """
    _multicolumns = re.findall(r"-([ \w]+)-", raw)
    # "Caption" is a special case because it is the only column that contains
    # special characters, such as : and /.
    specials = ["Caption"]
    multicolumns = []
    for _col in _multicolumns:
        col = _col.replace(" ", "-")
        raw = raw.replace(f"-{_col}-", col)
        multicolumns += [col]
    cols = re.sub("[ ]+", " ", raw).split(" ")
    return {
        "columns": cols,
        "multicolumns": multicolumns,
        "specials": specials,
    }

def cmdowRowFmt(raw: Union[str, Dict[str,List[str]]]) -> str:
    """
    Takes the first line of cmdow's /p flag output and creates a regex pattern
    to match the remaining lines and create rows despite multi-value columns.
    """
    if isinstance(raw, str):
        coldata = cmdowHeader(raw)
        multicolumns = coldata["multicolumns"]
        columns = coldata["columns"]
        specials = coldata["specials"]
    elif isinstance(raw, dict):
        multicolumns = raw["multicolumns"]
        columns = raw["columns"]
        specials = raw["specials"]
    else:
        raise TypeError(f"raw must be a string or a dictionary, not {type(raw)}")
    
    pattern = r""

    for col in columns:
        end = r" " if col != columns[-1] else r""
        if col in multicolumns:
            pattern += r"([a-zA-Z ]+)" + end
        elif col in specials:
            pattern += r"([ \w\:\.\'\[\]\\\/\-]+)" + end
        else:
            if col != columns[-1]:
                pattern += r"(.+?)" + end
            else:
                pattern += r"(#?[\d\w]+)" + end
    return pattern

def cmdowRow(raw: str, pattern: str) -> List[str]:
    row = re.sub(r"[ ]+", " ", raw)
    try:
        prow = re.findall(pattern, row).pop()
    except IndexError:
        raise IndexError(f"Could not find a match for the pattern {pattern} in the row {row} from cmdow's /p flag output.")
    prow = [autocast(v) for v in prow]
    return [prow]

def cmdowRows(raw_rows: List[str], pattern: str) -> List[List[str]]:
    rows = []
    for row in raw_rows:
        rows += cmdowRow(row, pattern)
    return rows

def cmdowRawDF(raw: str) -> pl.DataFrame:
    """
    The raw DataFrame is the DataFrame that is created from the raw output
    of cmdow's /p flag. It is not cleaned up or formatted in any way, except
    for the removal of extra spaces and the addition of hypens to multi-word
    column names.

    Args:
        raw (str): the raw output of cmdow's /p flag
            can be obtained by running `subprocess.run(["cmdow", "/p" "/f"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True).stdout`
            runing `rcmdow raw` or calling `rcmdow.core.cmdow.rawCmdow()`

    Returns:
        pl.DataFrame: the raw DataFrame
    """
    rows = raw.splitlines()
    columns, rows = rows[0], rows[1:]
    columns = cmdowHeader(columns)
    pattern = cmdowRowFmt(columns)
    rows = cmdowRows(rows, pattern)

    return pl.DataFrame(rows, columns=columns["columns"])

def cmdowDF(raw: str, expr: Optional[str] = None) -> pl.DataFrame:
    """cmdowDF is the main function for creating a DataFrame from the raw output of cmdow's /p flag.

    Adds a way to filter the DataFrame by process name.

    Args:
        raw (str): the raw output of cmdow's /p flag
            can be obtained by running `subprocess.run(["cmdow", "/p"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True).stdout`
            runing `rcmdow raw` or calling `rcmdow.core.cmdow.rawCmdow()`
        
        expr (Optional[str], optional): a string to filter the DataFrame by. Defaults to None.
            You can specify OR conditions by separating the names with a pipe (|).
            You can specify AND conditions by separating the names with an ampersand (&).
            Either OR or AND conditions can be used, but not both in the same name.

    Returns:
        pl.DataFrame: the DataFrame with the truncated process names recovered
    """
    rawDf = cmdowRawDF(raw)
    if expr:
        strfilter = expr
    else:
        return rawDf
    
    # inefficient, but no time to optimize right now
    processes = list(
        map(
            lambda proc: [str(proc.info["pid"]), proc.info["name"]],
            getProcessListByName(strfilter)
        )
    )

    procDf = pl.DataFrame(processes, columns=["Pid", "FullName"])

    df = rawDf.join(procDf, on="Pid")

    return df


def rawCmdow(taskbar: Optional[bool] = False) -> str:
    """Returns the raw output of cmdow's /p flag.

    Args:
        taskbar (bool, optional): whether or not to include the taskbar in the output. Defaults to False.
    
    Returns:
        str: the raw output of cmdow's /p flag
    """
    cmd = ["cmdow", "/p", "/f", "/t"] if taskbar else ["cmdow", "/f", "/p"]
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True).stdout

def cmdowActive(
    showtaskbar: Optional[bool] = False
    ) -> pl.DataFrame:
    """Returns a DataFrame with the layout of the currently active window.

    Args:
        showtaskbar (bool, optional): whether or not to include the taskbar in the output. Defaults to False.

    Returns:
        pl.DataFrame: the DataFrame with the layout of the windows on the screen.
    """
    df = cmdowDF(rawCmdow(taskbar=True))
    df = df.filter(pl.col("Window-status").str.contains("^[a-zA-Z]{3} Act").alias("regex"))
    if not showtaskbar:
        df = df.filter(pl.col("Image") != "SystemSettings")
    return df

def cmdowActiveName() -> str:
    """Returns the name of the currently active window.

    Returns:
        str: the name of the currently active window.
    """
    return cmdowActive().select("Image").row(0)[0]

def cmdowActiveHandle() -> str:
    """Returns the handle of the currently active window.

    Returns:
        str: the name of the currently active window.
    """
    return cmdowActive().select("Handle").row(0)[0]

def screenSize() -> Tuple[int, int]:
    """Returns the size of the screen in pixels.

    Returns:
        Tuple[int, int]: the width and height of the screen in pixels.
    """
    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()

def cmdowLayout(
    showtaskbar: Optional[bool] = False
    ) -> pl.DataFrame:
    """Returns a DataFrame with the layout of the currently active window.

    Args:
        showtaskbar (bool, optional): whether or not to include the taskbar in the output. Defaults to False.

    Returns:
        pl.DataFrame: the DataFrame with the layout of the windows on the screen.
    """
    df = cmdowDF(rawCmdow(taskbar=True))
    # get the maximum width and height of the screen
    maxWidth, mawHeight = screenSize()
    # if the window is maximized but not active, it is in the background
    # and we don't want to include it in the layout
    df = df.filter(
        (
            ( ~pl.col("Window-status").str.contains("^[a-zA-Z]{3} Act") )
            & ( pl.col("Width") < maxWidth ) & ( pl.col("Height") < mawHeight )
        ) | pl.col("Window-status").str.contains("^[a-zA-Z]{3} Act")
    )
    if not showtaskbar:
        df = df.filter(pl.col("Image") != "SystemSettings")
    return df


# Compare this snippet from core\cmdow.py:
if __name__ == "__main__":
    raw = rawCmdow()
    df = cmdowDF(raw)
    rich.print(df)
    
    # proc = getProcessByName("windowsterminal")
    # rich.print(proc)