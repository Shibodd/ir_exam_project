import asyncpraw
import urllib
import re
import bs4
import itertools

URL_ID_REGEX = re.compile(r'(r\/\w+?\/comments\/)?([\d\w]{6})')

def parse_submission_id_from_url(url: str):
  # Parse the submission id from links... Seems to work. Maybe.
  url = urllib.parse.urlparse(url.strip('/')).path.strip('/')
  m = URL_ID_REGEX.match(url)
  assert m
  return m.groups()[1]

async def get_submissions_for_year(red: asyncpraw.Reddit, year):
  subreddit = await red.subreddit('anime')
  page = await subreddit.wiki.get_page(f'discussion_archive/{year}')
  
  html = bs4.BeautifulSoup(page.content_html, 'html.parser')
  tables = html.find_all('table')
  anchors = itertools.chain.from_iterable(table.find_all('a') for table in tables)
  urls = (a.get('href') for a in anchors)
  
  return [parse_submission_id_from_url(url) for url in urls]