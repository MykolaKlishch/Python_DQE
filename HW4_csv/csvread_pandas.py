import argparse
import csv
import os


def from_cmd(filename):

    def _valid_directory(directory):
        if not os.path.isdir(directory):
            raise argparse.ArgumentTypeError(
                f"'{directory}' is not a name of an existing directory")
        if not os.path.isfile(os.path.join(directory, filename)):
            raise argparse.ArgumentTypeError(
                f"'{directory}' doesn't contain the required file")
        return directory

    parser = argparse.ArgumentParser()
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
    headers, junk_line = data.pop(0), data.pop(0)
    if number > len(data):
        print(f"Can't retrieve {number} records from the table.")
        print(f"There are only {len(data)} records in the file.")
        number = len(data)
    data = list(map(lambda line: (
        line[headers.index("HRR")],
        float(line[headers.index("Available Hospital Beds")].replace(",", ""))
        / float(line[headers.index("Total Hospital Beds")].replace(",", ""))
    ), data))
    data.sort(key=lambda item: item[1], reverse=True)
    for record in data[:number]:
        print(f"{record[0]:<30}{record[1]:<3.1%}")


if __name__ == "__main__":
    _main()
