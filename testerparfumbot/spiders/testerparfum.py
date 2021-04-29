import scrapy

from testerparfumbot.items import TesterparfumbotItem


class TesterparfumSpider(scrapy.Spider):
    name = 'testerparfum'
    allowed_domains = ['testerparfum.com']
    base_url = 'https://www.testerparfum.com/'

    def start_requests(self):
        base_url = 'https://www.testerparfum.com/page.php?ajax=1&act=arama&catID=0&str=&page=%s'
        urls = []
        for page in range(87):
            urls.append(base_url % page)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        product_details = response.css(".product > article > .content > h5 > a::attr(href)").getall()
        for product_detail in product_details:
            detail_url = self.base_url + product_detail
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        product_images = []

        response_item = TesterparfumbotItem()

        product_name = response.css("h5.pro-title::text").get()
        response_item['name'] = product_name

        product_price = response.css(".price > span::text").get()
        response_item['price'] = product_price.split(' TL')[0]

        product_discounted_price = response.css(".price > price::text").get()
        response_item['discounted_price'] = product_discounted_price.split(' TL')[0]

        product_description = response.css("#description").get()
        response_item['description'] = product_description

        product_category = response.css('.breadcrumb > li > a > span::text')[-1].extract()
        response_item['category'] = product_category

        p_images = response.css('.slider-nav__item > img::attr(data-lazy)').getall()
        for p_image in p_images:
            product_images.append(self.base_url + p_image.replace('120x120', '1024x1024'))

        response_item['images'] = product_images

        yield response_item
