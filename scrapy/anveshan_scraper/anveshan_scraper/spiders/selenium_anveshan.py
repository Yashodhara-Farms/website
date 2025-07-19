import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SeleniumAnveshanSpider(scrapy.Spider):
    name = 'selenium_anveshan'
    allowed_domains = ['anveshan.farm']
    start_urls = ['https://www.anveshan.farm/collections/all']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=chrome_options)

    def smooth_scroll(self, pause=0.3, step=300):
        """
        Simulates user-like scrolling by scrolling in small steps and waiting briefly.
        """
        scroll_pos = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while scroll_pos < last_height:
            scroll_pos += step
            self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            time.sleep(pause)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height > last_height:
                last_height = new_height  # Page expanded, continue scrolling


    def parse(self, response):
        self.logger.info("🌐 Loading main page...")
        self.driver.get("https://www.anveshan.farm/collections/all-products")
        time.sleep(5)

        self.smooth_scroll(pause=0.2, step=400)
        time.sleep(3)  # allow time for JS to inject more items
        
        products = self.driver.find_elements(By.CSS_SELECTOR, 'li.grid__item')
        current_count = len(products)
        self.logger.info(f"🧾 {current_count} products loaded so far")

        pdp_urls = []
        for product in products:
            try:
                link_elem = product.find_element(By.CSS_SELECTOR, 'a')
                relative_url = link_elem.get_attribute('href')
                if relative_url:
                    pdp_urls.append(relative_url)
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to extract link: {e}")

        self.logger.info(f"✅ Collected {len(pdp_urls)} product URLs")

        for url in pdp_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)


    def parse_product(self, response):
        self.driver.get(response.url)
        time.sleep(3)
        sel = Selector(text=self.driver.page_source)

        title = sel.css('h1.product__title::text').get()
        price = sel.css('span.price::text').get()
        image_url = sel.css('img.product__media-image::attr(src)').get()
        description = sel.css('div.product__description').xpath('string()').get()

        yield {
            'url': response.url,
            'title': title.strip() if title else '',
            'price': price.strip() if price else '',
            'image_url': response.urljoin(image_url) if image_url else '',
            'description': description.strip() if description else ''
        }

    def closed(self, reason):
        self.logger.info("Closing Selenium driver")
        self.driver.quit()
