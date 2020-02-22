# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from listal_image.items import ListalImageItem
from time import sleep

id = input("Enter starting URL: ")

class ScrapeimgSpider(scrapy.Spider):
    name = 'scrapeimg'
    allowed_domains = ['listal.com']
    start_urls = [id]

    def parse2(self, response):
        # item = ImageScrapeItem()
        images = response.xpath('//center')
        link = ""
        if images.xpath('./a'):
            urltemp = 'https://www.listal.com' + \
                images.xpath('./a/@href').extract_first()
            sleep(2)
            yield scrapy.Request(urltemp, dont_filter=True, callback=self.parse2)
        else:
            link = images.xpath('./img/@src').extract_first()

        if link:
            loader = ItemLoader(item=ListalImageItem(), selector=images)
            loader.add_value('image_urls', link)
            yield loader.load_item()

    def parse(self, response):
        pics = response.xpath('//*[@class="imagebox "]')

        for pic in pics:
            url = pic.xpath('./div')[0].xpath('.//a/@href').extract_first()
            sleep(2)
            yield scrapy.Request(url, dont_filter=True, callback=self.parse2)
            sleep(2)

        next_pg = response.xpath('//*[@class="pages"]').xpath('.//a/@href')
        if len(next_pg):
            next_pg_url = next_pg[len(next_pg)-1].extract()
            next_pg_url = 'https://www.listal.com' + next_pg_url
            yield scrapy.Request(next_pg_url, dont_filter=True, callback=self.parse)
            sleep(5)

        # for pic in pics:
        #     loader = ItemLoader(item=ListalImageItem(), selector=pic)
        #     url = pic.xpath('./div')[0].xpath('.//img/@src').extract_first()
        #     loader.add_value('image_urls', url)
        #     yield loader.load_item()
