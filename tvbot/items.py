# -*- coding: utf-8 -*-
import scrapy


class TvChannel(scrapy.Item):
    key = scrapy.Field()
    name = scrapy.Field()
    uris = scrapy.Field()
