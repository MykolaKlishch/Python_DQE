import xml.etree.ElementTree as et


def parse_and_remove(filename, element_tag):
    doc = et.iterparse(filename, ('start', 'end'))
    for event, elem in doc:
        if elem.tag == element_tag:
            yield elem


def get_government(country):
    return country.attrib['government'].strip()


def main():
    countries = parse_and_remove("mondial-3.0.xml", "country")
    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    main()
