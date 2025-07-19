import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.anveshan.farm/products/a2-desi-ghee?variant=32459662590030",
        "https://www.anveshan.farm/products/gir-cow-ghee?variant=43355933245632",
        "https://www.anveshan.farm/products/a2-desi-ghee?variant=32459662590030",
        "https://www.anveshan.farm/products/gir-cow-ghee",
        "https://www.anveshan.farm/products/a2-desi-ghee",
        "https://www.anveshan.farm/products/kashmiri-mongra-saffron?variant=43376001188032",
        "https://www.anveshan.farm/products/millet-health-mix-sachets-strawberry-flavour-with-20-natural-superfoods",
        "https://www.anveshan.farm/products/wood-pressed-groundnut-oil?variant=43844700340416",
        "https://www.anveshan.farm/products/moringa-sattu-drink-mix-sachets-jaljeera-flavour",
        "https://www.anveshan.farm/products/a2-ghee-mustard-oil?variant=42819454468288",
        "https://www.anveshan.farm/products/wood-pressed-mustard-oil?variant=43844702404800",
        "https://www.anveshan.farm/products/a2-desi-ghee-combo",
        "https://www.anveshan.farm/products/kashmiri-mongra-saffron",
        "https://www.anveshan.farm/products/a2-ghee-groundnut-oil?variant=42819383984320",
        "https://www.anveshan.farm/products/ghee-honey-combo",
        "https://www.anveshan.farm/products/diwali-gift-box-a-flavourful-festivity",
        "https://www.anveshan.farm/products/hallikar-ghee-and-gir-ghee-combo",
        "https://www.anveshan.farm/products/a2-ghee-groundnut-oil",
        "https://www.anveshan.farm/products/a2-desi-ghee-combo?variant=37347042328768",
        "https://www.anveshan.farm/products/desi-buffalo-ghee",
        "https://www.anveshan.farm/products/wood-pressed-groundnut-oil?variant=30393551323214",
    ]

    def parse(self, response):
        for product in response.css('section.product__info-container'):
            description = product.css('div.product__description p::text').get()
            description_parts = []
            if not description:
                descriptionAray = product.css('div.product__description p span::text').getall()
                for desc in descriptionAray:
                    if desc.strip():
                        description_parts.append(desc.strip())
                
            else:
                description_parts.append(description)
            yield {
                "title": product.css('div.product__title h1::text').get(),
                "regular-price": product.css('div.price__sale span s.price-item--regular::text')[1].get(),
                "sale-price": product.css('div.price__sale span.price-item--sale::text')[1].get(),
                "description": description_parts,
                # "image": product.css('div.product__media img::attr(src)').get(),
                "url": response.url,

            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)