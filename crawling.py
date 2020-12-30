from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
from slugify import slugify


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)

FEED_URL =  'https://news.detik.com/indeks'

driver.get(FEED_URL)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

media_links  = soup.find_all("a", class_="media__link")
for link in media_links:
    if not os.path.exists('./corpus'):
        os.makedirs('./corpus')
    print(link['href'])
    driver.get(link['href'])
    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, 'html.parser')
    body = soup.find('div', class_="detail__body-text")
    if body :
        with open('./corpus/'+slugify(link.contents[0])+'.txt','a') as file :
            file.write(f"<link>{link['href']}</link> \n")
            file.write(f"<title>{link.contents[0]}</title> \n")
            file.write(body.text.strip())
driver.quit()

