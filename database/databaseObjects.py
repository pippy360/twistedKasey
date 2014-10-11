#TODO: be able to save user UPLOAD DATA(ip addr and stuff)
#TODO: change SearchableObject name
import objectInfoDatabase
import databaseFunctions

acceptedFileTypes = ['image','video','sound']#TODO: MOVE THIS TO A CONFIG
databaseIdPrefix = '_databaseId'
dataPrefix = '_data_'

#TODO: explain
class StorableObject( object ):

  localPrimitivesKey = 'info'

  @classmethod
  def getClassId( cls ):
    return cls.__name__

  def __init__( self, databaseId ):
    if databaseId == None:
      databaseId = databaseFunctions.getNewDatabaseId()

  def save( self ):
    data = self.serialize()
    databaseFunctions.storeObjectInfo( data, self.databaseId, self.getClassId() )#FIXME:

  def load( self ):
    keys = [ self.localPrimitivesKey ]
    serializedObj = databaseFunctions.getSerializedObject( self.databaseId, keys )
    self.deserialize( serializedObj[ self.localPrimitivesKey ] )

  def serialize( self ):
    return self.createDatabaseObj( {} )

  def deserialize( self, serializedObj ):
    for key, val in serializedObj.iteritems():
      if isinstance( val, (int, long, float, complex, basestring, list) ):
        setattr( self, key, val )
      else:
        print "ERROR: bad var type"#TODO: learn errors


class SearchableObject( StorableObject ):
  #TODO: add file function, make sure it doesn't let two files with the same databaseId
  fileIdsKey = 'fileIds_'
  tagsKey    = 'tags_'
  searchableObjectString = 'searchableObject'

  def __init__( self, databaseId, fileType = '', title = '', description = '',
               metadata = '', relatedFileIds = '', uploadInfo = '', tags=[] ):
    self.files = []
    self.tags           = tags
    self.databaseId     = databaseId
    self.fileType       = fileType
    self.title          = title
    self.description    = description
    self.metadata       = metadata
    self.relatedFileIds = relatedFileIds
    self.uploadInfo     = uploadInfo

  def addNewFile( self, fileInfo,databaseId=None ):
    for f in self.files:
      if f.databaseId == databaseId:
        print "ERROR: file with id exists"
        return

    self.files.append( databaseFunctions.createNewFile( databaseId, fileInfo ) )

  def save( self ):
    fileIds = []
    for f in self.files:
      f.save()
      fileIds.append( f.databaseId )

    data = self.serialize()
    data.update( { self.fileIdsKey : fileIds } )
    data.update( { self.tagsKey : self.tags } )
    databaseFunctions.storeObjectInfo( data, self.databaseId, self.getClassId() )

  def load( self ):
    self.files = []

    keys = [ self.localPrimitivesKey, self.fileIdsKey, self.tagsKey ]#TODO: make a keys array maybe
    serializedObj = databaseFunctions.getSerializedObject( self.databaseId, keys )
    self.deserialize( serializedObj[ self.localPrimitivesKey ] )

    print 'loading tags'
    print serializedObj
    print serializedObj.get( self.tagsKey, [] )
    tags = serializedObj.get( self.tagsKey, [] )
    self.tags = tags

    #todo: clean up the fileIds == None
    #load the related files
    fileIds = serializedObj.get( self.fileIdsKey, [] )
    if fileIds == None:
      return

    for fileId in fileIds:
      f = databaseFunctions.getFile( fileId )
      self.files.append( f )

  #todo: comment
  #data that is sent to the client in json
  def getData( self ):#FIXME: hardcoded
    result  = { 'files': [] }
    for f in self.files:
      result['files'].append( f.getFileInfo() )#fixme: hardcoded

    result.update( { self.tagsKey: self.tags } )
    result.update( { self.searchableObjectString: self.serializePrimitives() } )
    return result

  #serializes the local primitive vars
  #(i.e. the variable that can be grouped and stored in a redis hash)
  def serializePrimitives( self ):
    return {
          'fileType':       self.fileType,
          'title':          self.title,
          'description':    self.description,
          'metadata':       self.metadata,
          'relatedFileIds': self.relatedFileIds,
          'uploadInfo':     self.uploadInfo
      }

  def serialize( self ):
    return { self.localPrimitivesKey: self.serializePrimitives() }


class uploadInfo( StorableObject ):
  pass


class BasicFile( StorableObject ):

  #TODO: something about the init
  def __init__( self, databaseId=None, fileData={}):
    if databaseId == None:
      databaseId = databaseFunctions.getNewDatabaseId()

    self.databaseId   = databaseId
    self.originalFile = fileData.get( 'originalFile' )
    self.fileHash     = fileData.get( 'fileHash' )
    self.filename     = fileData.get( 'filename' )
    self.fileLocation = fileData.get( 'fileLocation' )
    self.extension    = fileData.get( 'extension' )
    self.mimetype     = fileData.get( 'mimetype' )
    self.fileMetadata = fileData.get( 'metadata' )

  def getFileInfo( self ):
    return self.serializePrimitives()

  def serializePrimitives( self ):
    return {
      'databaseId'  : self.databaseId,
      'originalFile': self.originalFile,
      'fileHash':     self.fileHash,
      'filename':     self.filename,
      'fileLocation': self.fileLocation,
      'extension':    self.extension,
      'mimetype':     self.mimetype,
      'fileMetadata': self.fileMetadata
    }

  def serialize( self ):
    return { self.localPrimitivesKey: self.serializePrimitives() }


class ImageFile( BasicFile ):
  pass


class VideoFile( BasicFile ):
  pass


class SoundFile( BasicFile ):
  pass
