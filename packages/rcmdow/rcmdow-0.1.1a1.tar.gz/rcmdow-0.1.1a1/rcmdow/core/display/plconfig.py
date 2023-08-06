import polars as pl
from typing import Tuple, List, Optional

def guessDfSize(df: pl.DataFrame) -> tuple:
    """Guesses the size of a DataFrame by counting the number of lines and the
    maximum number of characters in a line.
    
    Args:
        df (pl.DataFrame): the DataFrame to guess the size of
    
    Returns:
        tuple: a tuple containing the width and height of the DataFrame
    """
    dfrep = str(df)
    cheight = dfrep.count("\n")
    cwidth = max([len(row) for row in dfrep.splitlines()[:10]])
    return (cwidth, cheight)

def smartConfig(df: pl.DataFrame, console_size: Tuple[int]) -> pl.Config:
    """Returns a Config object with the correct number of rows and columns
    set.
    
    Args:
        df (pl.DataFrame): the DataFrame to guess the size of
        numrows (int): the number of rows to set
        numcols (int): the number of columns to set
    
    Returns:
        pl.Config: a Config object with the correct number of rows and columns
        set
    """
    console_width, console_height = console_size
    df_width, df_height = guessDfSize(df)
    
    plcfg = pl.Config()

    if not df_width > console_width:
        plcfg.set_tbl_cols(-1)

    return plcfg

def defaultConfig(
    df: pl.DataFrame,
    console_size: Tuple[int],
    numrows: Optional[int] = None,
    ) -> pl.Config:
    """Returns a Config object with the correct number of rows and columns
    set.
    
    Args:
        df (pl.DataFrame): the DataFrame to guess the size of
        numrows (int): the number of rows to set
        
    Returns:
        pl.Config: a Config object with the correct number of rows and columns
        set
    """
    if numrows is None:
        numrows = -1
    plcfg = smartConfig(df, console_size)
    plcfg.set_tbl_rows(numrows)
    plfcfg = plcfg.set_tbl_hide_dataframe_shape(True)
    plfcfg.set_tbl_column_data_type_inline(True)

    return plcfg