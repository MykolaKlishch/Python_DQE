from xml.etree import ElementTree as et


def get_government(country):
    return country.attrib['government'].strip()


def main():
    countries = et.parse("mondial-3.0.xml").getroot().iter("country")

    import sys
    print(sys.getsizeof(et.parse("mondial-3.0.xml")))
    print(sys.getsizeof(et.parse("mondial-3.0.xml").getroot()))
    print(sys.getsizeof(et.parse("mondial-3.0.xml").getroot().iter("country")))
    print(sys.getsizeof(countries))
    print(sys.getsizeof(set(map(get_government, countries))))

    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    main()
