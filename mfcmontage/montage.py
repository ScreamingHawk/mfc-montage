#!/usr/bin/env python
"""Generates a pretty montage of a users MFC lists.

Montage downloads images from myfigurecollection using a users list and then
generates a pretty montage using ImageMagick with a commandline call. 
"""

from . import helper

import os
import concurrent.futures

montage_image_size_w = 256
montage_image_size_h = 256

def generateMontage(username, statusWord):
    """Generates a pretty montage with the saved images. """
    magickCmd = 'magick montage *'
    magickCmd += ' -shadow'
    magickCmd += ' -geometry "{}x{}+1+1>"'.format(montage_image_size_w, \
                                                  montage_image_size_h)
    magickCmd += ' -background {}'.format('white')
    magickCmd += ' ../{}_{}.jpg'.format(username, statusWord)

    print('Magick command: {}'.format(magickCmd))
    
    os.system('cd {} && {}'.format(helper.imageFolder, magickCmd))


def montageStatus(username, status):
    """Generates a montage for the given user and status. """
    statusWord = helper.getStatusWord(status)
    
    print('Getting {} list. '.format(statusWord))
    items = helper.getCollection(username, status, 1, [])
    print('Collection size: {}'.format(len(items)))

    helper.createImageFolder()

    # Get images
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
        for item in items:
            e.submit(helper.saveItemImage(item))

    generateMontage(username, statusWord)


if __name__ == '__main__':
    # Get user input
    username = str(input('MFC Username: '))
    status = str(input(\
        'Wished (0), Ordered (1), Owned (2) or All (<blank>): '))

    # Do montage
    if status == '':
        for status in range(0, 3):
            montageStatus(username, status)
    else:
        montageStatus(username, status)

    helper.deleteImageFolder()


