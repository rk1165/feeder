import xml.etree.cElementTree as ET

from rss import ExtractionParameters, create_feed

URL = "https://www.eurekalert.org/news-releases/browse?view=summaries&date=01/20/2024"


def create_extraction_parameters():
    params = ExtractionParameters()
    params.item_filter = ('article', 'post')
    params.title_filter = ('h2', 'post_title')
    params.link_filter = ('a', ['', 'has-thumb'])
    params.description_filter = ('div', 'intro')
    return params


def main():
    rss = create_feed("EurekaAlert", URL, "RSS Feed To Fetch Eurekalert News",
                      create_extraction_parameters())
    tree = ET.ElementTree(rss)
    tree.write("eureka.xml", xml_declaration=True, encoding="UTF-8")


if __name__ == '__main__':
    main()
