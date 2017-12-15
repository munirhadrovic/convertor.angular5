import re
import requests
from bs4 import BeautifulSoup
import base64

# with given url this will download all images to library
def download_all_images(site):
    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = []
    for tag in img_tags:
        try:
            urls.append(tag['src'])
        except:
            pass
    json_response = {'arr':[]}
    for j in urls:
        url = j    
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        try:
            d1 = filename.group(1)
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                if url.startswith('/'):
                    url = '{}{}'.format(site,url)
                else:
                    url = '{}/{}'.format(site, url)
            response = requests.get(url)
            d2 = base64.encodestring(response.content)
            json_response['arr'].append({'img_Name':d1,'img_base64':d2})
        except Exception as e:
            pass
    return json_response


def get_all_images(site):
    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = []
    for tag in img_tags:
        try:
            urls.append(tag['src'])
        except:
            pass
    return urls
