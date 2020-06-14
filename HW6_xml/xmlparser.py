from typing import Generator, NoReturn
from xml.etree import ElementTree as ET


def parse_and_remove(filename: str, target_tag: str) -> \
        Generator[ET.Element, ET.Element, NoReturn]:
    for event, element in ET.iterparse(filename):
        if element.tag == target_tag:
            yield element


def get_government(country: ET.Element) -> str:
    return country.attrib['government'].strip()


def parse_and_print():
    countries = parse_and_remove("mondial-3.0.xml", "country")
    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    parse_and_print()
