import time
import random
from database import databaseFunctions, databaseObjects
#TODO: clients way of uploading, removing, editing files and the files data

filesLocation = './static/storage/'

def uploadFileFromUrl( request ):
  #FIXME: not implemented
  #attempt to get the URL
  #then upload File
  pass

def getId():
  return databaseFunctions.getNewDatabaseId()

def uploadFileFromForm( request ):

  fileInfo   = getFileInfo( f )#TODO: ERROR checking

  uploadInfo = getUploadInfo( request )

  formData   = getFormData( request )

  #check if the hash is already there, if it is just add the upload info and form data
  #else if
  #get a databaseId and add the data


#this function handles a every uploaded file once it is finished uploading
#whether it's from a URL or POST or anything else
def hanldeUploadedFile( fileOnServer, postData ):
  pass


def isValidFile():
  #check size
  #check format
  pass


def addFileToDatabases():
  pass


def getNewFileId():
  #the number of the file uploaded,
  #TODO: make the file ID system easy enough that people can write down the values manually
  pass



'''TODO: remove
  #at the point the file is saved on the server
  #process it, this should be done in the background

  #if not isValidFile( 'the file' ):
  #  return 'some error'

  fileId = ''
  size = ''
  originalFileName = ''
  fileId + ext = ''
  mimetype = ''
  userIp = ''
  title = ''
  description = ''
  fileMetadata = ''
  fileTags = ''

  #get the size
  #get the orginal filename #this might need some clean up if it came from a url
  #set the filename
  #get the mimetype
  #get the IP
  #get the title/desc
  #get the metadata
  #get the tags
  fileInfo = {}
  fileInfo['fileId']           = fileId
  fileInfo['originalSize']     = size
  fileInfo['originalFileName'] = originalFileName
  fileInfo['filename']         = fileId + ext
  fileInfo['mimetype']         = mimetype
  fileInfo['uploadDate']       = getUnixTime()
  fileInfo['ip']               = userIp
  fileInfo['title']            = title
  fileInfo['description']      = description
  fileInfo['metadata']         = fileMetadata
  fileInfo['convertedFiles']   = []
  fileInfo['tags']             = fileTags


  #get the file Id after making sure it's a valid file, that way we don't waste generated file ids
  '''

#  form = request.form
#  files = request.files

#  file = files['photo']
#  location = './static/storage/'#TODO: make this a fixed path so no problem with starting python like ./twistedKasey
#  file.save( location+file.filename )
#  tags = form['tags'].split()
#  title = form['title']
#  description = form['description']

#  databaseId = getId()
#  databaseFunctions.addTags( databaseId, tags )

#  print "search id : " + databaseId

#  search = databaseObjects.SearchableFile( databaseId )
#  print 'testing the class:'
#  print databaseObjects.SearchableFile.files

#  search.title = title
#  search.description = description
#  search.tags = tags
#  databaseId = getId()
#  print "file id : " + databaseId

#  newFile = databaseObjects.ImageFile( databaseId )
#  newFile.fileLocation = location
#  newFile.filename = file.filename

#  print search.files
#  search.files.append( newFile )
#  search.save()
#  search.saveRelatedFiles()
