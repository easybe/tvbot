# -*- coding: utf-8 -*-
import os
import re
import scrapy
import uppod
from urllib import parse
from tvbot import items
from slugify import slugify


class TvonlineSpider(scrapy.Spider):
    name = "tvonline"
    allowed_domains = ['tv-online.im', 'tv-live.in']
    start_urls = ['http://tv-online.im/page/1']
    log_file = 'tvonline.log'

    def __init__(self, category=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            os.remove(self.log_file)
        except FileNotFoundError:
            pass
        self._log = open(self.log_file, 'a')

    def parse(self, response):
        for uri in response.css('article.cactus-post-item').css(
                '.cactus-post-title').css('a::attr(href)').extract():
            print(response.url + ' -> ' + uri, file=self._log)
            yield scrapy.Request(response.urljoin(uri), self.parse_channel)

        next_page = response.css('.nextpostslink::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_channel(self, response):
        cont = response.css('.main-content-col')
        name = cont.css('.single-title::text').extract_first()
        if name:
            key = slugify(name)
            channel = items.TvChannel(name=name, key=key, uris=[])
            uri = cont.css('iframe::attr(src)').extract_first()
            if uri is None:
                return None
            print(response.url + ' --> ' + uri, file=self._log)
            return scrapy.Request(
                uri, callback=self.parse_iframe, meta={'channel': channel})

    def parse_iframe(self, response):
        channel = response.meta['channel']
        uri = response.css('iframe::attr(src)').extract_first()
        if uri is None:
            return None
        print(response.url + ' ---> ' + uri, file=self._log)

        #more_streams = response.css('.pan a::attr(name)')
        #for uri in more_streams.extract():
        #    yield scrapy.Request(
        #        response.urljoin(uri), callback=self.parse_iframe,
        #        meta={'channel': channel})

        yield scrapy.Request(
            response.urljoin(uri), callback=self.parse_iframe2,
            meta={'channel': channel})

    def parse_iframe2(self, response):
        channel = response.meta['channel']

        uri = response.css('iframe::attr(src)').extract_first()

        if uri:
            print(response.url + ' ----> ' + uri, file=self._log)

        stream_uri = None
        m = None
        if uri:
            m = re.search(r'(url|file)=', uri)
        if m:
            query = parse.urlparse(uri).query
            stream_uri = parse.parse_qs(query)[m.group(1)][0]
            if 'uppod' in uri:
                stream_uri = uppod.decode(stream_uri)
        elif uri and (uri.endswith('.m3u8') or uri.startswith('rtmp://')):
            stream_uri = uri

        if stream_uri and re.search(r'^(rtmp|https?)://', stream_uri):
            if stream_uri not in channel['uris']:
                channel['uris'].append(stream_uri)
            return channel

        with open(os.path.join('out', channel['key'] + '.html'), 'w') as f:
            print(response.text, file=f)

        return None
