import xml.etree.cElementTree as ET

from rss import ExtractionParameters, create_feed

URL = "https://plurrrr.com/"


def create_extraction_parameters():
    params = ExtractionParameters()
    params.item_filter = ('article', '')
    params.link_filter = ('a', '')
    params.title_filter = ('a', '')
    return params


def main():
    rss = create_feed("Plurr Feed", URL, "RSS Feed To Fetch Plurr Feed",
                      create_extraction_parameters())
    tree = ET.ElementTree(rss)
    tree.write("plurr.xml", xml_declaration=True, encoding="UTF-8")


if __name__ == '__main__':
    main()
