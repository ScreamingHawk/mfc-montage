#!/usr/bin/env python
"""Generates a pretty montage of a users MFC lists.

Montage downloads images from myfigurecollection using a users list and then
generates a pretty montage using ImageMagick with a commandline call. 
"""

try:
    # Module import
    from . import helper
except SystemError:
    # Local import
    import helper

import os
import concurrent.futures

montage_image_size_w = 256
montage_image_size_h = 256
montage_background = 'white'
montage_strip_bordercolor = 'grey'

montageFlags = None
montageFlagArgs = None

def resetMontageFlags():
    global montageFlags
    global montageFlagArgs
    montageFlags = '-shadow -geometry "{}x{}+1+1>" -background {}'
    montageFlagArgs = [montage_image_size_w, montage_image_size_h, \
                   montage_background]

# Init the flags
resetMontageFlags()

def preProcessMontage():
    """Resizes all images in image folder. """
    magickCmd = 'mogrify -resize "{}x{}^" -gravity center '+\
                '-crop {}x{}+0+0 +repage -bordercolor {} -border 1 *'
    helper.callMagick(magickCmd.format(montage_image_size_w, \
                                       montage_image_size_h, \
                                       montage_image_size_w, \
                                       montage_image_size_h, \
                                       montage_strip_bordercolor))    
        

def generateMontage(username, statusWord, title=True, \
                    overrideFilename=False, pause=0):
    """Generates a pretty montage with the saved images. """
    magickCmd = 'montage * '
    magickCmd += montageFlags.format(*montageFlagArgs)
    if title:
        magickCmd += ' -title "{}"'.format(str(statusWord).title())
    if not overrideFilename:
        magickCmd += ' ../{}_{}.jpg'.format(username, statusWord)

    helper.callMagick(magickCmd, pause=pause)


def montageStatus(username, status, strip=False):
    """Generates a montage for the given user and status. """
    statusWord = helper.getStatusWord(status)
    
    helper.console('Getting {} list. '.format(statusWord))
    items = helper.getCollection(username, status, 1, [])
    helper.console('Collection size: {}'.format(len(items)))

    helper.createImageFolder()

    # Get images
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
        for item in items:
            e.submit(helper.saveItemImage(item))

    if strip:
        global montage_image_size_w
        global montage_image_size_h
        montage_image_size_w = 100
        montage_image_size_h = 300
        resetMontageFlags()
        preProcessMontage()
        global montageFlags
        montageFlags += ' -tile x1'
        
    generateMontage(username, statusWord, title=(not strip))


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
        montageStatus(username, status, strip=True)

    helper.deleteImageFolder()


