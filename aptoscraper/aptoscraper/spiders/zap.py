import scrapy

class ZapSpider(scrapy.Spider):
    name = 'zap'
    allowed_domains = ['zapimoveis.com.br']
    start_urls = ['http://zapimoveis.com.br/']

    # This is a built-in Scrapy function that runs first where we'll override the default headers
    # Documentation: https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider.start_requests
    def start_requests(self):
        url = "https://www.eventbriteapi.com/v3/organizers/[ORG_ID]/events/?token=[YOUR_TOKEN]"

        # Set the headers here. The important part is "application/json"
        headers =  {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9',
            'origin': 'https://www.zapimoveis.com.br',
            'referer': 'https://www.zapimoveis.com.br',
            'access-control-request-headers': 'x-domain',
            'access-control-request-method': 'GET'
        }

        yield scrapy.http.Request(url, headers=headers)

    def parse(self, response):
        pass
