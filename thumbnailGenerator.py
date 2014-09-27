
from flask import send_file
import os.path
import Image
import math
import ast
from database   import databaseFunctions, databaseObjects

thumbnailCacheFolder = '/static/cache/thumbs'#DIRTY QUICK FIX

#FIXME: this whole thing is patched together with horrible code just to get it working

def handleThumbnailRequest( request ):
  print request.args
  height  = request.args['height']
  width   = request.args['width']
  imageId = request.args['imageId']
  fileloc = genThumbnail( imageId, (int( width ), int( height) ) )
  return send_file( fileloc, mimetype='image/png')


#if maintainAspectRatio is true then 'size' is the max possible width/height of the thumbnail
def genThumbnail( imageId, size, maintainAspectRatio=True ):
  imageInfo = databaseFunctions.getFileInfo( imageId )

  result = {}
  result = ast.literal_eval( imageInfo['fileMetadata'] )

  width  = result['dimensions']['width']
  height = result['dimensions']['height']

  imageInfoSize = ( width , height )

  if maintainAspectRatio:
    thumbSizeX, thumbSizeY = getThumbnailSize( imageInfoSize, size )
  else:
    thumbSize = size

  thumbFilename = getThumbnailFilename( imageId, thumbSizeX, thumbSizeY )
  if os.path.isfile( thumbnailCacheFolder + thumbFilename ):#check cache
    return thumbnailCacheFolder + thumbFilename

  loc = '.' + imageInfo['fileLocation'] + imageInfo['filename']
  orginalImg = Image.open( loc )
  im = orginalImg.resize((thumbSizeX, thumbSizeY), Image.ANTIALIAS)
  im.save( '.' + thumbnailCacheFolder + thumbFilename + imageInfo['extension'] )

  return '.' + thumbnailCacheFolder + thumbFilename + imageInfo['extension']


def getThumbnailFilename( imageId, width, height ):
  return "thumbnail_{0}_{1}_{2}".format( imageId, width, height )


def getThumbnailSize( imageSize, thumbSize):
  x, y = imageSize

  if x > thumbSize[0]:
    y = max(y * thumbSize[0] / x, 1)
    x = thumbSize[0]

  if y > thumbSize[1]:
    x = max(x * thumbSize[1] / y, 1)
    y = thumbSize[1]

  return x, y


##TODO: COMMENT
#def genThumbnailWithOriginalAspectRatio( imageId, maxWidth, maxHeight ):
#  imageInfo = imageInfoDatabase.getImageInfo( imageId )
#  if( imageInfo.width/imageInfo.height > maxWidth/maxHeight ):
#    #maxWidth is the value that limits size
#    thumbWidth  = maxWidth
#    thumbHeight = math.floor( thumbWidth * imageInfo.height/imageInfo.width )
#  else:
#    #maxHeight is the value that limits size
#    thumbHeight = maxHeight
#    thumbWidth  = math.floor( thumbHeight * imageInfo.width/imageInfo.height )
#
#  #DEBUG:
#  print "width:"
#  print thumbWidth
#  print "height:"
#  print thumbHeight
#
#  #check what the width and height should be
#  return genThumbnail( imageId, thumbWidth, thumbHeight )


#make a get size function so that we can check the cache


