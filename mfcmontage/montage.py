#!/usr/bin/env python
"""Generates a pretty montage of a users MFC lists.

Montage downloads images from myfigurecollection using a users list and then
generates a pretty montage using ImageMagick with a commandline call. 
"""

try:
    # Module import
    from . import helper, image_config
except SystemError:
    # Local import
    import helper, image_config

import os
import concurrent.futures


def preProcessMontage(config=image_config.Config()):
    """Resizes all images in image folder. """
    magickCmd = 'mogrify -resize "{}x{}^" -crop {}x{}+0+0 +repage {} *'
    helper.callMagick(magickCmd.format(config.getImageWidth(), \
                                       config.getImageHeight(), \
                                       config.getImageWidth(), \
                                       config.getImageHeight(), \
                                       config.generateFlags()))
    

def generateMontage(config=image_config.Config(), pause=0):
    """Generates a pretty montage with the saved images. """
    config.setFilenameIfNone('out.jpg')
    magickCmd = 'montage {} {}'.format(helper.listImageFolderString(), \
                                       config.generateFlags())
    helper.callMagick(magickCmd, pause=pause)


def generateMontageStrip(configStrip=image_config.Config(), \
                         configMontage=image_config.Config(), \
                         vertical=False):
    """Generates a strip formatted montage using saved images. """
    if vertical:
        configStrip.setImageWidth(300)
        configStrip.setImageHeight(100)
        configMontage.setImageWidth(300)
        configMontage.setImageHeight(100)
        configMontage.setTile('1x')
    else:
        configStrip.setImageWidth(100)
        configStrip.setImageHeight(300)
        configMontage.setImageWidth(100)
        configMontage.setImageHeight(300)
        configMontage.setTile('x1')
    # Default if not set
    if not configStrip.has_gravity:
        configStrip.setGravity('center')
    if not configStrip.has_border:
        configStrip.setBorderColor('grey')
    if not configMontage.has_geometry:
        configMontage.setGeometry("{}x{}+1+1>".format(\
            configMontage.image_width, configMontage.image_height))
    if not configMontage.has_background:
        configMontage.setBackgroundColor('white')
    if not configMontage.has_shadow is None:
        configMontage.setHasShadow(True)
    preProcessMontage(configStrip)
    generateMontage(configMontage)


def generateMontagePantsu(configStrip=image_config.Config(), \
                         configMontage=image_config.Config()):
    """Generates a strip formatted montage using saved images, in vertical. """
    generateMontageStrip(configStrip=configStrip, \
                         configMontage=configMontage, \
                         vertical=True)


def montageStatus(username, status, strip=False, vertical=False):
    """Generates a montage for the given user and status. """
    statusWord = helper.getStatusWord(status)
    
    helper.console('Getting {} list. '.format(statusWord))
    items = helper.getCollection(username, status, 1, [])
    helper.console('Collection size: {}'.format(len(items)))

    if len(items) == 0:
        helper.console('Nothing to generate. ')
    else:
        helper.createImageFolder()

        # Get images
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
            for item in items:
                e.submit(helper.saveItemImage(item))

        config = image_config.createUserStatusConfig(username, statusWord)
        if strip:
            if vertical:
                generateMontagePantsu(configMontage=config)
            else:
                generateMontageStrip(configMontage=config)
        else:
            generateMontage(config)


if __name__ == '__main__':
    # Get user input
    username = str(input('MFC Username: '))
    status = str(input(\
        'Wished (0), Ordered (1), Owned (2) or All (<blank>): '))
    strip = str(input('Strip format (y/N): ')).lower() == 'y'
    if strip:
        vert = str(input('Pantsu format (y/N): ')).lower() == 'y'
    else:
        vert = False

    # Do montage
    if status == '':
        for status in range(0, 3):
            montageStatus(username, status, strip=strip, vertical=vert)
    else:
        montageStatus(username, int(status), strip=strip, vertical=vert)

    helper.deleteImageFolder()


