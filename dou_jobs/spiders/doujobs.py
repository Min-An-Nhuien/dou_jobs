import scrapy
import json
import lxml.html
import re
from dou_jobs.items import DouJobsItem


class DouJobsSpider(scrapy.Spider):
    name = 'dou_jobs'
    start_urls = ['https://jobs.dou.ua/vacancies/']
    form_data = {'csrfmiddlewaretoken': '',
                'count': '20'}

    def parse(self, response):
        last = False

        if response.headers[b'Content-type'].startswith(b'application/json'):
            response_array = json.loads(response.text)
            html = lxml.html.fromstring(response_array['html'])
            last = response_array['last']
            self.form_data['count'] = str(int(self.form_data['count']) + 40)
        else:
            html = lxml.html.fromstring(response.text)
            self.form_data['csrfmiddlewaretoken'] = response.headers.getlist('Set-Cookie')[0].decode('utf-8').split(';')[0].split('=')[1]
        for vacancy_url in html.xpath('//a[@class="vt"]/@href'):
            yield scrapy.Request(vacancy_url, callback=self.parse_item)
        if not last:
            yield scrapy.FormRequest(url='https://jobs.dou.ua/vacancies/xhr-load/?', formdata=self.form_data)

    def parse_item(self, response):
        item = DouJobsItem()
        item['title'] = response.xpath('//h1[@class="g-h2"]/text()').extract_first()
        item['city'] = response.xpath('//span[@class="place"]/text()').extract_first()
        item['salary'] = response.xpath('//span[@class="salary"]/text()').extract_first()
        full_description = response.xpath('//div[@itemprop="description"]/h3/text() |'
                                          ' //div[@itemprop="description"]/div[@class="text b-typo vacancy-section"]/p').extract()
        description_to_string = '\n'.join(full_description).replace('<br>', '\n')
        item['description'] = re.sub('<[^>]*>', '', description_to_string)
        item['company'] = response.xpath('//div[@class="l-n"]/a/text()').extract_first()
        item['date'] = response.xpath('//div[@class="date"]/text()').extract_first()
        item['url'] = response.url
        yield item
