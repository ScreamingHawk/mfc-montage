#!/usr/bin/env python
"""A configuration class for enhancing image generation.

Contains a set of configuration options for use when generating images. """

class Config:
    """A configuration class for enhancing image generation. """

    def __init__(self):
        self.has_title = False
        self.title = ''
        self.image_width = 256
        self.image_height = 256
        self.has_background = True
        self.background_color = 'white'
        self.has_border = False
        self.border_color = 'grey'
        self.border_width = 1
        self.has_shadow = True
        self.has_gravity = False
        self.gravity = 'center'
        self.has_tile = False
        self.tile = 'x1'
        self.has_geometry = False
        self.geometry = None
        self.has_filename = False
        self.filename = 'out.jpg'

    def setHasTitle(self, hasTitle):
        self.has_title = hasTitle

    def setTitle(self, title):
        self.title = title
        self.setHasTitle(True)

    def setImageWidth(self, width):
        self.image_width = width

    def getImageWidth(self):
        return self.image_width

    def setImageHeight(self, height):
        self.image_height = height

    def getImageHeight(self):
        return self.image_height

    def setHasBackground(self, hasBackground):
        self.has_background = hasBackground

    def setBackgroundColor(self, color):
        self.background_color = color
        self.setHasBackground(True)

    def setHasBorder(self, hasBorder):
        self.has_border = hasBorder

    def setBorderColor(self, color):
        self.border_color = color
        self.setHasBorder(True)

    def setBorderWidth(self, width):
        self.border_width = width
        self.setHasBorder(True)

    def setHasShadow(self, hasShadow):
        self.has_shadow = hasShadow

    def setHasGravity(self, hasGravity):
        self.has_gravity = hasGravity

    def setGravity(self, gravity):
        self.gravity = gravity
        self.setHasGravity(True)

    def setHasTile(self, hasTile):
        self.has_tile = hasTile

    def setTile(self, tile):
        self.tile = tile
        self.setHasTile(True)

    def setHasGeometry(self, hasGeometry):
        self.has_geometry = hasGeometry

    def setGeometry(self, geometry):
        self.geometry = geometry
        self.setHasGeometry(True)

    def setHasFilename(self, hasFilename):
        self.has_filename = hasFilename

    def setFilename(self, filename):
        self.filename = filename
        self.setHasFilename(True)

    def setFilenameIfNone(self, filename):
        if not self.has_filename:
            self.setFilename(filename)


    def generateFlagsIgnoreFilename(self):
        flags = ' '
        if self.has_title:
            flags += '-title "{}" '.format(self.title)
        if self.has_background:
            flags += '-background {} '.format(self.background_color)
        if self.has_border:
            flags += '-border {} -bordercolor {} '.format(self.border_width, \
                                                          self.border_color)
        if self.has_gravity:
            flags += '-gravity {} '.format(self.gravity)
        if self.has_tile:
            flags += '-tile {} '.format(self.tile)
        if self.has_geometry:
            flags += '-geometry "{}" '.format(self.geometry)

        # Remove trailing space
        return flags[:-1]
        

    def generateFlags(self):
        flags = self.generateFlagsIgnoreFilename()

        if self.has_filename:
            flags += ' "../{}"'.format(self.filename)

        return flags



def createUserStatusConfig(username, statusWord):
    config = Config()
    if username is not None and statusWord is not None:
        setConfigTitleAndFilename(config, username, statusWord)
    return config


def setConfigTitleAndFilename(config, username, statusWord):
    """Sets the configuration objects title and filename to use username and
    status.
    """
    config.setTitle('{}\'s {}'.format(username, statusWord))
    config.setFilename('{}_{}.jpg'.format(username, statusWord))
    return config
            
