from bs4 import BeautifulSoup

book_list = ""
with open('book_list.html') as f:
    book_list = f.read()

book_info = ""
with open('book_info.html') as f:
    book_info = f.read()

# print(book_info)


# soup = BeautifulSoup(book_list, "html.parser")
# for book_info in soup.find_all('li', {'class', 'subject-item'}):
#     print(book_info.find('a').get('href'))

soup2 = BeautifulSoup(book_info, "html.parser")
name = soup2.find('div', id='wrapper').find('h1').find('span').get_text()
print(name)
# rating = soup2.find('strong', {'class': 'll rating_num'}).get_text()
# people_num = soup2.find('a', {'class': 'rating_people'})


# if people_num is None:
#     people_num = 0
# else:
#     people_num = people_num.get_text()
# auther = soup2.find('div', id="info").get_text()
# auther2 = soup2.find('div', id="info").find('span').find_all('a')
# auther3 = [x.get_text() for x in auther2]
# info = soup2.find('div', id="info").find('br').get_text()

# print(name, rating, people_num, auther,  info)
# # print(soup2.find('div', id="info").find('br').get_text())
# # for book_info in soup.find_all('li', {'class', 'subject-item'}):
# #     print(book_info.find('a').get('href'))
