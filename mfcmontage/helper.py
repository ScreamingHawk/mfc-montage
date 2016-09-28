#!/usr/bin/env python
"""A helper class for common functions.

Helper contains methods to download collection images, get JSON responses from
API calls, maps status codes to words. 
"""

import urllib.request
import json
import sys
import os
import shutil
import time
import re

mfc_base = 'http://myfigurecollection.net/api.php?type=json'
mfc_img_base = 'http://s1.tsuki-board.net/pics/figure/big/'
imageFolder = 'img'

def getResponse(url):
    """A helper method for getting a JSON response. """
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    resp = json.loads(data)
    if 'error' in resp:
        print('Error: {}'.format(resp['error']['msg']))
        input('Press Enter to Close')
        sys.exit()
    return resp


def getStatusWord(status):
    """Returns the status word from the status code. """
    statusWord = 'owned'
    if status == 0:
        return 'wished'
    elif status == 1:
        return 'ordered'
    return statusWord


def getStatusCode(statusWord):
    """Returns the status code from the status word. """
    try:
        return ['ordered', 'wished', 'owned'].index(statusWord)
    except ValueError:
        return -1


def getCollection(username, status, page, items):
    """Returns all items in a users list. """
    print('Getting page: {}'.format(page))
    resp = getResponse('{}&mode=collection&username={}&status={}&page={}'\
                       .format(mfc_base, username, status, page))

    # Get collection
    try:
        coll = resp['collection'][getStatusWord(status)]

        for item in coll['item']:
            items.append(item)
            print(item['data']['name'])
    except KeyError:
        # Nothing in this page
        return items
    
    if int(coll['num_pages']) > page:
        return getCollection(username, status, page+1, items)
    return items


def saveItemImage(item):
    """Saves the image for the item to disk. """
    itemName = item['data']['name']
    print('Getting image for: {}'.format(itemName))
    fullImgUrl = '{}{}.jpg'.format(mfc_img_base, item['data']['id'])
    req = urllib.request.Request(fullImgUrl, \
                                 headers={'User-Agent' : "Magic Browser"})
    foutName = '{}/{}.jpg'.format(imageFolder, \
                                  re.sub(r'([^\s\w]|_)+', '', itemName)[:32])
    with urllib.request.urlopen(req) as response, \
         open(foutName, 'wb+') as fout:
        shutil.copyfileobj(response, fout)


def createImageFolder():
    """Creates or empties the image folder. """
    try:
        os.makedirs(imageFolder)
    except FileExistsError:
        # Exists, delete contents instead
        filelist = [f for f in os.listdir(imageFolder)]
        for f in filelist:
            os.remove('{}/{}'.format(imageFolder, f))


def deleteImageFolder():
    """Clears the image folder. """
    try:
        shutil.rmtree(imageFolder)
    except PermissionError:
        #Still busy creating the montage or something. Try once more
        time.sleep(5)
        shutil.rmtree(imageFolder)

    
if __name__ == '__main__':
    # Do nothing
    pass


