import os
import threading
import subprocess
from thumbnailGenerator import createThumbnail

builderPath = './databaseBuilder/images/'

def handlePageLoad( request ):
    return getImageIds()
    

def getImageIds():
    return os.listdir( builderPath )

def allTheOtherStuff():
    pass