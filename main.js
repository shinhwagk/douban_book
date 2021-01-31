const puppeteer = require('puppeteer');
const fs = require('fs');

const tags = ['理财', '金融'];
(async () => {
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    // const tag = '金融'
    for (const tag of tags) {
        await getTags(tag, page)
    }
    await browser.close();
})();

async function getTags(tag, page) {
    let start = 0
    const BOOKURLS = [];
    while (true) {
        const bookUrls = await getTagUrls(page, tag, start)
        bookUrls.forEach(u => BOOKURLS.push(u))
        start += 20
        console.log(tag, start)
        if (bookUrls.length === 0) {
            break
        }
    }
    console.log(BOOKURLS, BOOKURLS.length)
    fs.writeFileSync(`tag_${tag}.json`, JSON.stringify(BOOKURLS), { encoding: 'utf8' })
}

async function getTagUrls(page, tag, start) {
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