from xml.etree import ElementTree as ET


def get_government(country: ET.Element) -> str:
    return country.attrib['government'].strip()


def parse_and_print():
    countries = ET.parse("mondial-3.0.xml").getroot().iter("country")
    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    parse_and_print()
