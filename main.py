import time
import requests
import random
from bs4 import BeautifulSoup
from openpyxl import Workbook


# Some User Agents
hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]


def book_spider(book_tag):
    page_num = 0
    book_list = []

    while(True):
        url = "http://www.douban.com/tag/{}?start={}&type={}".format(
            book_tag, page_num*20, 'T')

        try:
            r = requests.get(url, headers=hds[page_num % len(hds)])
            plain_text = r.text
            print(len(plain_text))
        except Exception as e:
            print(e)
            continue

        soup = BeautifulSoup(plain_text, "html.parser")
        books = soup.find_all('li', {'class', 'subject-item'})
        print(book_tag, page_num, len(books))
        if len(books) == 0:
            break

        for b in books:
            book_url = b.find('a').get('href')
            print(book_url)
            name, rating, people_num, info = get_book_info(book_url)

            book_list.append(
                [name, rating, people_num, info])
            time.sleep(random.random()*5)
        page_num += 1
        print('Downloading Information From Page %d' % page_num)
        time.sleep(random.random()*5)
    return book_list


def get_book_info(url):
    try:
        r = requests.get(url, headers=hds[random.randint(0, len(hds))])
        plain_text = r.text
    except Exception as e:
        print(e)
    soup = BeautifulSoup(plain_text, "html.parser")
    name = soup.find('div', id='wrapper').find('h1').find('span').get_text()
    rating = soup.find('strong', {'class': 'll rating_num'}).get_text()
    people_dom = soup.find('a', {'class': 'rating_people'})
    # people_num = soup.find('div', {'class': 'rating_sum'}).findAll('span')[
    #     1].string.strip()
    people_num = "0"
    if people_dom is None:
        people_num = 0
    else:
        people_num = people_dom.find('span').get_text()
    info = soup.find('div', id="info").get_text()
    return [name, rating, people_num, info]


# def get_people_num(url):
#     # url='http://book.douban.com/subject/6082808/?from=tag_all' # For Test
#     try:
#         r = requests.get(url, headers=hds[random.randint(0, len(hds))])
#         plain_text = r.text
#     except Exception as e:
#         print(e)
#     soup = BeautifulSoup(plain_text)
#     people_num = soup.find('div', {'class': 'rating_sum'}).findAll('span')[
#         1].string.strip()
#     return people_num


def do_spider(book_tag_lists):
    book_lists = []
    for book_tag in book_tag_lists:
        book_list = book_spider(book_tag)
        book_list = sorted(book_list, key=lambda x: x[1], reverse=True)
        book_lists.append(book_list)
    return book_lists


def print_book_lists_excel(book_lists, book_tag_lists):
    wb = Workbook()
    ws = []
    for i in range(len(book_tag_lists)):
        # utf8->unicode
        ws.append(wb.create_sheet(title=book_tag_lists[i]))
    for i in range(len(book_tag_lists)):
        ws[i].append(['序号', '书名', '评分', '评价人数', '作者', '出版社'])
        count = 1
        for bl in book_lists[i]:
            ws[i].append([count, bl[0], float(bl[1]),
                          int(bl[2]), bl[3], bl[4]])
            count += 1
    save_path = 'book_list'
    for i in range(len(book_tag_lists)):
        save_path += ('-'+book_tag_lists[i].decode())
    save_path += '.xlsx'
    wb.save(save_path)


if __name__ == '__main__':
    # book_tag_lists = ['心理','判断与决策','算法','数据结构','经济','历史']
    # book_tag_lists = ['传记','哲学','编程','创业','理财','社会学','佛教']
    # book_tag_lists = ['思想','科技','科学','web','股票','爱情','两性']
    # book_tag_lists = ['计算机','机器学习','linux','android','数据库','互联网']
    # book_tag_lists = ['数学']
    # book_tag_lists = ['摄影','设计','音乐','旅行','教育','成长','情感','育儿','健康','养生']
    # book_tag_lists = ['商业','理财','管理']
    book_tag_lists = ['名著']
    # book_tag_lists = ['科普','经典','生活','心灵','文学']
    # book_tag_lists = ['科幻','思维','金融']
    # book_tag_lists = ['个人管理', '时间管理', '投资', '文化', '宗教']
    book_lists = do_spider(book_tag_lists)
    # print_book_lists_excel(book_lists, book_tag_lists)
