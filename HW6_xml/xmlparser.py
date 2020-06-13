from xml.etree.ElementTree import iterparse


def parse_and_remove(filename, target_tag):
    for event, element in iterparse(filename):
        if element.tag == target_tag:
            yield element


def get_government(country):
    return country.attrib['government'].strip()


def main():
    countries = parse_and_remove("mondial-3.0.xml", "country")

    import sys
    print(sys.getsizeof(iterparse("mondial-3.0.xml")))
    print(sys.getsizeof(parse_and_remove("mondial-3.0.xml", "country")))
    print(sys.getsizeof(countries))
    print(sys.getsizeof(set(map(get_government, countries))))

    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    main()
