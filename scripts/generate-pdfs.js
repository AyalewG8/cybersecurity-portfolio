const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const outputDir = path.join(process.cwd(), 'assets');
  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const documents = [
    ['resume.html', 'Ayalew_Cherenet_Resume.pdf'],
    ['portfolio-overview.html', 'Ayalew_Cherenet_Portfolio.pdf']
  ];

  for (const [source, output] of documents) {
    await page.goto(`file://${path.join(process.cwd(), source)}`, { waitUntil: 'networkidle' });
    await page.pdf({
      path: path.join(outputDir, output),
      format: 'Letter',
      printBackground: true,
      margin: { top: '0.25in', right: '0.25in', bottom: '0.25in', left: '0.25in' }
    });
  }

  await browser.close();
})();