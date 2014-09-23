import time
import random
import base64
import hashlib
import os
from database   import databaseFunctions, databaseObjects
from processing import detect
#TODO: clients way of uploading, removing, editing files and the files data

filesLocation = './static/storage/'

#FIXME: the current implementation allows tags to be added only after the file has finished uploading
def hanldeUploadFormSubmit( request ):
  working = []
  for k, f in request.files.iteritems():
    returnData = storeFile( f )
    tags = request.form['tags'].split()
    if tags:
      databaseFunctions.addTags( returnData['databaseId'], tags )#FIXME: THIS IS SO FUCKING HACKY
    working.append( returnData['fileLocation'] )

  #tags should be a dict #!! so that multiple tags can be added to multiple images
  #databaseFunctions.addTags(  )

  #databaseFunctions.updateData(  )
  return working

#TODO: this should really be moved to the databaseFunctions, encase the layout of databases changes
def storeFile( f, originalFilename='' ):

  fileInfo = getFileInfo( f )

  #FIXME: the paths here are badly done
  filePath = './static/storage/'
  sitePath = '/static/storage/'
  fileInfo['fileLocation'] = sitePath

  status = isValidFile( fileInfo )
  if status != 0:
    return status

  #check if the file already exists
  existingFileIdDict = databaseFunctions.getFileIdWithHash( fileInfo['hash'] )
  print 'Hash:'
  print fileInfo['hash']

  if existingFileIdDict != None:
    print 'existing file'
    #call special update function
    existingFileInfo = databaseFunctions.getFileInfo( existingFileIdDict['fileId'] )
    return {
      'databaseId': existingFileIdDict['searchableId'],
      'fileLocation': existingFileInfo['filename']
    }
  else:
    #FIXME: ALL THIS IS SO FUCKING MESSY
    print 'new File'
    #TODO: write the return information and decide on a standard way of doing it
    fileIds = databaseFunctions.addFileToDatabase( fileInfo )
    f.seek( 0 )
    f.save( filePath + fileInfo['filename'] )
    return {
      'databaseId': fileIds['databaseId'],
      'fileLocation': fileIds['fileLocation']
    }


def getFileInfo( f ):
  #FIXME:
  tempPath = './static/storage/'
  f.save( tempPath+f.filename )
  result = detect.detect( tempPath+f.filename )

  result['size'] = 100000

  result['hash'] = getBeautifulHash( f )

  #get extension, just get it from the filename ATM
  fileName, fileExtension = os.path.splitext( f.filename )
  result['extension'] = fileExtension

  result['filename'] = result['hash'] + result['extension']

  #then just the file type specific stuff
  #put type specific stuff into functions
  return result

def getBeautifulHash( f ):
  tempHash = get_hash( f )
  return to_id( tempHash )

def get_hash(f):
  f.seek(0)
  return hashlib.md5(f.read()).digest()

def isValidFile( fileInfo ):
  #FIXME:
  if fileInfo['size'] > 1000:
    return False
  elif not fileInfo['type'] in ['image']:
    return False
  else:
    return True

def getNewFileId():
  #the number of the file uploaded,
  #TODO: make the file ID system easy enough that people can write down the values manually
  pass

to_id = lambda h: base64.b64encode(h)[:12].replace('/', '_').replace('+', '-')
