import sys
import requests
import datefinder
import yaml
import re

from bs4 import BeautifulSoup

# print(sys.getrecursionlimit())
# sys.setrecursionlimit(15000)
# print(sys.getrecursionlimit())
from ruamel.yaml import YAML

url = 'https://www.gsb.stanford.edu/exec-ed/programs?pid=1283113613.1598246549'
def get_program_url(url):
    r= requests.get(url)
    htmlContent = r.content
    #print(htmlContent)
    soup =BeautifulSoup(htmlContent,'html.parser')
    #print(type(soup))
    soup_div= soup.find_all('div',class_='program-title')
    program_url=[]
    for soup_list in soup_div:
        #print(soup_list.a.string)
        a=soup_list.a.get('href')
        if a[0]== '/' :
            linkText = 'https://www.gsb.stanford.edu/'+a
            program_url.append(linkText)

    for i in range(3):
        program_url.pop()
    return program_url

#funtion for fetching  program fee
def get_program_fee(url):
    # print(url)
    program_fee=[]
    r =requests.get(url)
    ht_content = r.content
    soup =BeautifulSoup(ht_content,'html.parser')
    # print(soup.prettify)
    # print(soup_fee)
    soup_fee=soup.find('div',class_='main-middle')#
    # print((soup_fee))
    if soup_fee!=None:
        p_fee = (soup_fee.find_all('p'))
        for p in p_fee:
            if str(p.string).find('$')!=-1:
                program_fee.append(str(p.string[0:10]))
                break
    else:
        soup_fee=soup.find_all('div',class_='tuition-amount')
        # print(soup_fee)
        for i in soup_fee:
            if (str(i.string)).find('$')==-1:
                program_fee.append('TBD')
            else:
                program_fee.append(str(i.string))

    # print(program_fee)
    return program_fee

### Function for getting program start Date and program end Date, it return list.
### In this list index number 0 represent start Date end index number 1 represent End Date.
### Function take url as argument.
def get_program_date(pr_url):
    # print(pr_url)
    start_date = []
    end_date = []
    u=requests.get(pr_url)
    ht_content = u.content
    so=BeautifulSoup(ht_content,'html.parser')
    so_fee=so.find('div',class_='gsb-program-program-instance-fields')
    # print(so_fee)
    if so_fee!=None:
        h2=(so_fee.find_all('h2'))
        # print(type(h2))

        for i in h2:
            if str(i).find('TBD')==-1:
                # print(i)
                matches = list(datefinder.find_dates(str(i),source=True))
                # print(matches)
                if len(matches)>0:
                    start_date.append(matches[0][1])
                    end_date.append(matches[1][1])
                else:
                    start_date.append('TBD')
                    end_date.append('TBD')
            else:
                start_date.append('TBD')
                end_date.append('TBD')
    else:
        start_date.append('TBD')
        end_date.append('TBD')
    return [start_date,end_date]





def get_faculty_name(program_url):
    try:
        u = requests.get(program_url + '/faculty')
        ht_content = u.content
        so = BeautifulSoup(ht_content, 'html.parser')
        so_fac= so.find('div',class_='field field-name-field-faculty-1 field-type-field-collection field-label-hidden')
        if so_fac==None:
            so_faculty = so.find('div', class_='field field-name-field-other-name field-type-text field-label-hidden')
            # print(so_faculty.text)
        else:
            so_faculty = so.find('div', class_='field field-name-title field-type-ds field-label-hidden')
            # print(so_faculty.text)
        return str(so_faculty.text)
    except:
        try:
            u=requests.get(program_url+'/faculty')
            ht_content = u.content
            so=BeautifulSoup(ht_content,'html.parser')
            so_faculty=so.find('div',class_='field field-name-title field-type-ds field-label-hidden')
            # print(so_faculty.text)
            return str(so_faculty.text)
        except:
            u=requests.get(program_url)
            ht_content=u.content
            so=BeautifulSoup(ht_content,'html.parser')
            so_faculty=so.find('div',class_='person-name')
            # print(so_faculty.text)
            return str(so_faculty.text)



def get_faculty_img(pr):
    print(end='.')
    u=requests.get(pr+'/faculty')
    ht_content = u.content
    so=BeautifulSoup(ht_content,'html.parser')
    try:
        so_faculty=so.find('div',class_='ds-1col entity entity-field-collection-item field-collection-item-field-faculty-directors view-mode-full')
        if so_faculty!=None:
            pass
            # print('Image url:   ', so_faculty.img['src'])
        else:
            so_faculty=so.find('div',class_='ds-1col entity entity-field-collection-item field-collection-item-field-faculty-1 view-mode-full')
            if so_faculty!=None:
                pass
                # print('Image url:   ',so_faculty.img['src'])
            else:
                u=requests.get(pr)
                # print(pr)
                ht_content=u.content
                so=BeautifulSoup(ht_content,'html.parser')
                so_faculty=so.find('div',class_='person-list-view')
                # print('Image url:   ', so_faculty.img['src'])
        return (so_faculty.img['src'])
    except:
        print('Sorry we could not fetch data')



program_url=(get_program_url(url))
program_url.sort()

program_url_wo_d=list(dict.fromkeys(program_url))

program_fee=[]
print('Fetching program Fee',end='.')
for pr in program_url_wo_d:
    print(end='.')
    program_fee.extend(get_program_fee(pr))
print()


start_date = []
end_date = []
print('Fetching program Date.',end='.')
for pr_url in program_url_wo_d:
    print(end='.')
    data=get_program_date(pr_url)
    start_date.extend(data[0])
    end_date.extend(data[1])
# print(start_date,'\n',end_date)
print()

faculty_name=[]
print('Fetching program faculty Name',end='.')
for pr in program_url:
    print(end='.')
    faculty_name.append(get_faculty_name(pr))
print()


faculty_img=[]
print('Fetching Faculty img',end='.')
for pr in program_url:
    faculty_img.append(get_faculty_img(pr))
print()

class YamlObject(YAML):
    def __init__(self):
        YAML.__init__(self)
        self.default_flow_style = False
        self.block_seq_indent = 2
        self.indent = 4
        self.allow_unicode = True
        self.encoding = 'utf-8'
yaml=YamlObject()
program_fee[9]=program_fee[9].replace('\u200b','')

dict_file=[{'a. Program_URL':program_url},{'b. Start Date':start_date},{'c. End Date':end_date},{'d. Faculty Name':faculty_name},{'e. Faculty Image':faculty_img},{'f. Program Fee':program_fee}]
with open('assignment3.yaml', 'w') as file:
    documents = yaml.dump(dict_file, file)
