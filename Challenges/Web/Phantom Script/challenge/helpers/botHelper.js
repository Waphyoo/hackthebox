const puppeteer = require('puppeteer');
const fs = require('fs');
let io; 
let isBotRunning = false; 
let browser; // Keep the browser instance
const flag = fs.readFileSync('/flag.txt', 'utf8');

// Initialize the browser once when the application starts
browser = puppeteer.launch({
  headless: true,
  executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || '/usr/bin/chromium-browser',
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-extensions',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding'
  ],
});

const visit = async (query) => {
  if (isBotRunning) {
    console.log('Bot is already running. Skipping new request.');
    return;
  }

  isBotRunning = true;

  let page;

  try {
    // Open a new page for each request
    page = await (await browser).newPage();

    console.log('New page opened successfully!');

    // Navigate to the URL
    await page.goto(`http://127.0.0.1:1337?q=${query}`, { waitUntil: 'domcontentloaded' });

    let alertHandled = false;

    // Check for alert dialogs using Puppeteer's page.on('dialog') event listener
    page.on('dialog', async (dialog) => {
      await dialog.accept();
      alertHandled = true;
      if (io) {
        io.emit('flag', { message: 'Alert detected!', flag: flag.trim() });
      }
      await page.close(); // Close the page after handling the alert
      isBotRunning = false; 
    });

    // Use setTimeout to wait for the alert to appear
    setTimeout(async () => {
      if (!alertHandled) {
        await page.close(); // Close the page if no alert was detected
        isBotRunning = false; 
      }
    }, 500); // 500ms wait before closing the page if no alert is handled

  } catch (e) {
    console.error(`Failed to navigate: ${e.message}`);
    if (page) {
      await page.close(); // Ensure the page is closed on error
    }
    isBotRunning = false; 
  }
};

// Setter function to initialize io
const setIo = (socketIoInstance) => {
  io = socketIoInstance;
};

module.exports = { visit, setIo };
