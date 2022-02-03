from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("C:\chromedriver")
browser.get(START_URL)
time.sleep(10)


headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []

def scrap():
    for i in range(1,430):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            if current_page_num < i:
                # second arrow , greater than symbol
                browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
            elif current_page_num > i:
                # first arrow, less than
                browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
            else:
                break
            for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
                li_tags = ul_tag.find_all("li")
                temp_list = []
                for index, li_tag in enumerate(li_tags):
                    if index == 0:
                        temp_list.append(li_tag.find_all("a")[0].contents[0])
                    else:
                        try:
                            temp_list.append(li_tag.contents[0])
                        except:
                            temp_list.append("")
                hyperlink_li_tag = li_tags[0]
                temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
                planet_data.append(temp_list)
            browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()

def scrapmoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class","fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class","value"})[0].contents[0] )
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrapmoredata(hyperlink)

scrap()

for index,data in enumerate(planet_data):
    scrapmoredata(data[5])
    print(f"Page done-{index+1}")
    
final_planet_data = []

for index,data in enumerate(planet_data):
    e = new_planet_data[index]
    e = [elem.replace("\n","") for i in e]
    e = e[:7]
    final_planet_data.append(data+e)

with open("final.csv","w") as w:
    c = csv.writer(w)
    c.writerow(headers)
    c.writerows(final_planet_data())

        

        