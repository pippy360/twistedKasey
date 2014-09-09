#TODO: UPLOAD DATA
import objectInfoDatabase
import databaseFunctions

acceptedFileTypes = ['image','video','sound']#TODO: MOVE THIS TO A CONFIG

#serialize returns strings and lists

#TODO: explain
class StorableObject( object ):

  databaseId = ''#used to access database

  def save( self ):
    data = self.serialize()
    databaseFunctions.storeSerializedObject( self.databaseId, data )

  def load( self ):
    skeleton = self.serialize()
    data = databaseFunctions.getSerializedObject( self.databaseId, skeleton )
    self.updateData( data )

  #TODO: EXPLAIN
  #TODO: turn it into a get skeleton function
  def serialize( self ):
    return {}

  def updateData( self, fileData ):
    for key, val in fileData.iteritems():
      if isinstance( val, (int, long, float, complex, basestring) ):
        setattr( self, key, val )
      elif type( val ) is list:
        setattr( self, key, val )
      elif type( val ) is dict:
        for k,v in val.iteritems():
          setattr( self, k, v )
      else:
        print "ERROR"#TODO: learn erro

  #TODO: explain
  def deserialize( self, skeletonSerializedDict ):#TODO: replace fileID with self.id
    self.updateData( skeletonSerializedDict )

  def __init__( self, databaseId ):
    self.databaseId = databaseId


class SearchableFile( StorableObject ):

  files = []
  title = ''
  description = ''
  metadata = ''
  fileType = ''#video, sound, image
  tags = []
  relatedFileIds = ''
  uploadInfo = []

  def __init__( self, databaseId, fileType=None ):
    self.databaseId = databaseId
    self.fileType = fileType
    if not fileType in acceptedFileTypes:
      print "ERROR"#TODO: learn how to handle errors


  def createNewFile( self, databaseId, fileType=None ):
    if fileType is None: fileType = self.fileType
    if not fileType in acceptedFileTypes: print "ERROR"

    if fileType == 'image':
      return ImageFile( databaseId )
    elif fileType == 'video':
      return VideoFile( databaseId )
    elif fileType == 'sound':
      return SoundFile( databaseId )


  def addFile( self, databaseId, fileType=None, fileData={} ):
    if fileType is None: fileType = self.fileType
    newFile = getNewFile()
    files.append( )

  #TODO: fileIds shouldn't be hardcoded
  def saveRelatedFiles( self ):
    fileIds = []
    for currfile in self.files:
      currfile.save()
      fileIds.append( currfile.databaseId )

    serializedObj = { "fileIds": fileIds }
    databaseFunctions.storeSerializedObject( self.databaseId, serializedObj )


  def loadRelatedFiles( self ):
    files = []
    serializedObj = { "fileIds": [] }
    serializedObj = databaseFunctions.getSerializedObject( self.databaseId, serializedObj )
    print serializedObj
    for fileDatabaseId in serializedObj['fileIds']:
      newFile = self.createNewFile( fileDatabaseId )
      self.files.append( newFile )

    for currfile in self.files:
      currfile.load()


  def serialize( self ):
    return {
      'data': {
        'title': self.title,
        'description': self.description,
        'metadata': self.metadata,
        'fileType': self.fileType,
        'relatedFileIds': self.relatedFileIds,
        'uploadInfo': self.uploadInfo
      },
      'tags': self.tags
    }


class uploadInfo( StorableObject ):

  ip = ''
  time = ''
  fileId = ''

class BasicFile( StorableObject ):

  databaseFilePrefix = 'file_'
  originalFile = ''#TODO: explain
  fileHash = ''
  filename = ''
  fileLocation = ''
  extension = ''
  mimetype = ''
  fileMetadata = ''

  def __init__( self, databaseId, fileData={} ):
    self.databaseId = databaseId
    self.updateData( fileData )

  def serializeBasicFile( self ):
    return {
      'originalFile': self.originalFile,
      'fileHash': self.fileHash,
      'filename': self.filename,
      'fileLocation': self.fileLocation,
      'extension': self.extension,
      'mimetype': self.mimetype,
      'fileMetadata': self.fileMetadata
    }

  def serialize( self ):
    return {
      'info': self.serializeBasicFile()
    }


class ImageFile( BasicFile ):

  width = ''

  def serialize( self ):
    result = self.serializeBasicFile()
    result.update({
      'width': self.width,
    })
    return {
      'info': result
    }


class VideoFile( BasicFile ):

  width = ''

  def serialize( self ):
    result = self.serializeBasicFile()
    result.update({
      'width': self.width,
    })
    return {
      'info': result
    }


class SoundFile( BasicFile ):

  length = -1

  def serialize( self ):
    result = self.serializeBasicFile()
    result.update({
      'length': self.length,
    })
    return {
      'info': result
    }
