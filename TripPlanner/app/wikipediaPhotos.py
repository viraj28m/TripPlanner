from bs4 import BeautifulSoup

import requests

def extractBestFromSrcset(srcset):
    return srcset[srcset.rfind('//') : srcset.rfind(" ")]

def getCityPhoto(location):
    spl = location.split(", ")

    urlsToTry = []

    if len(spl) == 2:
        city, country = spl
    else:
        city, admin, country = spl
        urlsToTry.append(city + ",_" + admin + ",_" + country)
        urlsToTry.append(city + ",_" + admin)

    urlsToTry.append(city + ",_" + country)
    urlsToTry.append(city)
    
    prefix = "https://en.wikipedia.org/wiki/"
    for url in urlsToTry:
        
        page = requests.get(prefix + url)
        if page.status_code != 200:
            continue

        soup = BeautifulSoup(page.text, "html.parser")

        result = soup.find('img', class_="mw-file-element", src=lambda x: x and '.svg' not in x)
        
        if result is None:
            continue

        srcset = result['srcset']

        return extractBestFromSrcset(srcset)

    return ""

def getCountryFlag(location):
    country = location.split(", ")[-1]
    url = "https://en.wikipedia.org/wiki/" + country.replace(" ", "_")

    page = requests.get(url)
    if page.status_code != 200:
        return ""

    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.find('img', src=lambda x: x and 'Flag' in x)
    if result is None:
        return ""
    srcset = result['srcset']
    return extractBestFromSrcset(srcset)

def test(location):
    print(getCityPhoto(location))
    print(getCountryFlag(location))

if __name__ == "__main__":
    test("Berlin, Berlin, Germany")
