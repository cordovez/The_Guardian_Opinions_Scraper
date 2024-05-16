from scrapy import Item, Field
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


class GuardianItem(Item):
    headline = Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    author = Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    teaser = Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    published = Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    content = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join("\n"),
    )
    url = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
