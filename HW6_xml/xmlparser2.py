import re
from xml.etree import ElementTree as ET


def get_element(event_element_pair):
    return event_element_pair[1]


def is_country(element):
    return element.tag == "country"


def has_long_name(country):
    compiled_long_name_pattern = re.compile(r"^(\w+\s)+\w+$")
    return compiled_long_name_pattern.match(country.attrib['name'])


def get_government(country):
    return country.attrib['government'].strip()


def parse_and_print():
    elements = map(get_element, ET.iterparse("mondial-3.0.xml"))
    countries = filter(is_country, elements)
    countries_with_long_names = filter(has_long_name, countries)
    governments = set(map(get_government, countries_with_long_names))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    parse_and_print()
