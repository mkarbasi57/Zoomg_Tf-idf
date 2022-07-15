import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv

#find last page number
def GetLastPageNumber():
    webpage = requests.get('https://www.zoomg.ir/')

    webpage = webpage.text

    soup = BeautifulSoup(webpage, 'lxml')
    #read page btn tag
    course_cards = soup.find_all('ul', class_="pagination")
    #splite btn from their tag and 6th is the last page.
    page = str(course_cards).split('<li>')
    #use regex to get number
    s = re.search('/page/(.*?)/\"',page[5]).group(1)
    s = int(s)
    return s

rows = []

def scrap(page_number):
    #base url request
    webpage = requests.get('https://www.zoomg.ir/page/{}/'.format(page_number))

    webpage = webpage.text

    soup = BeautifulSoup(webpage, 'lxml')
    #scrape all news of current page
    titr = soup.find_all('div',class_="Contents col-md-8 col-sm-8 col-xs-8")
    for t in titr:
        title = t.h3.text
        link = t.h3.a['href']
        author = t.ul.li.a.text
        definition = t.p.text
        author_link = t.ul.li.a['href']
        row = [title, definition, link, author, author_link]
        rows.append(row)


def main():
    fields = ['Title', 'Defination', 'Link', 'Author', 'Author_link']
    filename = "zoomg.csv"

    LastPageNumber = GetLastPageNumber()
    print("Total page to scrape: {}".format(LastPageNumber))
    #scraping(2,fields)
    for page_number in tqdm(range(1,LastPageNumber)):
        scrap(page_number)

    with open(filename, 'w',encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

main()