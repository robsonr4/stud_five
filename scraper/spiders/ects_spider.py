import scrapy
from scraper.items import TitlesItem
class EctsSpider(scrapy.Spider):
    name = 'ects'
    start_urls = ['https://cas.swps.edu.pl/cas/login',]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'rfalkowski@st.swps.edu.pl', 'password': 'Sepuku44!'},
            callback=self.after_login
        )

    def after_login(self, response):
        scrapy.Request(url="https://portal.swps.edu.pl/pl/group/student/home?swps_redirect_target=true", dont_filter=True)
        return scrapy.Request(url="https://zapisy.swps.edu.pl/study-program", dont_filter=True,callback=self.inside)
    
    def inside(self, response):
        # item = TitlesItem() 
        titles = response.xpath("//tr[@class='prog']/td[@class='c3']/text()").getall()
        for title in titles:
            item = TitlesItem()
            clean = title.removeprefix('\n    \t\t\t\t\t\t\t\t\t\t').removesuffix('\n    \t\t\t\t\t\t\t\t\t')
            item['name'] = clean
            yield item


        # item['name'] = response.xpath("//tr[@class='prog']/td[@class='c3']/text()").get()
        # return item
        # return {'title' : response.xpath("//tr[@class='prog']/td[@class='c3']/text()")}
    