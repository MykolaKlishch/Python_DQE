"""Parse xml document 'mondial-3.0.xml' and print all
types of government that are mentioned in this file.
"""

from typing import Generator, NoReturn
from xml.etree import ElementTree as ET


def parse_and_remove(filename: str, target_tag: str) -> \
        Generator[ET.Element, ET.Element, NoReturn]:
    """Generator that yields specific elements from an XML file.

    :param filename: a file to be parsed
    :param target_tag: only elements with this tag will be yielded
    """
    for event, element in ET.iterparse(filename):
        if element.tag == target_tag:
            yield element


def get_government(country: ET.Element) -> str:
    return country.attrib["government"].strip()


def parse_and_print():
    countries = parse_and_remove("mondial-3.0.xml", "country")
    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    parse_and_print()
