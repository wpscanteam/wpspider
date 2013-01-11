from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item, Field
import re

class Result(Item):
    url = Field()

class WPSpider(CrawlSpider):
    name = 'wpspider'
    
    def __init__(self, *args, **kwargs):
        if kwargs.get('where') is not None:
            self.allowed_domains = ['%s.svn.wordpress.org' % kwargs.get('where')]
            self.start_urls = ['http://%s.svn.wordpress.org/' % kwargs.get('where')]
        else:
            self.allowed_domains = [
                'themes.svn.wordpress.org',
                'plugins.svn.wordpress.org'
            ]
    
        self.start_urls = [
            'http://themes.svn.wordpress.org/',
            'http://plugins.svn.wordpress.org/'
        ]

        what = re.escape(kwargs.get('what'))

        self.rules = (
            Rule(SgmlLinkExtractor(allow=('.+',))),
            Rule(SgmlLinkExtractor(allow=(what,)), callback='parse_result'),
            #Rule(SgmlLinkExtractor(allow=(what,), deny_extensions=('php', 'jpg', 'jpeg', 'gif', 'png', 'htm', 'html')), callback='parse_item',),
        )

        # super() has to be called after the rules
        super(WPSpider, self).__init__(*args, **kwargs) 

    def parse_result(self, response):
        self.log('Found:\t%s' % response.url)
        item = Result()
        item['url'] = str(response.url)
        return item
