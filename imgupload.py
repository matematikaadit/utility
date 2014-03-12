#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import requests                 # Remove non-stdlib dependencies
import sys


def usage():
    print """usage: imgupload.py FILE_INPUT

Upload each image pointed by urls in FILE_INPUT to imgur.
Output uploaded image name and it's imgur url.
Example of FILE_INPUT content:

http://upload.wikimedia.org/wikipedia/en/4/4c/Jc-rogo2.png
http://upload.wikimedia.org/wikipedia/en/b/b3/AnimeSuki_logo.JPG
http://upload.wikimedia.org/wikipedia/commons/6/63/Firefox_Screenshot.PNG
http://upload.wikimedia.org/wikipedia/commons/c/c6/Guido_van_Rossum.jpg
http://upload.wikimedia.org/wikipedia/commons/7/76/Yukihiro_Matsumoto.JPG
"""

def output(img_name, upname):
    print "{}: {}".format(img_name, upname)


def main():
    file_name = get_fn()
    with open(file_name, 'r') as f:
        upload_each(f)


def upload_each(urls):
    for url in urls:
        url = url.strip()       # iter(file) didn't remove trailing \n
        if not url: continue    # ignore blank line
        img_name, upname = upload_once(url)
        output(img_name, upname)


def upload_once(url, retry=0):
    error_location = 'http://imgur.com/?error'
    max_retry = 3

    r = imgur_upload(url)

    location = r.headers['location']
    if error_location == location:
        if retry <= max_retry:
            upload_once(url, retry=retry+1)
        else:
            raise Exception("Max retry in uploading: " + url)

    img_name = get_in(url)
    upname = get_un(location, img_name)

    return (img_name, upname)


def imgur_upload(url):
    address = 'http://imgur.com/upload'
    params = { 'url' : url }

    r = requests.get(address, params=params, allow_redirects=False)
    return r


def get_fn():
    try:
        fn = sys.argv[1]
    except IndexError:
        usage()
        sys.exit(1)

    return fn


def get_in(url):
    url = url.split('#')[0]     # Remove fragment
    url = url.split('?')[0]     # Remove query
    name = url.split('/')[-1]   # Last part of path

    return name


def get_un(location, img_name):
    host = 'http://i.imgur.com'
    imgid = location.split('/')[-1]
    ext = img_name.split('.')[-1]

    return "{host}/{imgid}.{ext}".format(host=host, imgid=imgid, ext=ext)


def reqget(url, params={}, allow_redirects=True):
    pass
    #TODO: Emulate requests.get and it's Response object


def debug(text):
    if os.environ.get('DEBUG'):
        sys.stderr.write("DEBUG: {text!r}\n".format(text=text))


if __name__ == '__main__':
    main()
