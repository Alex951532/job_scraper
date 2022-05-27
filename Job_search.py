from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
import requests
import re
import math
import pandas as pd
import numpy as np
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M")

url = "https://www.helloworld.rs/oglasi-za-posao/python"
#url = "https://www.helloworld.rs/oglasi-za-posao/"

page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#Broj oglasa / broj oglasa po stranici
def count_posts_per_page():
    posts_per_page=0
    posts_per_page_raw=doc.find_all(class_="relative bg-white dark:bg-gray-800 shadow-md rounded-md")
    for i in posts_per_page_raw:
        posts_per_page=posts_per_page+1
    #print(str(posts_per_page)+" posts per page")

    return posts_per_page

def count_posts():
    post_count_raw = doc.find_all(text=re.compile('\([0-9]+ [A-z]+\)'))
    post_count = int(re.compile('[0-9]+').findall(str(post_count_raw))[0])
    #print(str(post_count) + " posts")

    return post_count


def page_count():
    page_count = count_posts()/count_posts_per_page()
    return int(math.ceil(page_count))

def fix_button(button):
    button=str(button)
    button=button.replace(" ","-")
    button=button.replace(">"," ")
    button=button.replace("<"," ")
    button=button.split(" ")

    for word in button:
        if word in ["Junior","Intermediate","Senior"]:
            return word

def get_all_page_post_info():
    global jobs
    for i in range(count_posts_per_page()):
        try:
            posts_per_page_raw=doc.find_all(class_="relative bg-white dark:bg-gray-800 shadow-md rounded-md")
        except:
            posts_per_page_raw="NaN"
        try:
            postition=posts_per_page_raw[i].find(class_="hover:opacity-50 font-bold text-lg").string
        except:
            postition="NaN"
        try:
            company=posts_per_page_raw[i].find("h4").a.string
        except:
            company="NaN" 
        try:
            description=posts_per_page_raw[i].find(class_="text-sm opacity-90").string
        except:
            description="NaN" 
        try:
            location=posts_per_page_raw[i].find(class_="las la-map-marker text-lg leading-none").next_sibling.next_sibling.text
        except:
            location="NaN"
        try:
            end_date=posts_per_page_raw[i].find(class_="las la-clock text-lg leading-none").next_sibling.next_sibling.text
        except:
            end_date="NaN"
        try:
            student_support=False
            available_to=posts_per_page_raw[i].find(class_="las la-graduation-cap")
            if available_to: 
                student_support=(True)
        except:
            student_support=False
        try:
            disabled_support=False
            available_to=posts_per_page_raw[i].find(class_="las la-wheelchair")
            if available_to: 
                disabled_support=(True)
        except:
            disabled_support=False
        try:
            online_interview=False
            available_to=posts_per_page_raw[i].find(class_="las la-microphone text-lg leading-none")
            if available_to: 
                online_interview=(True)
        except:
            online_interview=False
        try:
            tags=[]
            for tag in posts_per_page_raw[i].find_all(class_="btn btn-xs btn-primary jobtag __jobtag w-auto"):
                tags.append(tag.find("span").string)
        except:
            tags=["NaN"]
        try:
            seniority=[]
            for position in posts_per_page_raw[i].find_all(class_="flex items-center gap-2 flex-wrap"):
                buttons = position.find_all("button",class_=re.compile('(btn __quick_senioritet btn-xs btn-primary senioritet-[\d] w-auto)'))
                for status in buttons:
                    seniority.append(fix_button(status))
        except:
            seniority=seniority.append("")
        try:
            if posts_per_page_raw[i].find(class_="flex flex-wrap items-center justify-center gap-2").text:
                premium=True
        except:
            premium=False
        try:
            link=posts_per_page_raw[i].find(class_="hover:opacity-50 font-bold text-lg")["href"]
            link="https://www.helloworld.rs/" + str(link)
        except:
            link="NaN" 
        
        print(postition.strip())
        print(company.strip())
        print(description.strip())
        print(location)
        print(end_date)
        print(student_support)
        print(disabled_support)
        print(online_interview)        
        print(tags)
        print(seniority)
        print(premium)
        print(link)
        print("---------------------------------------------------------")
        global data_global

        data_global['Position'].append(postition.strip())
        data_global['Company'].append(company.strip())
        data_global['Description'].append(description.strip())
        data_global['Location'].append(location)
        data_global['Vaild until'].append(end_date)
        data_global['Student Support'].append(student_support)
        data_global['Disabled Support'].append(disabled_support)
        data_global['Online Interview'].append(online_interview)
        data_global['Tags'].append(tags)
        data_global['Seniority'].append(seniority)
        data_global['Premium'].append(premium)
        data_global['Link'].append(link)

        jobs=jobs+1


data_global = {'Position':[],
        'Company':[],
        'Description':[],
        'Premium':[],
        'Location':[],
        'Vaild until':[],
        'Student Support':[],
        'Disabled Support':[],
        'Online Interview':[],
        'Tags':[],
        'Seniority':[],
        'Link':[]
        }


jobs = 0
get_all_page_post_info()
for i in range(page_count()):
    try:
        link=doc.find(class_="las la-angle-right text-lg").parent["href"]
        url = "https://www.helloworld.rs/" + str(link)
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        get_all_page_post_info()
    except:
        break

print("---------------------------------------------------------")
print("Jobs found: " + str(count_posts()) + " | " + "Jobs Parsed: " + str(jobs))
print("---------------------------------------------------------")

def convert_date(df):
    try:
        df['Vaild until'] = pd.to_datetime(df['Vaild until'], format='%d.%m.%Y.')
        df['Vaild until'] = df['Vaild until'].dt.date
        df=df.sort_values(by="Vaild until")
        return df
    except:
        print("-!-Conversion failed-!-")
        return df


df = pd.DataFrame(data=data_global)
df = convert_date(df)
#.reset_index(drop=True)
print(df)
df.to_excel(f"C:/Users/aleks/Desktop/output/HW_scrape_{dt_string}.xlsx")
df.to_csv(f'C:/Users/aleks/Desktop/output/HW_scrape_{dt_string}.csv')
