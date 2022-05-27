from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('C:/Users/aleks/Desktop/output/HW_scrape_30_04_2022_16_24.csv')

tags = df["Tags"]

unique_tags=[]

thisdict = {}

for tag_list in tags:
    tag_list=tag_list.replace("["," ")
    tag_list=tag_list.replace("]"," ")
    tag_list=tag_list.replace("'"," ")
    tag_list=tag_list.replace("   "," ")
    tag_list=tag_list.strip()
    tag_list=tag_list.split(",")
    for element in tag_list:
        element=element.strip()
        if element:
            if element not in unique_tags:
                unique_tags.append(element)
                thisdict[element]=1
            elif element in unique_tags:
                thisdict[element]=thisdict[element]+1

thisdict = dict(sorted(thisdict.items(), key=lambda item: item[1], reverse=True))

df = pd.DataFrame.from_dict(data=thisdict,orient='index')

head=50

pd.set_option("display.max_rows", None, "display.max_columns", None)
print("displaying top " + str(head) + " most wanted technologies")
print(df.head(head))
print("Unique types of technologies: " + str(len(unique_tags)))


#input("-Press <Enter> to display graph-")

def set_other(x):
    x="Other"
    return x

def plot_bar():
    ax = df.plot.bar(rot=90, color="#7eb54e")
    plt.legend(['Demand'])
    plt.show()


def plot_pie():
    df_1 = df.iloc[:26,:]
    df_2 = df.iloc[10:,:]
    x=0
    for i in df_2[0]:
        x=x+i
        
    df_other = pd.DataFrame({0:x},index=["Other"])

    df_3=df_1.append(df_other)

    ax = df_1.plot.pie(autopct='%1.5f%%',shadow=False, startangle=90, subplots=True, figsize=(10, 4))
    plt.suptitle("25 Most Demanded Technologies currently")
    plt.show()

plot_pie()
plot_bar()


#Make a proper dataframe