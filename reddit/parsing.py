from markdown import Markdown
from bs4 import BeautifulSoup

def markdown_to_plaintext(text):
  __md = Markdown(output_format="html")
  __md.stripTopLevelTags = False
  return BeautifulSoup(__md.convert(text), 'html.parser').get_text().strip()

def parse_post_title(post_title: str):
  try:
    title, episode = post_title.split(" - Episode ")
    title = title.removeprefix("[Spoilers] ")
    episode = episode.removesuffix(" - FINAL")
    episode = episode.removesuffix(" discussion")
    episode = int(episode)
    return (title, episode)
  except:
    return None