from xml.etree import ElementTree as et


def get_government(country):
    return country.attrib['government'].strip()


def parse_and_print():
    countries = et.parse("mondial-3.0.xml").getroot().iter("country")
    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    parse_and_print()
