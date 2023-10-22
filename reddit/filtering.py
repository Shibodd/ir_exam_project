from markdown import Markdown
from bs4 import BeautifulSoup


def markdown_to_plaintext(text):
  __md = Markdown(output_format="html")
  __md.stripTopLevelTags = False
  return BeautifulSoup(__md.convert(text), 'html.parser').get_text()