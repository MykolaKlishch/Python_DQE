"""Read 'user_details.csv' file from a specified path.
Remove sensitive information from the obtained user data.
Convert data to json format, pretty-print it and save
into json file under the specified name and path."""

import argparse
import csv
import json
import os
from typing import Dict, List, Tuple, Iterable

CSV_FILENAME = "user_details.csv"


def get_args_from_cmd() -> Tuple[str, str]:
    """Get the name of the directory with .csv file
    and the name of .json dump file from command line.

    :return: the name of the directory with .csv file to be read,
             the name of .json dump file.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-csv", type=valid_directory_with_csv, default=os.getcwd(),
        help="a directory with .csv file to be opened")
    parser.add_argument(
        "-json", type=in_valid_directory, default="user_details.json",
        help="absolute or relative filename of .json dump file")
    args = parser.parse_args()
    return args.csv, args.json


def valid_directory_with_csv(directory: str) -> str:
    """Used for validation of the command line argument -csv.

    :param directory: -csv argument value
    :raise ArgumentTypeError: if the directory does not exist
           or does not contain a required .csv file.
    """
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(
            f"'{directory}' is not a name of an existing directory")
    if not os.path.isfile(os.path.join(directory, CSV_FILENAME)):
        raise argparse.ArgumentTypeError(
            f"'{directory}' doesn't contain the required file")
    return directory


def in_valid_directory(filename: str) -> str:
    """Used for validation of the command line argument -json

    :param filename: -json argument value
    :raise ArgumentTypeError: if the file name is absolute but
           the specified directory does not exist.
    """
    if os.path.isabs(filename):
        directory, rel_filename = os.path.split(filename)
        if not os.path.isdir(directory):
            raise argparse.ArgumentTypeError(
                f"'{directory}' is not a name of an existing directory")
    return filename


def make_records_safe(sensitive_records: Iterable[Dict[str, str]]
                      ) -> List[Dict[str, str]]:
    """Remove sensitive information from all records in the iterable

    :param sensitive_records: records that may contain passwords
    :return: records without sensitive information
    """
    return list(map(remove_password_from_record, sensitive_records))


def remove_password_from_record(record: Dict[str, str]) -> Dict[str, str]:
    """Remove password from the record.

    :param record: a record that may contain 'password' key
    :return: a record without a 'password' key
    """
    if "password" in record.keys():
        del record["password"]
    return record


if __name__ == "__main__":
    csv_file_path, json_abs_filename = get_args_from_cmd()
    csv_abs_filename = os.path.join(csv_file_path, CSV_FILENAME)
    reader = csv.DictReader(
        open(csv_abs_filename, mode="rt", encoding='utf-8', newline=""))
    safe_records = make_records_safe(reader)
    print(json.dumps(safe_records, indent=4))
    with open(json_abs_filename, mode="wt", encoding='utf-8') as writer:
        json.dump(safe_records, writer, indent=4)
