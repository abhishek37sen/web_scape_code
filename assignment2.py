from bs4 import BeautifulSoup
from ruamel.yaml import YAML
from selenium import webdriver
import time

url='https://www.london.edu/executive-education/programme-search-results#sort=relevancy'

# chrome_d_p='D:\jigserv_assignment\assignment1\chromedriver'
driver=webdriver.Chrome('./chromedriver')
driver.get(url)
time.sleep(5)
html=driver.page_source

soup=BeautifulSoup(html,'html.parser')
soup_div=soup.find_all('div',class_='coveo-list-layout CoveoResult')
Program_title=[]
Program_URL=[]
try:
    for i in soup_div:
        Program_URL.append(str(i.a.get('href')))
        Program_title.append(str(i.a.string))
    dict_file=[{'a. Program_title':Program_title},{'b. Program_URL':Program_URL}]
except:
    print('something going wrong')
finally:
    driver.close()

class YamlObject(YAML):
    def __init__(self):
        YAML.__init__(self)
        self.default_flow_style = False
        self.block_seq_indent = 2
        self.indent = 4
        self.allow_unicode = True
        self.encoding = 'utf-8'
yaml=YamlObject()
with open('assignment4.yaml', 'w') as file:
    documents = yaml.dump(dict_file, file)
