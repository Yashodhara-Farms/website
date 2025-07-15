// index.js
const express = require('express');
const chromium = require('chrome-aws-lambda');
const app = express();

app.get('/bbScrape', async (req, res) => {
  const { keyword = 'ghee', page = 1 } = req.query;
  try {
    const browser = await chromium.puppeteer.launch({
      args: chromium.args,
      executablePath: await chromium.executablePath,
      headless: chromium.headless,
    });
    const pg = await browser.newPage();
    await pg.goto(
      `https://www.bigbasket.com/search/?q=${encodeURIComponent(keyword)}&page=${page}`,
      { waitUntil: 'networkidle2' }
    );
    const items = await pg.$$eval("div[qa='pname'] > a", els =>
      els.map(a => ({ title: a.innerText.trim(), url: a.href }))
    );
    await browser.close();
    res.set('Access-Control-Allow-Origin', '*'); // allow cross‑origin from Sheets
    res.json(items);
  } catch (err) {
    console.error(err);
    res.status(500).send({ error: err.toString() });
  }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Listening on ${PORT}`));
