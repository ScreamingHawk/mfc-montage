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

def console(out):
    """Catches unicode errors when printing. """
    try:
        print(out)
    except UnicodeEncodeError:
        print(re.sub(r'([^\s\w]|_)+', '', out))


def getResponse(url):
    """A helper method for getting a JSON response. """
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    resp = json.loads(data)
    if 'error' in resp:
        console('Error: {}'.format(resp['error']['msg']))
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


def getCollection(username, status, page, items, figuresOnly=True, \
                  prepaintedOnly=False):
    """Returns all items in a users list. """
    console('Getting page: {}'.format(page))
    resp = getResponse('{}&mode=collection&username={}&status={}&page={}'\
                       .format(mfc_base, username, status, page))

    # Get collection
    coll = resp['collection'][getStatusWord(status)]

    for item in coll['item']:
        if (not figuresOnly or item['root']['name'] == 'Figures') and \
           (not prepaintedOnly or \
            item['category']['name'] == 'Prepainted'):
            items.append(item)
            console(item['data']['name'])
    
    if int(coll['num_pages']) > page:
        return getCollection(username, status, page+1, items)
    return items


def saveItemImage(item):
    """Saves the image for the item to disk. """
    itemName = item['data']['name']
    console('Getting image for: {}'.format(itemName))
    fullImgUrl = '{}{}.jpg'.format(mfc_img_base, item['data']['id'])
    req = urllib.request.Request(fullImgUrl, \
                                 headers={'User-Agent' : "Magic Browser"})
    foutName = '{}/{}.jpg'.format(imageFolder, \
                                  re.sub(r'([^\s\w]|_)+', '', itemName)[:32])
    with urllib.request.urlopen(req) as response, \
         open(foutName, 'wb+') as fout:
        shutil.copyfileobj(response, fout)


def listImageFolder():
    """Returns a list of all filenames in the image folder. """
    #Note: Ignores files ending in ~ which is a backup/lock file
    return [f for f in os.listdir(imageFolder) if f[-1] is not '~']

def listImageFolderString():
    """Returns a string containing a list of all filename in the image
    folder.
    """
    return ' '.join(map('"{}"'.format, listImageFolder()))

def createImageFolder():
    """Creates or empties the image folder. """
    try:
        os.makedirs(imageFolder)
    except FileExistsError:
        # Exists, delete contents instead
        clearImageFolder()


def clearImageFolder():
    """Clears the contents of the image folder. """
    filelist = listImageFolder()
    for f in filelist:
        os.remove('{}/{}'.format(imageFolder, f))
            

def deleteImageFolder(pause=5):
    """Deletes the image folder. """
    try:
        shutil.rmtree(imageFolder)
    except PermissionError:
        # Still busy creating the montage or something. Try once more
        time.sleep(pause)
        shutil.rmtree(imageFolder)
    except FileNotFoundError:
        # Folder already gone
        pass


def callMagick(magickCmd, pause=1, cd=True):
    console('Magick command: {}'.format(magickCmd))
    cmd = ''
    if cd:
        cmd = 'cd {} && '.format(imageFolder)
    os.system('{}magick {}'.format(cmd, magickCmd))
    time.sleep(pause)


def deleteFile(filename, cd=False):
    cmd = ''
    if cd:
        cmd = 'cd {} && '.format(imageFolder)
    os.system('{}del {}'.format(cmd, filename))
    
    
if __name__ == '__main__':
    # Do nothing
    pass


