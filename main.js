const puppeteer = require('puppeteer');
const fs = require('fs');

// const tags = ['理财', '金融'];

(async () => await main())();

async function main() {
    const argTag = process.argv[2]
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    await getTags(argTag, page)
    await browser.close();
}

async function getTags(tag, page) {
    const BOOKURLS = [];
    while (true) {
        const start = BOOKURLS.length
        const books = await getTagBooks(page, tag, start)
        console.log(tag, start)
        if (books.length === 0) {
            break
        }
        books.forEach(u => BOOKURLS.push(u))
    }
    console.log(BOOKURLS, BOOKURLS.length)
    fs.writeFileSync(`tag_${tag}.json`, JSON.stringify(BOOKURLS), { encoding: 'utf8' })
}

async function getTagBooks(page, tag, start) {
    await page.goto(`https://book.douban.com/tag/${tag}?start=${start}`, { waitUntil: 'networkidle2' });
    return await page.evaluate(() => {
        const urls = []
        for (const i of [...document.querySelectorAll('li[class="subject-item"] div[class="pic"] a')]) {
            urls.push(i.href)
        }
        return urls
    });
}

async function getBookInfo(page) {
    // const info ={name}
    return await page.evaluate(() => {
        const name = document.querySelector('body div[id="wrapper"] h1 span').innerText
        // document.querySelector('div[id="content"] ')
        const rate = document.querySelector('strong[class="ll rating_num "]').innerText
        const people = document.querySelector('a[class="rating_people"] span').innerText
        // const author = document.querySelector('div[id="info"] span a').innerText
        const info = document.querySelector('div[id="info"]').innerText
        return { name, rate, people, info }
    });

}