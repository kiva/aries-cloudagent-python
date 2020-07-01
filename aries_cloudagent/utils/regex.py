import re


def find_attach_in_attribute(attribute: str):
    bool(re.search("~attach", attribute))
