import logging
import sqlite3
import xml.etree.cElementTree as ET
from datetime import datetime
from multiprocessing.pool import ThreadPool

from data import ExtractionParameters
from models import Feed
from rss import get_feed_items, create_item_element

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def get_feeds():
    feeds = list()
    conn = sqlite3.connect('instance/feeds.db')
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM feeds'):
        (_, title, name, url, desc, item_tag, item_cls, title_tag, title_cls,
         link_tag, link_cls, description_tag, description_cls) = row
        feed = Feed(title, name, url, desc, item_tag, item_cls, title_tag, title_cls,
                    link_tag, link_cls, description_tag, description_cls)
        feeds.append(feed)
    logging.info(f"Fetched {len(feeds)} feeds")
    cursor.close()
    conn.close()
    return feeds


def update_feed(feed):
    path = f"{feed.name}"
    logging.info(f"Started updating feed with {path=}")
    params = ExtractionParameters(feed.item_tag, feed.item_cls, feed.title_tag, feed.title_cls,
                                  feed.link_tag, feed.link_cls, feed.description_tag, feed.description_cls)
    items = get_feed_items(feed.url, params)

    with open(f'./static/feeds/{path}', 'r') as f:
        rss = ET.fromstring(f.read())
        channel = rss.find('channel')
        guids = get_guid(channel)
        logging.info(f"Current item counts for {path=} {len(channel)}")
        while items:
            new_item = create_item_element(None, items.pop())
            if new_item.find('guid').text not in guids:
                channel.insert(0, new_item)
        logging.info(f"Updated item counts for {path=} {len(channel)}")
        with open(f'./static/feeds/{path}', 'w') as writer:
            writer.write(ET.tostring(rss, xml_declaration=True, encoding="utf-8").decode('utf-8'))
            logging.info(f"Finished updating feed with {path=}")


def remove_old_items(feed):
    path = f"{feed.name}"
    logging.info(f"Started removing items older than 3 days")
    with open(f'./static/feeds/{path}', 'r') as f:
        rss = ET.fromstring(f.read())
        channel = rss.find('channel')
        logging.info(f"Current item counts for {path=} {len(channel)}")
        for item in channel.findall('item'):
            if is_item_day_old(item, 24 * 3 * 3600):
                channel.remove(item)
        logging.info(f"Updated item counts for {path=} after removal {len(channel)}")
        with open(f'./static/feeds/{path}', 'w') as writer:
            writer.write(ET.tostring(rss, xml_declaration=True, encoding="utf-8").decode('utf-8'))
            logging.info(f"Finished removing old items for {path=}")


def is_item_day_old(item, delta):
    pub_date = item.find('pubDate').text
    pub_time = datetime.strptime(pub_date, '%Y-%m-%d %H:%M:%S.%f')
    time_delta = datetime.now() - pub_time
    if time_delta.seconds >= delta:
        return True
    return False


def get_guid(channel):
    guids = set()
    for item in channel.findall('item'):
        guids.add(item.find('guid').text)
    return guids


def update_feeds():
    logging.info("Running updater Job")
    all_feeds = get_feeds()
    with ThreadPool(processes=4) as pool:
        pool.map(update_feed, all_feeds)


def clean_feeds():
    logging.info("Running removal Job")
    all_feeds = get_feeds()
    with ThreadPool(processes=4) as pool:
        pool.map(remove_old_items, all_feeds)
