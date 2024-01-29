import xml.etree.cElementTree as ET

from feed import ExtractionParameters
from rss import create_feed_file

URL = 'https://careers.scaleway.com/#anchor-joblist'


def create_extraction_parameters():
    params = ExtractionParameters('a', 'JobsTable__body', 'div', 'jobname',
                                  'a', 'JobsTable__body', '' ,'')

    return params


def generate_feed_file(url):
    params = create_extraction_parameters()
    rss = create_feed_file("HackerNews Newest", url, "RSS Feed to fetch latest articles", params)
    tree = ET.ElementTree(rss)
    tree.write(f"static/tree.xml", xml_declaration=True, encoding="UTF-8")


generate_feed_file(URL)
