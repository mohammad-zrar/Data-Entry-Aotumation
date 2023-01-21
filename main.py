from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfrvBDykaBliTJ2G8dHtlg23Iw7-3z5kjvDf1JXkgI0h7fjzA/viewform?usp=sf_link"
zillow_URL = "https://www.zillow.com"
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
header = {"Accept-Language": "en-GB,en;q=0.9,ar-AE;q=0.8,ar;q=0.7,en-US;q=0.6,fa;q=0.5,zh-CN;q=0.4,zh;q=0.3",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
CHROME_DRIVER_PATH = r"C:\Users\mzrar\.wdm\drivers\chromedriver\win32\104.0.5112\chromedriver.exe"


response = requests.get(URL, headers=header)
# print(response)

soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())
info_list = []

list_items = soup.select(".List-c11n-8-69-2__sc-1smrmqp-0 li")
count = 0
for li in list_items:
    if li.find("a") is not None:
        # #### LINK #### #
        link = li.find("a")
        if link["href"][:len(zillow_URL)] != zillow_URL:
            link = zillow_URL + link["href"]
        else:
            link = link["href"]
        # print(link)
        # ######## #
        # #### PRICES #### #
        price = li.select("[data-test=property-card-price]")[0].text.split("+")[0]
        # print(price)
        # ######## #
        # #### ADDRESS #### #
        address = li.select("address")[0].text
        # print(address)
        # ######## #
        info_list.append([link, price, address])

for info in info_list:
    print(info)

for info in info_list:
    time.sleep(5)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    driver.get(FORM_URL)
    time.sleep(5)
    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(info[0])
    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(info[1])
    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(info[2])
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
    time.sleep(5)
    driver.close()
