import sched
import time
import xml.etree.cElementTree as ET

from rss import ExtractionParameters, create_feed


def create_extraction_parameters1():
    url = "https://news.ycombinator.com/newest"
    params = ExtractionParameters()
    params.item_filter = ('span', 'titleline')
    params.title_filter = ('a', '')
    params.link_filter = ('a', '')
    return params, url


def create_extraction_parameters2():
    url = "https://www.eurekalert.org/news-releases/browse?view=summaries&date=01/20/2024"
    params = ExtractionParameters()
    params.item_filter = ('article', 'post')
    params.title_filter = ('h2', 'post_title')
    params.link_filter = ('a', ['', 'has-thumb'])
    params.description_filter = ('div', 'intro')
    return params, url


def create_extraction_parameters3():
    url = "https://betterdev.link/"
    params = ExtractionParameters()
    params.item_filter = ('div', 'issue-link')
    params.link_filter = ('a', '')
    params.title_filter = ('a', '')
    params.description_filter = ('p', '')
    return params, url


def create_extraction_parameters4():
    url = "https://plurrrr.com/"
    params = ExtractionParameters()
    params.item_filter = ('article', '')
    params.link_filter = ('a', '')
    params.title_filter = ('a', '')
    return params, url


count = 0


def generate_feed_file(scheduler):
    global count
    print(f"Generating feed for {count}")
    scheduler.enter(60, 1, generate_feed_file, (scheduler,))
    params, url = create_extraction_parameters1()
    rss = create_feed("HackerNews Newest", url, "RSS Feed to fetch latest articles", params)
    tree = ET.ElementTree(rss)
    tree.write(f"static/hackernews-{count}.xml", xml_declaration=True, encoding="UTF-8")
    count += 1


def schedule():
    scheduler = sched.scheduler(time.monotonic, time.sleep)
    scheduler.enter(5, 1, generate_feed_file, (scheduler,))
    scheduler.run()


if __name__ == '__main__':
    schedule()
