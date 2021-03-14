import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs

"""
    Incompleto Revisar Mejor
"""


def get_start_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    result_final = []
    result = []
    x_algolia_agent = "Algolia%20for%20vanilla%20JavaScript%203.17.0"
    x_algolia_application_id = "EI7S1GLGKN"
    x_algolia_api_key = "4ab01079145dab5d03fb5c4a0455f564"
    url = f'https://ei7s1glgkn-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent={x_algolia_agent}&x-algolia-application-id={x_algolia_application_id}&x-algolia-api-key={x_algolia_api_key}'
    i = 0
    per_page = 8000
    while True:
        json = {
            "requests":[
                {
                    "indexName":"facilities-production",
                    "params":"hitsPerPage={}&maxValuesPerFacet=3&page={}&facets=%5B%5D&tagFilters=".format(per_page, i)
                }
            ]
        }
        r = session.post(url, headers=headers, json=json)
        if r.status_code == 200:
            data = r.json()
            print(len(data['results'][0]['hits']), i)
            if len(data['results'][0]['hits']) > 0:
                for item in data['results'][0]['hits']:
                    adress = item['address']
                    operador = item['operator']
                    payload = {
                        "id": item['objectID'],
                        "name": item['name'], 
                        "fullAddress": None, 
                        "url": item.get('url'),
                        "providerId": None,
                        "providerName": operador.get('name'), 
                        "longitude": adress.get('lng'),
                        "latitude": adress.get('lat'),
                        "country": adress.get('country'),
                        "state": adress.get('region'),
                        "city": adress.get('city'),
                        "zip": adress.get('zipCode'),
                        "websiteUrl": item.get('website'),
                        "yearFounded": None,
                        "supportPhone": None,
                        "supportEmail": None,
                        "hqFullAddress": None
                    }
                    result.append(payload)
            else:
                break
        i+=1

    return result


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Cookie': 'fs_uid=rs.fullstory.com#D1C3D#4740063881576448:4843846531792896/1646966387; _rbs=eyJpdiI6ImczaVwvamlyK3J4RE1xbDk0WmVmQUFBPT0iLCJ2YWx1ZSI6Ikt4TThcL1A2OEpcLzJBTjU2aVwvbFByN1E9PSIsIm1hYyI6IjUzMzE2ZTE4OGU5NWYxMWJiNDM5YTk0YmFkMWE0NGQ4OTBmNzZhNTFhMmQ2ZTBmNDZmOGQwNWNkZmNiZDZiODYifQ==; OptanonConsent=isIABGlobal=false&datestamp=Wed+Mar+10+2021+23:39:50+GMT-0300+(hora+estándar+de+Argentina)&version=6.13.0&landingPath=https://cloudscene.com/data-center/united-states-of-america/chicago/equinix-ch2&groups=1:1,0_146040:0,3:0,0_146038:0,0_171650:1,0_162162:0,2:0,0_171654:1,4:0,0_162161:0,0_119541:0,0_146037:0,0_119544:0,0_119543:0,0_171721:0,0_171652:0; XSRF-TOKEN=eyJpdiI6IkZZZlpyZWlnN0wwNHlhVEUzSmI4YUE9PSIsInZhbHVlIjoidW5kTlgzRVZMMVNLTzRWM0pXRlJoZGIxclFzUlZjeFdTczZ3Rm5wT1grWnhKd2oyOWJDU25oSlp4XC9GdE9DcHMiLCJtYWMiOiI3MGU3ZTRlNWE3ZTQ5MmY5NWEwNmI1ZWU2MTc3YzFjMTI4ODU4MDZkMWZhYzE3YTVmMjVhMWY0NWQ3MmQ0MWVjIn0=; laravel_session=eyJpdiI6IkZUOCsxdWsreFFvT1h5OHFVeXg2VVE9PSIsInZhbHVlIjoiaWhLZWRqdmVXQlB6YkFlblFcLzRVd2xFcHdVejJXTzUyOFJFVXlqXC9sNFZNaVVobEtPcHlFUnBCY21kNm01WGlXIiwibWFjIjoiNDExZWMzMWZiNjk1YTAwN2U3OWUyZDEwZDIxMmU5NDIwNGI1NGM5OTFkMDkzYTJlYjk5YjMzNzU0ZTAxMDRlOCJ9',
        'accept': 'application/json, text/plain, */*',
        'x-csrf-token': 'Jgp1nBy8yC6c4Nnexx0cZwgxO3ER397cfsX3TqVO',
        'x-requested-with': 'XMLHttpRequest'
    }
    r = session.get(url, headers=headers)
    if r.status_code == 200:
        print(r.status_code, url)
        data = r.json()
        return data
    else:
        print(r.status_code, url)
    return False


