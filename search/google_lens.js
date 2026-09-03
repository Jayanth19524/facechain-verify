const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const browser = await chromium.launch({
    headless: false
  });

  const page = await browser.newPage();

  await page.goto("https://yandex.com/images/");

  // Open visual search
  await page.locator('button').filter({ hasText: '' }).nth(0).click();

  await page.waitForTimeout(2000);

  const fileInput = page.locator('input[type="file"]');

  await fileInput.setInputFiles(
    path.resolve("samples/face.jpg")
  );

  console.log("Image uploaded");

  await page.waitForTimeout(30000);

  await browser.close();
})();