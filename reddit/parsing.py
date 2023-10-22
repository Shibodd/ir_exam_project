from markdown import Markdown
from bs4 import BeautifulSoup

def markdown_to_plaintext(text):
  __md = Markdown(output_format="html")
  __md.stripTopLevelTags = False
  return BeautifulSoup(__md.convert(text), 'html.parser').get_text().strip()

def parse_post_title(title: str):
  try:
    anime_title, episode = title.split(" - Episode ")
    anime_title = anime_title.removeprefix("[Spoilers] ")
    anime_episode = episode.removesuffix(" - FINAL")
    anime_episode = episode.removesuffix(" discussion")
    anime_episode = int(anime_episode)
    return (anime_title, anime_episode)
  except:
    return None