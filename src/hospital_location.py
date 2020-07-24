from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd


def scrape_save_hosp_wiki():

    url = "https://en.wikipedia.org/wiki/List_of_hospitals_in_Colorado"
    r  = requests.get(url)
    response_html = r.text

    soup = BeautifulSoup(response_html, 'html.parser')

    tables = soup.find_all('table', class_="wikitable sortable")
    # print(len(tables))
    hospitals = tables[0]
    #print(hospitals)
    anchors = hospitals.find_all('a')


    hospital_county_city = []
    for anchor in anchors:
        if "href" in anchor.attrs and "title" in anchor.attrs:
            #print(anchor.text)
            if anchor.text in ["Psychiatric", "Long Term", "Rehabilitation", "Vibra Healthcare"]:
                continue
            else:
                hospital_county_city.append(anchor.text)
    #print(len(hospital_county_city))
    hospital_name = [hospital_county_city[x] for x in range(0, len(hospital_county_city), 3)]
    hospital_county = [hospital_county_city[x] for x in range(1, len(hospital_county_city), 3)]
    hospital_city = [hospital_county_city[x] for x in range(2, len(hospital_county_city), 3)]
    #print(hospital_county)
    data = []
    for x in range(0, len(hospital_name)):
        data.append([hospital_name[x], hospital_county[x], hospital_city[x]])

    df = pd.DataFrame(data)
    df.columns = ['Hospital', 'county', 'city']
    df.to_csv('../data/hospital_location.csv')

if __name__ =='__main__':
    scrape_save_hosp_wiki()