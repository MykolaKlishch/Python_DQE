"""Read 'HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv' file
from a specified path. Calculate percentage of available hospital
beds for all HRR. Display these percentages for a specified number
of HRR where the percentages are the highest.
"""

import argparse
import csv
import os
from typing import List, Tuple, Mapping

FILENAME = "HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv"


def get_args_from_cmd() -> Tuple[str, int]:
    """Get the path and number of records from command line.

    :return: path, number of records to display
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-path", type=valid_directory, default=os.getcwd(),
                        help="a directory with .csv file to be opened")
    parser.add_argument("-bed", type=int, default=5,
                        help="number or HRR to be displayed")
    args = parser.parse_args()
    return args.path, args.bed


def valid_directory(directory: str) -> str:
    """Used for validation of the command line argument -path

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


def transform_record(raw_record: Mapping[str, str]) -> Tuple[str, float]:
    """Take values from only three necessary fields
    from a raw record. Transform the values and
    calculate the fraction of available hospital beds.

    :param raw_record: a full row from the table
    :return: HRR, fraction of available beds
    """
    return (raw_record["HRR"],
            float(raw_record["Available Hospital Beds"].replace(",", ""))
            / float(raw_record["Total Hospital Beds"].replace(",", "")))


if __name__ == "__main__":
    path, number = get_args_from_cmd()
    abs_filename = os.path.join(path, FILENAME)
    reader = csv.DictReader(open(abs_filename, encoding='utf-8', newline=""))
    next(reader)  # skip second header line
    data: List[Tuple[str, float]] = sorted(
        map(transform_record, reader), key=lambda r: r[1], reverse=True)
    if number > len(data):
        print(f"Can't retrieve {number} records from the table.")
        print(f"There are only {len(data)} records in the file.")
        exit()
    print(*map(lambda r: "{:<30}{:<3.1%}".format(*r), data[:number]), sep="\n")
