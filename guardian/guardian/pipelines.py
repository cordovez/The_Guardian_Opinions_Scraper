import pymongo
from itemadapter import ItemAdapter


class MongoDBPipeline:
    collection_name = "opinions"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGODB_URI"),
            mongo_db=crawler.settings.get("MONGODB_DATABASE", "the_guardian"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = spider.name

        if item["content"] is not None and item["author"] is not None:
            self.db[collection_name].insert_one(ItemAdapter(item).asdict())
            return item
