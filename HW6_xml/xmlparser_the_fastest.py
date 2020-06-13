from xml.etree import ElementTree as et


def get_government(country):
    return country.attrib['government'].strip()


def main():
    countries = et.parse("mondial-3.0.xml").getroot().iter("country")
    governments = set(map(get_government, countries))
    print(*sorted(governments), sep=", ")


if __name__ == "__main__":
    main()
