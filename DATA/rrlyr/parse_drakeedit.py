#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Jacan Chaplais, 2022 (MIT License)
# EDITED FOR DRAKE
import sys
from pathlib import Path
from operator import methodcaller
from typing import Iterable, Union, List, Optional
from collections import OrderedDict, namedtuple

import click
import pandas as pd

str_ = methodcaller("decode")  # converts bytestring into regular string
RowElement = namedtuple("RowElement", ["slice", "dtype"])
SCHEMA = OrderedDict({  # byte regions and data types for each field
        "CSS_ID": RowElement(slice(0, 10), dtype=str_),
        "RAdeg": RowElement(slice(22, 30), dtype=float),
        "DEdeg": RowElement(slice(32, 40), dtype=float),
#        "VType": RowElement(slice(42, 56), dtype=str_),
#        "SpType": RowElement(slice(57, 75), dtype=str_),
#        "f": RowElement(slice(76, 84), dtype=str_),
#        "M0": RowElement(slice(85, 98), dtype=str_),
#        "l_dT": RowElement(slice(99, 100), dtype=str_),
#        "dT": RowElement(slice(100, 106), dtype=str_),
#        "VSX": RowElement(slice(107, 135), dtype=str_),
#        "VSXType": RowElement(slice(136, 149), dtype=str_),
#        "Blend": RowElement(slice(150, 159), dtype=str_),
#        "N": RowElement(slice(160, 162), dtype=str_),
        })


def rows_from_file(path: Union[str, Path]) -> Iterable[Iterable[bytes]]:
    """Creates a generator which provides each row of data as an
    iterable of each element, as bytestrings.
    
    Parameters
    ----------
    path : str, pathlib.Path
        The location of the data file.
    Yields
    ------
    row : iterable[bytes]
        Provides an iterable over the data row, where each element is
        a bytestring.
    """
    slices = tuple(val.slice for val in SCHEMA.values())
    with open(path, "rb") as f:
        for line in f:  # each line is bytestring
            row_elems = map(line.__getitem__, slices)  # slice bytes per schema
            row_elems = map(methodcaller("strip"), row_elems)  # strip spaces
            yield row_elems  # yield result as next value from this generator


def dict_from_rows(
    data_rows: Iterable[Iterable[bytes]]
) -> OrderedDict[str, Union[List[Optional[float]], List[Optional[str]]]]:
    """Instantiates a ``collections.OrderedDict`` from the iterable  of
    row byte data produced by ``parse_file()``.
    Parameters
    ----------
    data_rows : generator[iterable[bytes]]
        Generator of successive rows of data, in byte format.
    Returns
    -------
    data : collections.OrderedDict
        Ordered dictionary matching the schema, and populated by the
        data from the iterator over the provided file.
    Notes
    -----
    Uses the global ``SCHEMA``, and ``ROW_FORMAT`` constants. If there
    is a change to the format, these must be altered.
    If fields are missing, they are replaced with ``None`` by this
    function.
    """
    data = OrderedDict({key: [] for key in SCHEMA.keys()})
    dtypes = tuple(val.dtype for val in SCHEMA.values())
    cols = tuple(data.values())
    for row in data_rows:
        for elem, dtype, col in zip(row, dtypes, cols):
            col.append(dtype(elem) if elem else None)
    return data


def df_from_file(path: Union[str, Path]) -> pd.DataFrame:
    """Instantiates a pandas DataFrame from a data file which follows
    the layout in ``SCHEMA``, where each field is mapped to a column.
    Parameters
    ----------
    path : str, pathlib.Path
        The location of the data file.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame populated with the contents of the file at ``path``.
    """
    return pd.DataFrame(dict_from_rows(rows_from_file(path)))


@click.command()
@click.argument(
        "path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def main(path: Path) -> None:
    """Prints a DataFrame populated from the data file at PATH."""
    df = df_from_file(path)
    click.echo(df)


if __name__ == "__main__":
    sys.exit(main())
