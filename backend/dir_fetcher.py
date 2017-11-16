import requests
from bs4 import BeautifulSoup, SoupStrainer

REPORT_PAGE = 'https://registrar.wisc.edu/current-reports/'

def fetch_dir_links():
  page = requests.get(REPORT_PAGE)
  links = BeautifulSoup(page.text, 'html.parser', parse_only=SoupStrainer('a'))

  dir_hrefs = {}

  for link in links:
    if not link.has_attr('href'):
      continue

    href = link['href']
    href_upper = href.upper()

    # only parse DIR pdfs
    if 'DIR' not in href_upper:
      continue

    # ignore "memos" and "calls", they do not contain data
    if 'MEMO' in href_upper or 'CALL' in href_upper:
      continue

    file = href.split("/")[-1]
    sis_term_code = int(filter(str.isdigit, str(file)))

    # check if we already encountered this DIR, in case something weird is going on
    if sis_term_code in dir_hrefs:
      existing_href = dir_hrefs[sis_term_code]
      print('Already parsed %s DIR. Did registrar website update?' % sis_term_code)
      print('Ignoring: %s, using existing DIR: %s' % (href, existing_href))
      continue

    dir_hrefs[sis_term_code] = href

  return dir_hrefs

print(fetch_dir_links())