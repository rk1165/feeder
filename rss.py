import base64
import hashlib
import sqlite3
import xml.etree.cElementTree as ET
from datetime import datetime
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
        self.published_at = None


# In general extraction parameters should be same across a page
class ExtractionParameters:
    def __init__(self, item_tag, item_cls, title_tag, title_cls, link_tag, link_cls,
                 description_tag, description_cls):
        self.item_tag = item_tag
        self.item_cls = item_cls
        self.title_tag = title_tag
        self.title_cls = title_cls
        self.link_tag = link_tag
        self.link_cls = link_cls
        self.description_tag = description_tag
        self.description_cls = description_cls

    def __str__(self):
        return (f"({self.item_tag} {self.item_cls})\n"
                f" ({self.title_tag} {self.title_cls})\n"
                f"({self.link_tag} {self.link_cls})\n"
                f"({self.description_tag} {self.description_cls}")


class FormData:
    def __init__(self, channel_title, feed_url, channel_desc):
        self.channel_title = channel_title
        self.feed_url = feed_url
        self.channel_desc = channel_desc
        self.extraction_parameters = None

    def __str__(self):
        return f"{self.channel_title} - {self.feed_url} - {self.channel_desc}"


def update_feed():
    conn = sqlite3.connect('instance/feeds.db')
    cursor = conn.cursor()
    for extractor in cursor.execute('SELECT * FROM extractors'):
        (_, feed_path, url, item_tag, item_cls, title_tag, title_cls,
         link_tag, link_cls, description_tag, description_cls) = extractor
        print(f"Updating {feed_path}")
        params = ExtractionParameters(item_tag, item_cls, title_tag, title_cls,
                                      link_tag, link_cls, description_tag, description_cls)
        items = get_all_items(url, params)
        # print(items)

        with open(f'static/{feed_path}', 'r') as f:
            rss = ET.fromstring(f.read())
            channel = rss.find('channel')
            guids = get_guid(channel)
            print(len(channel))
            while items:
                new_item = create_item_element(None, items.pop())
                if new_item.find('guid').text not in guids:
                    channel.insert(0, new_item)
            print(len(channel))
            # print(ET.tostring(rss).decode('utf-8'))
            with open(f'static/{feed_path}', 'w') as writer:
                writer.write(ET.tostring(rss, xml_declaration=True, encoding="utf-8").decode('utf-8'))
            print(f"Updated {feed_path}")


def get_guid(channel):
    guids = set()
    for item in channel.findall('item'):
        guids.add(item.find('guid').text)
    return guids


def create_feed(title, url, description, extraction_params):
    items = get_all_items(url, extraction_params)  # get item links from web
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
    response = requests.get(url)
    # print(response.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_title(item, tag, title_class):
    title = ''
    if tag != '':
        title = item.find(tag, title_class)
        if title is not None:
            title = title.text.strip()
    return title


def get_link(item, tag, link_class):
    link = ''
    if tag != '':
        link = item.find(tag, link_class)
        if link is not None:
            link = link['href'].strip()
    return link


def get_description(item, tag, description_class):
    description = ''
    if tag != '':
        description = item.find(tag, description_class).text.strip()
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
def get_all_items(url, extraction_params):
    soup = scrape_url(url)
    items = list()
    item_elements = soup.find_all(extraction_params.item_tag, class_=extraction_params.item_cls)
    root_url = get_root_url(url)
    for item in item_elements:
        title = get_title(item, extraction_params.title_tag, extraction_params.title_cls)
        link = get_link(item, extraction_params.link_tag, extraction_params.link_cls)
        if not valid_link(link):
            # print(f"link {link} not valid")
            append = f"/{link}" if link[0] != "/" else f"{link}"
            link = f"{root_url}{append}"
        description = get_description(item, extraction_params.description_tag, extraction_params.description_cls)
        # print(f"{title=} {link=} {description=}")
        if title is not None and link is not None and len(title) > 0 and len(link) > 0:
            items.append(Item(title, link, description))
    return items

# update_feed()
