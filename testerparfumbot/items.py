from scrapy.item import Item, Field


class TesterparfumbotItem(Item):
    name = Field()
    description = Field()
    category = Field()
    discounted_price = Field()
    price = Field()
    images = Field()
