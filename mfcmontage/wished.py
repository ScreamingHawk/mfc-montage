#!/usr/bin/env python
"""Generates a pretty montage of a users MFC wished list.

Image is generated using wishability listing on MFC.
Useful as a way to showcase which items you most desire. 
"""

try:
    # Module import
    from . import montage, helper
except SystemError:
    # Local import
    import montage, helper

import os
import concurrent.futures


def montageWished(username):
    """Generates a montage for the given users wished list. """
    statusWord = 'wished'
    
    items = helper.getCollection(username, 0, 1, [])

    # Get images for each wishability
    helper.createImageFolder()
    montage.resetMontageFlags()
    montage.montageFlags += ' -tile x1'
    magickCmd = 'convert '
    wishabilityFilenames = []
    for wishability in reversed(range(1, 6)):
        wishabilityAdded = False
        helper.clearImageFolder()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
            for item in items:
                if int(item['mycollection']['wishability']) is wishability:
                    e.submit(helper.saveItemImage(item))
                    wishabilityAdded = True
        if wishabilityAdded:
            wishabilityFilenames.append('{}_{}.jpg'.format(\
                username, wishability))
            montage.generateMontage(username, wishability)

    # Join the seperate wishability images
    magickCmd += '{} -gravity center -append {}_wished.jpg'\
                 .format(" ".join(wishabilityFilenames), username)
    helper.callMagick(magickCmd, cd=False)

    # Clean up
    helper.deleteImageFolder()
    for filename in wishabilityFilenames:
        helper.deleteFile(filename)
        

if __name__ == '__main__':
    # Get user input
    username = str(input('MFC Username: '))

    montageWished(username)

    helper.deleteImageFolder()


