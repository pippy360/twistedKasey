
from flask import send_file
import os.path
import Image
import math
from database   import databaseFunctions, databaseObjects

thumbnailCacheFolder = './static/cache/'

def handleThumbnailRequest( request ):
  height  = int( request.args['height'] )
  width   = int( request.args['width'] )

  if request.args.get('imageId') != None:
    imageId = request.args['imageId']
    imageInfo = databaseFunctions.getFileInfo( imageId )
    thumbPath = createThumbnail( '.'+imageInfo['fileLocation'], imageInfo['filename'], (width,height) )
  else:
    imageLocation = request.args['imageLocation']
    imageFilename = request.args['imageFilename']
    thumbPath = createThumbnail( imageLocation, imageFilename, (width,height) )

  return send_file( thumbPath, mimetype='image/png')

def createThumbnail( imageLocation, imageFilename, thumbSize, maintainAspectRatio=True ):
  orginalImg = Image.open( imageLocation + imageFilename )
  imageSize = orginalImg.size

  if maintainAspectRatio:
    thumbSize = calcThumbnailSize( imageSize, thumbSize )

  thumbPath = thumbnailCacheFolder + genThumbFilename( imageFilename, thumbSize )
  #check if thumbnail is in cache
  if os.path.isfile( thumbPath ):
    return thumbPath

  thumb = orginalImg.resize( thumbSize, Image.ANTIALIAS )
  thumb.save( thumbPath )

  return thumbPath


def genThumbFilename( imageFilename, thumbSize ):
  #rip the extension
  filename, fileExtension = os.path.splitext( imageFilename )
  return "thumbnail_{0}_{1}_{2}{3}".format( filename, thumbSize[0], thumbSize[1], fileExtension )


def calcThumbnailSize( imageSize, thumbSize ):
  x, y = imageSize

  if x > thumbSize[0]:
    y = max(y * thumbSize[0] / x, 1)
    x = thumbSize[0]

  if y > thumbSize[1]:
    x = max(x * thumbSize[1] / y, 1)
    y = thumbSize[1]

  return x, y
