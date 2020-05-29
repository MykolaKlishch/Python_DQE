"""Read 'HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv' file
from a specified path. Calculate percentage of available hospital
beds for all HRR. Display these percentages for a specified number
of HRR where the percentages are the highest.
"""

import argparse
import os
import pandas as pd
from typing import Tuple

FILENAME = "HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv"


def valid_directory(directory: str) -> str:
    """Used for validation of the command line argument -path
    The function is passed as a value for 'type' parameter
    in ArgumentParser.add_argument() method.

    :param directory: -path value
    :raise ArgumentTypeError: if validation fails
    """
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(
            f"'{directory}' is not a name of an existing directory")
    if not os.path.isfile(os.path.join(directory, FILENAME)):
        raise argparse.ArgumentTypeError(
            f"'{directory}' doesn't contain the required file")
    return directory


def get_args_from_cmd() -> Tuple[str, int]:
    """Get file path and number of records from command line.

    :return: file path, number of records to display
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-path", type=valid_directory, default=os.getcwd(),
                        help="a directory with .csv file to be opened")
    parser.add_argument("-bed", type=int, default=5,
                        help="number or HRR to be displayed")
    args = parser.parse_args()
    return args.path, args.bed


if __name__ == "__main__":
    path, number = get_args_from_cmd()
    file_path = os.path.join(path, FILENAME)
    df = pd.read_csv(
        filepath_or_buffer=file_path,
        skiprows=lambda index: index == 1,
        usecols=["HRR", "Available Hospital Beds", "Total Hospital Beds"],
        thousands=","
    )
    df["%"] = df["Available Hospital Beds"] / df["Total Hospital Beds"]
    df = df[["HRR", "%"]].sort_values(by="%", ascending=False).head(number)
    df["%"] = df["%"].map("{:3.1%}".format)
    print(df.to_string(index=False, header=False))
