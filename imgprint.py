#!/usr/bin/env python


import requests
import sys
import urlparse
import re
from bs4 import BeautifulSoup


main_url = urlparse.urlparse(sys.argv[1])
BASE_URL = "{url.scheme}://{url.netloc}".format(url=main_url)

def get_links(url):
    # print '--> get: ' + url
    mainp = requests.get(url)
    document = BeautifulSoup(mainp.content)
    imglinks = document.select('.imgphoto a')
    return imglinks


def get_img_page(imglinks):
    imgpages = []
    for a in imglinks:
        link = a['href']
        url = get_url(link)
        # print '---> get: ' + url
        r = requests.get(url)
        doc = BeautifulSoup(r.content)
        imgpages.append(doc)

    return imgpages


def get_url(link, base_url=BASE_URL):
    return base_url + link


def get_img_urls(imgpages):
    imgurls = []
    for imgpage in imgpages:
        raw = imgpage.find('script', text=re.compile('ImageOrgFile')).text
        imgurls.extend(parse_url(raw))
    return imgurls

def parse_url(raw):
    pattern = r'Array\("([^"]+)"'
    return re.findall(pattern, raw)


def download_files(urls):
    for url in urls:
        target = get_url(url)
        filename = target.split('/')[-1]
        # print '----> download: ' + filename
        r = requests.get(target, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

def main():
    imglinks = get_links(main_url.geturl())
    imgpages = get_img_page(imglinks)
    imgurls = get_img_urls(imgpages)
    full_imgurls = map(lambda url: get_url(url), imgurls)

    print '\n'.join(full_imgurls)



if __name__ == '__main__':
    main()
