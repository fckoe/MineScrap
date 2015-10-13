import scrapy

"""from MinescrapItem.items import MinescrapItem"""

from scrapy.http import FormRequest
from loginform import fill_login_form
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class DmozSpider(scrapy.Spider):
    name = "mine"
    allowed_domains = ["forominecraft.com"]
    start_urls = [
        "http://forominecraft.com/content/"
    ]
    #foro = "http://forominecraft.com/forum.php"
    login_user = "fckoe"
    login_pass = "Win2015"
 
    def parse(self, response):
        args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
        return FormRequest(url, method=method, formdata=args, callback=self.after_login)
 
    def after_login(self, response):
        #print "hola "+response.url
        # you are logged in here
        return scrapy.Request(response.url,callback=self.parse_page2)

    def parse_page2(self, response):
        print "hola 2",response.url
        h2 = response.xpath('//h2')
        filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
        for a in h2.xpath('//a/@href'):  
            #print a.extract()
            #f.write(a.extract())
            yield scrapy.Request(a.extract(),callback=self.link)

 
    def link(self,response):
        h3 = response.xpath('//h3')
        filename = response.url.split("/")[-2]+'.html'
        with open (filename,'wb') as f:
            f.write(response.body)

