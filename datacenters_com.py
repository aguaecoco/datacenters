import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs


def get_start_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    url = 'https://www.datacenters.com/api/v1/locations?query=&withProducts=false&showHidden=false&nearby=false&radius=0&bounds=&circleBounds=&polygonPath=&forMap=true'
    r = session.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()

    return data


def get_data(list_for_search):
    list_result = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    
    for item in list_for_search:
        r = session.get(item['url'], headers=headers)
        if r.status_code == 200:
            print(item['url'])
            html = r.content
            html = bs(html.decode('UTF-8'), "html5lib")

            json_react = html.find("script", {'data-component-name':'LocationProviderDetail'}).text
            json_react = json.loads(json_react)
            location = json_react['location']
            payload = {
                "id": item['id'],
                "grossBuildingSize": location.get('grossBuildingSize'),
                "grossColocationSpace": location.get('grossColocationSpace'),
                "totalPowerMw": location.get('totalPowerMw'),
                "powerDensity": location.get('powerDensity'),
                "country": location.get('country'),
                "state": location.get('state'),
                "city": location.get('city'),
                "zip": location.get('zip')
            }
            list_result.append(payload)
    
    return list_result


if __name__ == "__main__":
    session = requests.session()
    data = get_start_data()

    df_providers = pd.DataFrame(data['providers'])
    df_providers = df_providers[['id', 'websiteUrl', 'yearFounded', 'supportPhone', 'supportEmail', 'displayPhoneNumber', 'hqFullAddress']]
    df_providers = df_providers.rename(columns = {'id': 'providerId'}, inplace = False)

    df_locations = pd.DataFrame(data['locations'])
    df_locations = df_locations[['id', 'name', 'fullAddress', 'url', 'providerId', 'providerName', 'longitude', 'latitude']]
    df_locations['url'] = df_locations.apply(lambda x: f'https://www.datacenters.com{x["url"]}', axis=1)

    list_for_search = []
    for index, row in df_locations.iterrows():
        list_for_search.append(
            {
                "id": row['id'],
                "url": row['url']
            }
        )

    new_data = get_data(list_for_search)
    df_scraping = pd.DataFrame(new_data)
    df_one_full = pd.merge(df_locations, df_scraping)
    df_full = pd.merge(df_one_full, df_providers)

    df_to_excel = df_full.replace(np.nan, '-', regex=True)
    df_to_excel = df_to_excel.replace('N/A', '-', regex=True)
    df_to_excel.to_excel(f'datacenters_com.xlsx')
