const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({
    headless: false
  });

  const page = await browser.newPage();

  await page.goto("https://yandex.com/images/");

  console.log("Yandex Images opened");

  await page.waitForTimeout(15000);

  await browser.close();
})();
