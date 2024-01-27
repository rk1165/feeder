import base64
import hashlib
import logging
import xml.etree.cElementTree as ET
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from feed import Channel, Item

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def create_feed_file(title, url, description, extraction_params):
    items = get_feed_items(url, extraction_params)  # get feed items from webpage
    channel = Channel(title, url, description)
    channel.items = items
    return create_rss_xml(channel)


def create_rss_xml(from_channel):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = from_channel.title
    ET.SubElement(channel, "link").text = from_channel.link
    ET.SubElement(channel, "description").text = from_channel.description
    for entry in from_channel.items:
        item = ET.SubElement(channel, "item")
        create_item_element(item, entry)
    return rss


def create_item_element(item, item_entry):
    if item is None:
        item = ET.Element("item")
    ET.SubElement(item, "title").text = item_entry.title
    ET.SubElement(item, "link").text = item_entry.link
    ET.SubElement(item, "description").text = item_entry.description
    ET.SubElement(item, "pubDate").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    ET.SubElement(item, "guid", isPermaLink="false").text = \
        (base64.urlsafe_b64encode(hashlib.sha3_256(item_entry.link.encode()).digest()).decode())
    return item


def scrape_url(url):
    try:
        logging.info(f"Request received for {url=}")
        response = requests.get(url, timeout=10)
        # print(response.headers)
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions:
        raise requests.exceptions.RequestException("Unable to fetch webpage details")


def get_title(item, tag, title_class):
    # print(f"{item=} {tag=} {title_class=}")
    title = ''
    if tag != '':
        title = item.find(tag, class_=title_class)
        if title is not None:
            title = title.text.strip()
    return title


def get_link(item, tag, link_class):
    link = ''
    if tag != '':
        link = item.find(tag, class_=link_class)
        if link is not None:
            link = link['href'].strip()
    return link


def get_description(item, tag, description_class):
    # print(f"{item=} {tag=} {description_class=}")
    description = ''
    if tag != '':
        description = item.find(tag, class_=description_class)
        if description is not None:
            description = description.text.strip()
    return description


def get_root_url(url):
    logging.info(f"Getting root for {url=}")
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    scheme = parsed_url.scheme
    return scheme + '://' + domain


def valid_link(link):
    logging.debug(f"Validating link {link=}")
    parsed_url = urlparse(link)
    domain = parsed_url.netloc
    scheme = parsed_url.scheme
    if domain == '' or scheme == '':
        return False
    return True


# Item is the encapsulation of a RSS Feed Item : It has title, link, description (if present)
def get_feed_items(url, extraction_params):
    soup = scrape_url(url)
    items = list()
    item_elements = soup.find_all(extraction_params.item_tag, class_=extraction_params.item_cls)
    logging.info(f"Found {len(item_elements)}")
    # print(f"Found {len(item_elements)} elements")
    root_url = get_root_url(url)
    for item in item_elements:
        title = get_title(item, extraction_params.title_tag, extraction_params.title_cls)
        link = get_link(item, extraction_params.link_tag, extraction_params.link_cls)
        if not valid_link(link):
            append = f"/{link}" if link[0] != "/" else f"{link}"
            link = f"{root_url}{append}"
        description = get_description(item, extraction_params.description_tag, extraction_params.description_cls)
        # logging.info(f"{title=} {link=} {description=}")
        if title is not None and link is not None and len(title) > 0 and len(link) > 0:
            items.append(Item(title, link, description))
    return items
