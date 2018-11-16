
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import csv
import re


def get_html(url):
    r = requests.get(url)
    return r.text

    
#  получаем количество страниц с кандидатами
def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find_all('a', class_='item')[-3].get('title')
    total_pages = pages.split(' ')[1]
    #  pages.split('=')[1]
    return str(total_pages)


# поолучить список регионов
def get_regions(html):
    soup = BeautifulSoup(html, 'lxml')
    reg_list_raw = []
    reg_list = []
    regions_un = soup.find_all('select', class_='ui search dropdown')[1]
    s = int(len(regions_un))-87
    for rere in range(1, s):
        regions = regions_un.find_all('option')[rere].get('value')
        reg_list_raw.append(regions)
    for r in range(len(reg_list_raw)):
        s = reg_list_raw[r]
        a = re.sub(' +', '+', s)
        a = re.sub('\(+', '%28', a)
        a = re.sub('\)+', '%29', a)
        reg_list.append(a)
    return reg_list


#  записать в tsv файл
def write_tsv(data):
    with open('bio.tsv', 'a', encoding="utf-8") as t:
        t = csv.writer(t, delimiter='\t')
        t.writerow((data['name'],
                    data['b_date'],
                    data['was_chosen'],
                    data['nominations'],
                    data['education'],
                    data['job']))


# получить все ссылки на страницы кандитов
def get_data_url(html):
    soup = BeautifulSoup(html, 'lxml')
    total_links = []
    tl_urls = []
    links = soup.find_all('a', class_='b')
    for link in links:
        l = link.get('href')
        total_links.append(l)
    #  переход по ссылке кандидата с последующей выкачкой данных
    for tl in total_links:
        tl_url = 'https://candidates.golosinfo.org' + tl
        tl_urls.append(tl_url)
        # tl_html = get_html(tl_url)
        # c_page = BeautifulSoup(tl_url, 'lxml')
        # print(tl_html)
    return tl_urls

    
def main():
    #  r_url - ссылка на сайт кандидатов, {0} - номер страницы, {1} - регион для поиска
    url = 'https://candidates.golosinfo.org/p'
    r_url = 'https://candidates.golosinfo.org/p?page={0}&q%5Bdistr%5D=&q%5Bed%5D=&q%5Belvl%5D=&q%5Bgroup%5D=&q%5Bn%5D=&q%5Bp%5D=&q%5Br%5D={1}&q%5Bs%5D=&q%5Bsort%5D=&search=%D0%98%D1%81%D0%BA%D0%B0%D1%82%D1%8C&utf8=%E2%9C%93'
    html = get_html(url)
    reg = get_regions(html)
    b_links = []
    for i in reg:
        html = get_html(r_url.format('1', i))
        pages = get_pages(html)
        for page in pages:
            i_html = get_html(r_url.format(page, i))
            b_info = get_data_url(i_html)
            for b in b_info:
                b_html = get_html(b)
                b_soup = BeautifulSoup(b_html, 'lxml')
                b_soup = b_soup.find('div', class_='sixteen wide column')
                name = b_soup.find('div', class_='content').text[11:-9]
                b_date = b_soup.find('b').text
                bio_full = b_soup.find_all('div', class_='column')[0].find_all('p')
                was_chosen = bio_full[0].text.split('\n')[1][14:]
                nominations = bio_full[1].text.split('\n')[1][14:]
                education = bio_full[2].text.split('\n')[1][14:]
                job = bio_full[3].text.split('\n')[1][14:]
                out_data_bio = {'name': name,
                                'b_date': b_date,
                                'was_chosen': was_chosen,
                                'nominations': nominations,
                                'education': education,
                                'job': job}
                write_tsv(out_data_bio)
                #print(out_data_bio)


if __name__ == '__main__':
    main()
