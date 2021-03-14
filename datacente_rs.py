import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs


def get_start_data():
    return_list = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    url = 'https://www.datacente.rs/api/geo/world'

    r = session.get(url, headers=headers)
    if r.status_code == 200:
        datas = r.json()

        for data in  datas['features']:
            return_list.append(
                {
                    'id': data['properties']['id']
                }
            )

    return return_list


def get_data(list_for_search):
    list_result = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    for item in list_for_search:
        key = "b2e2be86-4f00-4337-bc3f-d61f168ef7d2"
        url = f"https://www.datacente.rs/api/dc/{item}?key={key}"
        r = session.get(url, headers=headers)
        if r.status_code == 200:
            print(url)
            data = r.json()

            doc = data['dc']
            city = data['city']
            address = data['address'][0]
            company = data['company']

            payload = {
                'id': item,	
                'name': doc.get('Name'),	
                'fullAddress': address,	
                'url': f"https://www.datacente.rs/datacenter/{item}/profile",	
                'providerId': company.get('id'),	
                'providerName': company.get('name'),	
                'longitude': doc.get('Longitude'),
                'latitude': doc.get('Latitude'),	
                'country': doc.get('country'),	
                'state': '-',	
                'city': city.get('name'),	
                'zip': doc.get('PostalCode'),	
                'websiteUrl': company.get('website'),	
                'yearFounded': "-",	
                'supportPhone': company.get('tel'), 
                'supportEmail': company.get('email'),	
                'displayPhoneNumber': company.get('tel'), 	
                'hqFullAddress': company.get('address'),
                'net_white_space': doc.get('net_white_space'),
                'expansion_1year': doc.get('expansion_1year'),
                'gross_max_power':doc.get('gross_max_power'),	
                'customer_max_power': doc.get('customer_max_power'),	
                'additional_gross_max_power': doc.get('additional_gross_max_power'),	
                'redundancy': doc.get('redundancy'),	
                'green_other': doc.get('P_Percentage_Green_Biomass'),
                'green_biomass': doc.get('P_Percentage_Green_Other'),
                'green_water': doc.get('P_Percentage_Green_Water'),
                'green_wind': doc.get('P_Percentage_Green_Wind')
            }
            list_result.append(payload)
    
    return list_result


if __name__ == "__main__":
    session = requests.session()
    data = get_start_data()

    df_locations = pd.DataFrame(data)
    serie_locations = list(df_locations['id'])
    
    df_scraping = pd.DataFrame(get_data(serie_locations))
    df_to_excel = df_scraping.replace(np.nan, '-', regex=True)
    df_to_excel = df_to_excel.replace('', '-', regex=True)
    df_to_excel.to_excel(f'datacente_rs.xlsx')