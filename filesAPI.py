#clients way of uploading, removing, editing files and the files data


def uploadFileFromUrl( request ):
  #FIXME: not implemented
  #attempt to get the URL
  #then upload File
  pass


def uploadFileFromFileUpload( request ):
  pass


#this function handles a every uploaded file once it is finished uploading
#whether it's from a URL or POST or anything else
def hanldeUploadedFile( fileOnServer, postData ):
  #at the point the file is saved on the server

  #TODO: check if it's an accepted format

  #process it, this should be done in the background

  if not isValidFile( 'the file' ):
    return 'some error'

  #get the size
  #get the orginal filename #this might need some clean up if it came from a url
  #set the filename
  #get the mimetype
  #get the IP
  #get the title/desc
  #get the metadata
  #get the tags
  fileInfo.data['fileId']           = fileId
  fileInfo.data['originalSize']     = size
  fileInfo.data['originalFileName'] = originalFileName
  fileInfo.data['filename']         = fileId + ext
  fileInfo.data['mimetype']         = mimetype
  fileInfo.data['uploadDate']       = getUnixTime()
  fileInfo.data['ip']               = userIp
  fileInfo.data['title']            = title
  fileInfo.data['description']      = description
  fileInfo.data['metadata']         = fileMetadata
  fileInfo.data['convertedFiles']   = []
  fileInfo.data['tags']             = fileTags


  #get the file Id after making sure it's a valid file, that way we don't waste generated file ids


def isValidFile():
  #check size
  #check format
  return True


def addFileToDatabases():
  pass


def getNewFileId():
  #the number of the file uploaded,
  #TODO: make the file ID system easy enough that people can write down the values manually
