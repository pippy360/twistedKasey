import time
import random
import base64
import hashlib
import shutil
import os
from database   import databaseFunctions, databaseObjects
from processing import detect
#TODO: clients way of uploading, removing, editing files and the files data

filesLocation = './static/storage/'
tempDir = './static/temp/'

#FIXME: the current implementation allows tags to be added only after the file has finished uploading
def hanldeUploadFormSubmit( request ):
  f = request.files['photo']

  tags = request.form.get('tags')
  path = saveTempFile( f )
  status = handleUploadedFile( path )
  if tags:
    tags = tags.split()
    databaseFunctions.addTags( status, tags )#FIXME: THIS IS SO FUCKING HACKY

  return status

def saveTempFile( fileStorageObj ):
  #todo: there is functions to turn a path + filename into a valid path
  fileStorageObj.save( tempDir + fileStorageObj.filename )
  return tempDir + fileStorageObj.filename

#handles a file after it's finished uploading to the server
def handleUploadedFile( path ):

  fileInfo = getFileInfo( path )
  fileInfo['fileLocation'] = filesLocation#TODO: this is 

  #TODO: replace status with exceptions and all that good stuff
  status = isValidFile( path, fileInfo )
  if not status:#FIXME: status should be some sort of obj
    print 'ERROR'
    return status

  return storeFile( path, fileInfo )

#this function only accepts valid working files
def storeFile( path, fileInfo ):
  #check if the file already exists
  if databaseFunctions.getFileIdByHash( fileInfo['hash'] ) != None:
    return handleExistingFile( fileInfo )

  if fileInfo['type'] == 'image' and getVisuallyIdenticalFile( fileInfo['visualFingerprint'] ) != None:
    return handleVisualMatch( fileInfo )#todo: can this just be the handleExistingFile function ?

  returnData = databaseFunctions.addFileToDatabase( fileInfo )
#  if not status.valid:
 #   return status

  #move the file to storage
  shutil.copyfile( path, filesLocation + fileInfo['filename'] )

  return returnData['databaseId']

def handleExistingFile( fileInfo ):
  databaseFunctions.getFileIdByHash( fileInfo['hash'] )

def getVisuallyIdenticalFile( fingerPrint ):
  return None

def getFileInfo( path ):
  result = detect.detect( path )

  result['size'] = os.path.getsize(path)
  f = open( path )
  result['hash'] = getBeautifulHash( f )
  #get extension, just get it from the filename ATM
  fileName, fileExtension = os.path.splitext( path )
  result['extension'] = fileExtension

  result['filename'] = result['hash'] + result['extension']

  result['visualFingerprint'] = 'something'
  #then just the file type specific stuff
  #put type specific stuff into functions
  return result

#TODO: USE THIS
def getBasicFileInfo():
  pass

def getBeautifulHash( f ):
  tempHash = get_hash( f )
  return to_id( tempHash )

def get_hash(f):
  f.seek(0)
  return hashlib.md5(f.read()).digest()

def isValidFile( path, fileInfo ):
  #FIXME:
  if fileInfo['size'] > 100000000:
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
