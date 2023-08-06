import re

from markdown import markdown


SINGLE_PARAGRAPH_PATTERN = re.compile(r'^<p>((?:(?!<p>).)*)</p>$')
NESTED_TAG_PATTERN = re.compile(r'<p>(<.*>)</p>')


def get_html_from_markdown(text):
    html = markdown(text)
    match = SINGLE_PARAGRAPH_PATTERN.match(html)
    if match:
        html = match.group(1)
    return NESTED_TAG_PATTERN.sub(lambda _: _.group(1), html)
