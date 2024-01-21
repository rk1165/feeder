import xml.etree.cElementTree as ET

from rss import ExtractionParameters, create_feed

URL = "https://news.ycombinator.com/newest"


def create_extraction_parameters():
    params = ExtractionParameters()
    params.item_filter = ('span', 'titleline')
    params.title_filter = ('a', '')
    params.link_filter = ('a', '')
    return params


def main():
    rss = create_feed("HackerNews Newest", URL, "RSS Feed to fetch latest articles",
                      create_extraction_parameters())
    tree = ET.ElementTree(rss)
    tree.write("hackernews.xml", xml_declaration=True, encoding="UTF-8")


if __name__ == '__main__':
    main()
