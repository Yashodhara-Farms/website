import scrapy
from scrapy_splash import SplashRequest


class AnveshanSpider(scrapy.Spider):
    name = "anveshan"
    allowed_domains = ["anveshan.farm"]
    start_urls = ["https://www.anveshan.farm/collections/all"]

    script = """
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(2))

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")

        local prev_height = 0
        local current_height = get_body_height()

        for i = 1, 10 do
            scroll_to(0, current_height)
            assert(splash:wait(2))
            prev_height = current_height
            current_height = get_body_height()

            if current_height == prev_height then
                break
            end
        end

        return { html = splash:html() }
    end
    """

    def start_requests(self):
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse,
            endpoint="execute",
            args={'lua_source': self.script},
        )

    def parse(self, response):
        products = response.css('div.grid__item')
        for product in products:
            title = product.css('.product-title::text').get()
            price = product.css('.price--highlight span::text').get()
            link = product.css('a.full-unstyled-link::attr(href)').get()
            image = product.css('img::attr(src)').get()

            yield {
                'title': title.strip() if title else None,
                'price': price.strip() if price else None,
                'link': response.urljoin(link) if link else None,
                'image': response.urljoin(image) if image else None
            }
