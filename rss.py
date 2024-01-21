import xml.etree.cElementTree as ET
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class Channel:
    def __init__(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description
        self.items = []


class Item(object):
    def __init__(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description


# In general extraction parameters should be same across a page
class ExtractionParameters:
    def __init__(self):
        self.item_filter = (None, None)
        self.title_filter = (None, None)
        self.link_filter = (None, None)
        self.description_filter = (None, None)


def create_feed(title, url, description, extraction_parameters):
    items = get_all_items(url, extraction_parameters)
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
        # print(entry)
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link
        ET.SubElement(item, "description").text = entry.description
    return rss


def scrape_url(url):
    response = requests.get(url)
    # print(response.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_title(item, element, title_class):
    title = ''
    if element != '':
        title = item.find(element, title_class).text.strip()
    return title


def get_link(item, element, link_class):
    link = ''
    if element != '':
        link = item.find(element, link_class)['href'].strip()
    return link


def get_description(item, element, description_class):
    description = ''
    if element != '':
        description = item.find(element, description_class).text.strip()
    return description


def get_root_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    scheme = parsed_url.scheme
    return scheme + '://' + domain


def valid_link(link):
    parsed_url = urlparse(link)
    domain = parsed_url.netloc
    scheme = parsed_url.scheme
    if domain == '' or scheme == '':
        return False
    return True


# Item is the encapsulation of a RSS Feed Item : It has title, link, description (if present)
def get_all_items(url, extraction_parameters):
    soup = scrape_url(url)
    items = list()
    item_element, item_class = extraction_parameters.item_filter
    title_element, title_class = extraction_parameters.title_filter
    link_element, link_class = extraction_parameters.link_filter
    description_element, description_class = extraction_parameters.description_filter
    item_elements = soup.find_all(item_element, class_=item_class)
    root_url = get_root_url(url)
    for item in item_elements:
        title = get_title(item, title_element, title_class)
        link = get_link(item, link_element, link_class)
        if not valid_link(link):
            append = f"/{link}" if link[0] != "/" else f"{link}"
            link = f"{root_url}{append}"
        description = get_description(item, description_element, description_class)
        # print(f"{title=} {link=} {description=}")
        items.append(Item(title, link, description))
    return items
