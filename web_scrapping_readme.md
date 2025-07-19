# Web Scraping Environment Setup for Yashodhara

This guide explains how to set up and run the Python-based web scraping environment for the **Yashodhara** project on the `web-scrapping` branch.

## 🧪 Python Environment Setup

### 1. Activate the Virtual Environment

```bash
source Documents/Yashodhara/scrapy/yashodhara/bin/activate
```

✅ You should see the environment prefix in your shell:

```bash
(yashodhara) Deepaks-MacBook-Air:~ deepakverma$
```

### 2. Deactivate the Virtual Environment

To exit the environment:

```bash
deactivate
```

### 3. Alias for Activation (Optional)

Add the following alias to your `.zshrc` or `.bash_profile`:

```bash
alias activate-yashodhara='source ~/Documents/Yashodhara/scrapy/yashodhara/bin/activate'
```

Then simply run:

```bash
activate-yashodhara
```

---

## 🚀 Running the Scraper

To run the Selenium-based spider that scrapes products from Anveshan:

```bash
scrapy crawl selenium_anveshan -o all_products.json -s LOG_LEVEL=INFO
```

This will:

- Scroll the listing page to load all products
- Collect product URLs
- Visit each Product Detail Page (PDP)
- Extract required product data

## 🔍 Source URL

We scrape products from this Anveshan listing page:

🔗 [https://www.anveshan.farm/collections/all](https://www.anveshan.farm/collections/all)

---

## 📋 Fields Scraped from PDP

Each product page scrapes the following fields:

- `title`
- `price`
- `description`
- `image_urls`
- `ingredients`
- `usage_instructions`
- `benefits`
- `rating`
- `reviews_count`
- `variant_info` (if applicable)

---

## 🛠 Dependencies (Installed in Virtual Env)

- `scrapy`
- `selenium`
- `beautifulsoup4`
- `chromedriver-autoinstaller`

---

For questions, reach out to the development team or refer to the Jira ticket: `YOF-003 Web Scraper (Completed)`

