import feedparser
from datetime import date
import pickle


class FeedObject:
    def __init__(self, id, title, traffic, expanded_title, snippet, url, image_url):
        self.id = id
        self.title = self.sanitize_data(title)
        self.traffic = self.sanitize_data(traffic)
        self.expanded_title = self.sanitize_data(expanded_title)
        self.snippet = self.sanitize_data(snippet)
        self.url = url
        self.image_url = image_url

    def sanitize_data(self, data):
        for r in (("&#39;", "'"), ("&nbsp;", ""), ("&quot;", "'")):
            data = data.replace(*r)
        return data

    def formatted(self):
        data = ""
        data += self.title + ' (' + self.traffic + ' searches today)' + \
            '\n\n' + self.snippet + '\n\n' + 'Find out more: ' + self.url
        return data

    def __str__(self):
        return 'FeedObject: \n\n' + self.formatted() + '\n'


class GoogleTrendingSearch:
    def __init__(self, url):
        self.url = url
        self.display_date = str(date.today().strftime("%d %B %Y"))
        self.feed = feedparser.parse(url)
        self.feed_array = []

    def published_today(self, published_date):
        today = date.today().strftime("%d %B")
        if today in published_date:
            return True
        return False

    def get_feed_data_today(self):
        id = 0
        for post in self.feed.entries:
            if self.published_today(post['published']):
                id += 1
                self.feed_array.append(FeedObject(id, post['title'], post['ht_approx_traffic'], post['ht_news_item_title'],
                                                  post['ht_news_item_snippet'], post['ht_news_item_url'], post['ht_picture']))

    def get_feed_data_all(self):
        id = 0
        for post in self.feed.entries:
            id += 1
            self.feed_array.append(FeedObject(id, post['title'], post['ht_approx_traffic'], post['ht_news_item_title'],
                                                post['ht_news_item_snippet'], post['ht_news_item_url'], post['ht_picture']))