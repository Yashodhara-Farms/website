import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


class SeleniumAnveshanSpider(scrapy.Spider):
    name = 'selenium_anveshan'
    allowed_domains = ['anveshan.farm']
    start_urls = ['https://www.anveshan.farm/collections/all']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 10

        # Scroll until products stop loading
        while scroll_attempts < max_scroll_attempts:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_height = new_height

        # Extract all product URLs from loaded page
        products = self.driver.find_elements(By.CSS_SELECTOR, 'a.full-unstyled-link')
        product_urls = list(set([p.get_attribute("href") for p in products if p.get_attribute("href")]))

        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        title = response.css('h1.product__title::text').get()
        price = response.css('span.price--large::text').get()
        description = response.css('div.product__description rte p::text').getall()
        ingredients = response.css('div[data-product-ingredients] p::text').getall()
        images = response.css('img.product__media-img::attr(src)').getall()

        yield {
            'url': response.url,
            'title': title,
            'price': price,
            'description': ' '.join(description).strip(),
            'ingredients': ', '.join(ingredients),
            'images': [response.urljoin(img) for img in images]
        }

    def closed(self, reason):
        self.driver.quit()
