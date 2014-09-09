from flask import send_file
import os.path
import image
import math
import imageInfoDatabase

thumbnailCacheFolder = './static/cache/thumbs'


def handleThumbnailRequest( request ):
  pass
  #send_file('./static/img/1.png', mimetype='image/gif')


#if maintainAspectRatio is true then 'size' is the max possible width/height of the thumbnail
def genThumbnail( imageId, size, maintainAspectRatio=True ):
  imageInfo = imageInfoDatabase.getImageInfo( imageId )

  if maintainAspectRatio:
    thumbSize = getThumbnailSize( imageInfo.size, size )
  else:
    thumbSize = size

  thumbFilename = getThumbnailFilename( imageId, thumbSize )
  if os.path.isfile( thumbnailCacheFolder + thumbFilename ):#check cache
    return thumbnailCacheFolder + thumbFilename

  orginalImg = Image.open( imageInfo.filename )
  im = orginalImg.resize((width, height), Image.ANTIALIAS)
  im.save( thumbnailCacheFolder + thumbFilename )

  return thumbnailCacheFolder + thumbFilename


def getThumbnailFilename( imageId, width, height ):
  return "thumbnail_{0}_{1}_{2}".format( imageid, width, height )


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


