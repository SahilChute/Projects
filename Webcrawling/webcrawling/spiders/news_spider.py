# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor

#https://www.hindustantimes.com/india-news/farmers-say-govt-using-brute-force-we-dont-want-to-clash-10-points-101707896375822.html
#https://www.hindustantimes.com/world-news/us-news/prince-harry-and-meghan-markles-team-defend-sussexes-new-website-say-its-their-name-101707904884187.html
#https://www.hindustantimes.com/cricket/sri-lanka-vs-afghanistan-live-score-3rd-odi-of-afghanistan-tour-of-sri-lanka-2024-final-updates-today-14-feb-2024-101707898164651.html
#https://www.hindustantimes.com/photos/news/tear-gas-barbed-wires-cement-blocks-delhis-security-up-against-farmers-protest-in-pics-101707829576667.html
#https://www.hindustantimes.com/entertainment/bollywood/shah-rukh-khan-james-bond-too-short-world-government-summit-2024-dubai-101707897372751.html
#https://www.hindustantimes.com/education/competitive-exams/ap-set-2024-registration-begins-on-apset-net-in-link-to-apply-101707905022830.html


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "newscrawler"
    allowed_domains = ["hindustantimes.com"]
    start_urls = ["https://www.hindustantimes.com/"]

    rules = (
        Rule(LinkExtractor(allow=('india-news')), callback='parse_item'),
    )

    def parse_item(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "date": response.css(".dateTime::text").get(),
            "Body": response.css(".storyParagraphFigure p::text").get(),
            "image_src" : response.css("figure img::attr(src)").get(),
            "caption" : response.css("figcaption::text").get(),
        }