def get_asset_uid(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Cookie': 'fs_uid=rs.fullstory.com#D1C3D#4740063881576448:4843846531792896/1646966387; _rbs=eyJpdiI6ImczaVwvamlyK3J4RE1xbDk0WmVmQUFBPT0iLCJ2YWx1ZSI6Ikt4TThcL1A2OEpcLzJBTjU2aVwvbFByN1E9PSIsIm1hYyI6IjUzMzE2ZTE4OGU5NWYxMWJiNDM5YTk0YmFkMWE0NGQ4OTBmNzZhNTFhMmQ2ZTBmNDZmOGQwNWNkZmNiZDZiODYifQ==; OptanonConsent=isIABGlobal=false&datestamp=Wed+Mar+10+2021+23:39:50+GMT-0300+(hora+estándar+de+Argentina)&version=6.13.0&landingPath=https://cloudscene.com/data-center/united-states-of-america/chicago/equinix-ch2&groups=1:1,0_146040:0,3:0,0_146038:0,0_171650:1,0_162162:0,2:0,0_171654:1,4:0,0_162161:0,0_119541:0,0_146037:0,0_119544:0,0_119543:0,0_171721:0,0_171652:0; XSRF-TOKEN=eyJpdiI6IkZZZlpyZWlnN0wwNHlhVEUzSmI4YUE9PSIsInZhbHVlIjoidW5kTlgzRVZMMVNLTzRWM0pXRlJoZGIxclFzUlZjeFdTczZ3Rm5wT1grWnhKd2oyOWJDU25oSlp4XC9GdE9DcHMiLCJtYWMiOiI3MGU3ZTRlNWE3ZTQ5MmY5NWEwNmI1ZWU2MTc3YzFjMTI4ODU4MDZkMWZhYzE3YTVmMjVhMWY0NWQ3MmQ0MWVjIn0=; laravel_session=eyJpdiI6IkZUOCsxdWsreFFvT1h5OHFVeXg2VVE9PSIsInZhbHVlIjoiaWhLZWRqdmVXQlB6YkFlblFcLzRVd2xFcHdVejJXTzUyOFJFVXlqXC9sNFZNaVVobEtPcHlFUnBCY21kNm01WGlXIiwibWFjIjoiNDExZWMzMWZiNjk1YTAwN2U3OWUyZDEwZDIxMmU5NDIwNGI1NGM5OTFkMDkzYTJlYjk5YjMzNzU0ZTAxMDRlOCJ9',
        'accept': 'application/json, text/plain, */*',
        'x-csrf-token': 'Jgp1nBy8yC6c4Nnexx0cZwgxO3ER397cfsX3TqVO',
        'x-requested-with': 'XMLHttpRequest'
    }
    r = session.get(url, headers=headers)
    if r.status_code == 200:
        html = r.content
        html = bs(html.decode('UTF-8'), "html5lib")
        javascripts = html.find_all("script", {'type':'text/javascript'})
        for j in javascripts:
            content = j.text
            if content.find('assetUUID') >= 0:
                print(r.status_code, url)
                split_uid = content.split('assetUUID="')[1]
                split_uid = split_uid.split('";var')[0]
                return split_uid.strip()
        return False    
    else:
        print(r.status_code, url)
    return False


if __name__ == "__main__":
    session = requests.session()
    data = get_start_data()

    df_pre_scraping = pd.DataFrame(data)
    df_to_excel = df_pre_scraping.replace(np.nan, '-', regex=True)
    df_to_excel.to_excel(f'pre_scraping_cloundscense.xlsx')

    # for item in result:
    #     assetUUID = get_asset_uid(item['url'])
    #     if assetUUID:
    #         data = get_data(f"https://cloudscene.com/data-center/getData?assetId={assetUUID}&searchSP=&searchFab=&sortBySP=0&sortByFab=0&currentPageSP=1&currentPageFab=1")
    #         if data:
    #             facility = data['facility']
    #             item['providerId'] = facility.get('company_id')
    #             item["grossBuildingSize"] = facility.get('buildSizeGross')
    #             item["grossColocationSpace"] = facility.get('buildSizeColocationTot')
    #             item["totalPowerMw"] = facility.get('powerGenTotal')
    #             item["powerDensity"] = facility.get('powerGenRackMax')
    #             item["displayPhoneNumber"] = facility.get('salesPhone')

    #             result_final.append(item)
    
    # return result_final