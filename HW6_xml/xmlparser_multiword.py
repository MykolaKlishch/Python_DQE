"""Parse xml document 'mondial-3.0.xml' and print all
types of government that are mentioned in this file
for countries with multiword names.
"""

import re
from typing import Tuple
from xml.etree import ElementTree as ET


def get_element(event_element_pair: Tuple[str, ET.Element]) -> ET.Element:
    return event_element_pair[1]


def is_country(element: ET.Element) -> bool:
    return element.tag == "country"


def has_long_name(country: ET.Element) -> bool:
    return bool(re.match(r"^(\w+\s)+\w+$", country.attrib['name']))


def get_government(country: ET.Element) -> str:
    return country.attrib["government"].strip()


def parse_and_print():
    elements = map(get_element, ET.iterparse("mondial-3.0.xml"))
    countries = filter(is_country, elements)
    countries_with_long_names = filter(has_long_name, countries)
    governments = set(map(get_government, countries_with_long_names))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    parse_and_print()
