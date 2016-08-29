import random
from urllib.parse import quote

import lxml.html
import requests
from django.core.management.base import BaseCommand, CommandError

from yandex_parser.models import YandexPage

proxy_list = ['http://115.182.15.27:8080',
              'http://31.186.25.157:3128',
              'http://31.186.25.157:3128',
              'http://123.72.43.164:8888'
              ]
proxies = {
    "http": random.choice(proxy_list),
    "https": 'https://92.222.107.175:3128'}
print(proxies)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('word')

    def handle(self, *args, **options):
        word = options['word']
        word = quote(word)
        for i in range(3):
            url = "http://yandex.ru/yandsearch?text={word}&p={page}".format(
                word=word, page=i)
            # response = requests.get(url, proxies=proxies)
            response = requests.get(url)
            response.encoding = 'utf-8'
            tree = lxml.html.fromstring(response.text)
            title = tree.xpath('//title/text()')
            insert_list = []
            for link in tree.xpath('//div[@class="organic"]/h2/'
                                   'a[@class="link serp-item__title-link link link_cropped_no"]'):
                page = YandexPage()
                page.url = link.xpath('@href')
                page.title = ' '.join(link.xpath('text()'))
                page.page = i
                print(page)
                insert_list.append(page)
            YandexPage.objects.bulk_create(insert_list)
            print('Saved {} objects'.format(len(insert_list)))
