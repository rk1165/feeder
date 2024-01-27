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
                f"({self.title_tag} {self.title_cls})\n"
                f"({self.link_tag} {self.link_cls})\n"
                f"({self.description_tag} {self.description_cls})")


class FormData:
    def __init__(self, channel_title, feed_url, channel_desc):
        self.channel_title = channel_title
        self.feed_url = feed_url
        self.channel_desc = channel_desc
        self.extraction_parameters = None

    def __str__(self):
        return (f"[title={self.channel_title} url={self.feed_url} description={self.channel_desc}]\n"
                f"{self.extraction_parameters}")
