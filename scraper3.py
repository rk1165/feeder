import xml.etree.cElementTree as ET

from rss import ExtractionParameters, create_feed

URL = "https://betterdev.link/"


def create_extraction_parameters():
    params = ExtractionParameters()
    params.item_filter = ('div', 'issue-link')
    params.link_filter = ('a', '')
    params.title_filter = ('a', '')
    params.description_filter = ('p', '')
    return params


def main():
    rss = create_feed("BetterDev Feed", URL, "RSS Feed To Fetch BetterDev Feed",
                      create_extraction_parameters())
    tree = ET.ElementTree(rss)
    tree.write("better_dev.xml", xml_declaration=True, encoding="UTF-8")


if __name__ == '__main__':
    main()
