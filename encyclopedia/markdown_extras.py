import re

import markdown


def convert_markdown_to_html(value):
    # Rewrites [Link](SomePage) to [Link](/wiki/SomePage)
    value = re.sub(r"\((?!http)([^)]+)\)", r"(/encyclopedia\1)", value)
    return markdown.markdown(value)
