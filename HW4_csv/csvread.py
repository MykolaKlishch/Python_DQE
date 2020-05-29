"""Read 'HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv' file
from a specified path. Calculate percentage of available hospital
beds for all HRR. Display these percentages for a specified number
of HRR where the percentages are the highest.
"""

import argparse
import csv
import os
from typing import Tuple


def from_cmd(filename: str) -> Tuple[str, int]:
    """Get file path and number of records from command line.

    :param filename: a name of the file to be added to the path
    :return: file path, number of records to display
    """

    def _valid_directory(directory: str) -> str:
        """Used for internal validation of the command line argument -path

        :param directory: -path value
        :raise ArgumentTypeError: if validation fails
        """
        if not os.path.isdir(directory):
            raise argparse.ArgumentTypeError(
                f"'{directory}' is not a name of an existing directory")
        if not os.path.isfile(os.path.join(directory, filename)):
            raise argparse.ArgumentTypeError(
                f"'{directory}' doesn't contain the required file")
        return directory

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-path", type=_valid_directory, default=os.getcwd(),
                        help="a directory with .csv file to be opened")
    parser.add_argument("-bed", type=int, default=5,
                        help="number or HRR to be displayed")
    args = parser.parse_args()
    args.path = os.path.join(args.path, filename)
    return args.path, args.bed


def _main():
    filename = "HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv"
    file_path, number = from_cmd(filename)
    data = list(csv.reader(open(file_path, newline="")))
    headers, remark_line = data.pop(0), data.pop(0)
    if number > len(data):
        print(f"Can't retrieve {number} records from the table.")
        print(f"There are only {len(data)} records in the file.")
        number = len(data)
    data = list(map(lambda record: (
        record[headers.index("HRR")],
        float(record[headers.index(
            "Available Hospital Beds")].replace(",", ""))
        / float(record[headers.index(
            "Total Hospital Beds")].replace(",", ""))), data))
    data.sort(key=lambda record: record[1], reverse=True)
    for row in data[:number]:
        print(f"{row[0]:<30}{row[1]:<3.1%}")


if __name__ == "__main__":
    _main()
