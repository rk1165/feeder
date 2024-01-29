import logging
import xml.etree.cElementTree as ET

import selenium.webdriver as webdriver

from data import ExtractionParameters
from rss import create_feed_file

URL = 'https://careers.scaleway.com/#anchor-joblist'


def create_extraction_parameters():
    params = ExtractionParameters('a', 'JobsTable__body', 'div', 'jobname',
                                  'a', 'JobsTable__body', '', '')

    return params


def generate_feed_file(url):
    params = create_extraction_parameters()
    rss = create_feed_file("HackerNews Newest", url, "RSS Feed to fetch latest articles", params)
    tree = ET.ElementTree(rss)
    tree.write(f"static/tree.xml", xml_declaration=True, encoding="UTF-8")


def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    logging.info(f"Fetching html content for dynamic website {url}")
    driver.get(url)
    driver.implicitly_wait(2)
    content = driver.page_source
    driver.quit()
    return content


# print(get_html(URL))

# generate_feed_file(URL)
