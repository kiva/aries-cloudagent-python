"""Regex tools for aca-py."""

import re


def find_attach_in_attribute(attribute: str):
    """Find attach in string to be used in attachments for verifiable credentials."""
    bool(re.search("~attach", attribute))
