import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from ..items import GuardianItem
from scrapy.loader import ItemLoader

month = datetime.now().strftime("%b").lower()
year = datetime.now().strftime("%Y")


class OpinionsSpider(CrawlSpider):
    name = "opinions"
    allowed_domains = ["theguardian.com"]
    start_urls = ["https://www.theguardian.com/uk/commentisfree/"]
    # custom_settings = {"FEEDS": {"opinions_crawled.json": {"format": "json"}}}
    rules = (
        Rule(LinkExtractor(allow=(r"uk/commentisfree/",), deny=(r"-cartoon",))),
        Rule(
            LinkExtractor(allow=(rf"{year}/{month}/",)),
            callback="parse_opinion",
        ),
    )

    def parse_opinion(self, response):
        """
        headline = response.css("div[data-gu-name='headline'] div h1::text").get()
        author = response.css("a[rel='author'] ::text").get()
        teaser= response.css("aside[data-gu-name='meta'] summary span ::text").get()
        published = response.css("div.dcr-1kpcv08 span::text").get()
        joined_text = ''.join(response.css('div[data-gu-name="body"] p::text').extract())
        canonical_url = response.css('link[rel="canonical"]::attr(href)').get()
        """
        guardian_article = ItemLoader(item=GuardianItem(), response=response)

        guardian_article.add_css("headline", "div[data-gu-name='headline'] div h1")
        guardian_article.add_css("author", "a[rel='author']")
        guardian_article.add_css("teaser", "div[data-gu-name='standfirst'] div p")
        guardian_article.add_css("published", "aside[data-gu-name='meta'] summary span")
        guardian_article.add_css("content", "div[data-gu-name='body']")
        guardian_article.add_css("url", "link[rel='canonical']::attr(href)")

        return guardian_article.load_item()
