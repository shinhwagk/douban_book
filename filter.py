import os
import csv
import json


with open('all_books.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['分类', '序列号', '书名', '评分', '人数', '简介'])
    for tag in os.listdir('books'):
        with open(f'books/{tag}', 'r', encoding='utf-8') as f:
            books = json.load(f)
        try:
            for b in books:
                c0 = tag[:-5]
                c1 = b[0]
                c2 = b[1].replace('\n', '').strip()
                c3 = b[2]
                c4 = b[3].replace('\n', '').strip()
                c5 = b[4].replace('\n', '').strip()
                if type(c3) == 'str' and len(c3) == 0:
                    c3 = 0
                elif type(c3) == 'str':
                    c3 = int(c3)
                writer.writerow([c0, c1, c2, c3, c4, c5])
        except Exception as e:
            print(tag, b, e)
