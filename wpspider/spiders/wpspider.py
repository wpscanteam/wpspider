from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item, Field
from lib.log import LOGGER
from lib.enums import CUSTOM_LOGGING, EXTENSIONS
import re
import datetime


class Result(Item):
    url = Field()

class WPSpider(CrawlSpider):
    name = 'wpspider'
    sessionFilename = 'wpspider/results/%s.log' % str(datetime.datetime.now())


    def __init__(self, *args, **kwargs):

        if kwargs.get('where') is not None:
            self.allowed_domains = ['%s.svn.wordpress.org' % kwargs.get('where')]
            self.start_urls = ['http://%s.svn.wordpress.org/' % kwargs.get('where')]
        else:
            # Default repository domains: THEMES and PLUGINS 
            self.allowed_domains = [
                'themes.svn.wordpress.org',
                'plugins.svn.wordpress.org'
            ]
                                    
            # Default repository urls: THEMES and PLUGINS 
            self.start_urls = [
                'http://themes.svn.wordpress.org/',
                'http://plugins.svn.wordpress.org/'
            ]       
        

        if kwargs.get('what') is None:
            LOGGER.warning("WHAT parameter not set. Default value: ''")
            self.what = "" 
        else:
            self.what = kwargs.get('what')

        
        # Remove the used extension
        # @todo: Define a policy for the exclusion...
        extensions_toexclude = EXTENSIONS.ALL
        
        # Exclude the what .ext from those to exclude during crawl
        try:
            import os
            whatName, whatExtension = os.path.splitext(self.what)
            whatExtension = whatExtension.translate(None, ".")
            extensions_toexclude.remove(whatExtension)
        except ValueError:
            pass # or scream
    
    
        # add case-insensitive regex path 
        whatRgx = '(?i)' + re.escape(self.what)        
    
        
        self.rules = (
            Rule(SgmlLinkExtractor(allow=(), deny=(whatRgx, ),deny_extensions=(extensions_toexclude),)),
            Rule(SgmlLinkExtractor(allow=(whatRgx, ),deny_extensions=(extensions_toexclude),), callback='item_found'),
        )
        
        #Log before proceed
        LOGGER.info('Starting with parameters:')
        LOGGER.info('WHERE: ' + ' - '.join(map(str,self.allowed_domains)))
        LOGGER.info('WHAT: ' + self.what )
        
        # super() has to be called after the rules
        super(WPSpider, self).__init__(*args, **kwargs)        


            
    def item_found(self, response):
        found_resource = response.url 
        LOGGER.log(CUSTOM_LOGGING.RES_FOUND, found_resource)
        
        item = Result()
        item['url'] = found_resource

        # STORE THE RESULTS         
        # Opening the file...
        target = open(self.sessionFilename, 'a+')
        target.write(found_resource)
        target.write("\n")
        
        # ... and close
        target.close()
        
        return item
