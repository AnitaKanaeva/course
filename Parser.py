
# coding: utf-8



import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text

    
#  получаем количество страниц с кандидатами
def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find_all('a', class_='item')[-1].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


# поолучить список регионов
def get_regions(html):
    soup = BeautifulSoup(html, 'lxml')
    reg_list = []
    regions_un = soup.find_all('select', class_ = 'ui search dropdown')[1]
    s = int(len(regions_un))-87
    for rere in range(1,s):
        regions = regions_un.find_all('option')[rere].get('value')
        reg_list.append(regions)
    return reg_list

#  записать в tsv файл


def write_tsv(html):
    with open('bio.tsv','wt',encoding="utf-8") as t:
        t.write('id    name    date_of_birth    was_chosen    nominations    education    job'+'\n')
        #  ...будет дописываться, возможно заменится на csv
        #  pandas


def get_data_bio(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a', class_='b')
    #  в процессе, для начала надо решить вопрос с подстановкой в ссылку
    return links

    
def main():
    #  r_url - ссылка на сайт кандидатов, {0} - номер страницы, {1} - регион для поиска
    #  надо придумать, как подставить регион в ссылку
    #  в ссылке регион выглядит как-то так: Архангельская+область
    #  в chrome можно писать ссылки прямо как в примере, если не заработает, надо будет перевести в вид %D0%90 и т.д.
    r_url = 'https://candidates.golosinfo.org/p?page={0}&q%5Bdistr%5D=&q%5Bed%5D=&q%5Belvl%5D=&q%5Bgroup%5D=&q%5Bn%5D=&q%5Bp%5D=&q%5Br%5D={1}&q%5Bs%5D=&q%5Bsort%5D=&search=%D0%98%D1%81%D0%BA%D0%B0%D1%82%D1%8C&utf8=%E2%9C%93'
    html = get_html(url)
    reg = get_regions(html)
    #  pages = get_pages(html)
    #  b_links = get_data_bio(html)
    print(reg)
    

if __name__ == '__main__':
    main()