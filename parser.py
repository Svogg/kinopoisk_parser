import csv
import re
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

URL = 'https://www.kinopoisk.ru/lists/series-top250/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 '
                  'Safari/537.36',
    'accept': '*/*'
}


def get_html(url):
    browser = webdriver.Chrome(
        executable_path=r'chrome_driver/chromedriver.exe')  # Исправить путь к драйверу
    browser.get(url)
    time.sleep(17)
    browser.find_element(By.XPATH,
                         '/html/body/div[1]/div/div[2]/div[4]/div[2]/div[2]/div[1]/div/aside/div[2]/div[3]/div/div[2]'
                         ).click()
    time.sleep(5)
    return browser.page_source


def get_lst_key(html):
    soup = BeautifulSoup(html, 'html.parser')
    result_names = soup.find_all('div', class_='selections-select__dropdown-wrapper')
    lst_keys = []
    for url in result_names:
        lst_keys = (re.sub('<[^>]+>', ' ', str(url)).lower().split())[2:]
    return lst_keys


def get_lst_value():
    result_lst = []
    list_of_links = ['https://www.kinopoisk.ru/lists/series-top250/?page=1&tab=all',
                     'https://www.kinopoisk.ru/lists/series-top250/?page=2&tab=all',
                     'https://www.kinopoisk.ru/lists/series-top250/?page=3&tab=all',
                     'https://www.kinopoisk.ru/lists/series-top250/?page=4&tab=all',
                     'https://www.kinopoisk.ru/lists/series-top250/?page=5&tab=all']
    for link in list_of_links:
        html = get_html(link)
        time.sleep(5)
        soup = BeautifulSoup(html, 'html.parser')
        lst = soup.find_all('span', class_='selection-film-item-meta__meta-additional-item')
        lst_values = []
        for value in lst:
            lst_values += [re.sub('<[^>]+>', '', str(value)).split()]
        lst_values_test = [lst_values[i] for i in range(len(lst_values)) if i % 2 != 0]
        lst_values_test = [value[0][:len(value[0]) - 2] if len(value) == 2 else value[0][:len(value[0]) - 1] for value in lst_values_test]
        result_lst += lst_values_test
    return result_lst


def calculate():
    html = get_html(URL)
    dict_keys = {el: 0 for el in get_lst_key(html)}
    spes_dict_keys = {el[:len(el) - 1]: 0 for el in dict_keys.keys()}
    lst = get_lst_value()
    for i in range(len(lst)):
        if lst[i] == 'боеви':
            lst[i] = 'боевик'
        if lst[i] == 'детекти':
            lst[i] = 'детектив'
        if lst[i] == 'мультфиль':
            lst[i] = 'мультфильм'
        if lst[i] == 'мюзик':
            lst[i] = 'мюзикл'
        if lst[i] == 'трилле':
            lst[i] = 'триллер'
    for k, v in spes_dict_keys.items():
        for el in lst:
            if k == el:
                spes_dict_keys[k] += 1
    keys = list(dict_keys.keys())
    values = list(spes_dict_keys.values())
    res = dict()
    for idx in range(len(keys)):
        res[keys[idx]] = values[idx]
    return res


def dict_to_csv(dict):
    with open('statistic.csv', 'w', newline='') as statisic:
        field_names = ['genre', 'amount']
        writer = csv.DictWriter(statisic, fieldnames=field_names)
        writer.writeheader()
        for k, v in dict.items():
            writer.writerow({field_names[0]: k, field_names[1]: v})
    pass


def main():
    statistic_dict = calculate()
    dict_to_csv(statistic_dict)
    
    
main()
