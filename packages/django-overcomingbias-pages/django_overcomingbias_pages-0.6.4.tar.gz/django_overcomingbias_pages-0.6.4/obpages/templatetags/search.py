import bs4
from django import template

register = template.Library()


@register.filter
def html_to_plaintext(raw_html):
    return bs4.BeautifulSoup(raw_html, "lxml").text.strip()
