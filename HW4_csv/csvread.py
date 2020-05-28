import argparse
import csv
import os
from typing import List


def get_namespace(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-path",
                        help="a path to the .csv file")
    parser.add_argument("-bed", type=int, dest="top",
                        help="number or HRR to display")
    parsed_args = parser.parse_args(args)
    return parsed_args.path, parsed_args.top