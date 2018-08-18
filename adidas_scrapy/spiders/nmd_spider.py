import scrapy

class NMDSpider(scrapy.Spider):
    #NMD is a type of Adidas sneaker
    name = "nmd"
    start_urls = [
        'http://www.adidas.ca/en/nmd-shoes'
    ]

    def parse(self, response):
        for shoe in response.css('div.innercard.col'):
            yield {
                'status': shoe.css('span.badge-text::text').extract_first().strip(),
                'name': shoe.css('span.title::text').extract_first(),
                'color' : scrapy.Request(url=shoe.css('div.image.plp-image-bg a::attr(href)').extract_first(),
                                         callback=self.parse_colorway),
                'price': shoe.css('span.salesprice::text').extract_first().strip()
            }

    # Purpose: Get the colorway of the shoe, since shoes have the same name, the only way to distinguish
    # a unique shoe is from the colorway
    def parse_colorway(self, response):
        for item in response.css('div.js-main-product-section'):
            return item.css('span.product-color-clear::text').extract_first()
