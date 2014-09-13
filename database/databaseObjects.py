#TODO: UPLOAD DATA
import objectInfoDatabase
import databaseFunctions

acceptedFileTypes = ['image','video','sound']#TODO: MOVE THIS TO A CONFIG
databaseIdPrefix = '_databaseId'
objectTypePrefix = '_objectType'
dataPrefix = '_data_'

#TODO: explain
class StorableObject( object ):

  simpleInstantVarsPrefix = 'info'

  @classmethod
  def getClassId( cls ):
    return cls.__name__

  def __init__( self, databaseId ):
    if databaseId == None:
      databaseId = databaseFunctions.getNewDatabaseId()

  def createSerializeObj( self, data ):
    return databaseFunctions.createSerializeObj( data, self.databaseId, self.__class__.getClassId() )

  def save( self ):
    data = self.serialize()
    databaseFunctions.storeSerializedObjects( data )

  def load( self ):
    serializedObj = databaseFunctions.getSerializedObject( self.databaseId )
    self.deserialize( serializedObj )

  def serialize( self ):
    return self.createSerializeObj( {} )

  def deserialize( self, serializedObj ):
    for key, val in serializedObj[ dataPrefix ][ self.simpleInstantVarsPrefix ].iteritems():
      if isinstance( val, (int, long, float, complex, basestring, list) ):
        setattr( self, key, val )
      else:
        print "ERROR: bad var type"#TODO: learn errors


class SearchableObject( StorableObject ):
  #TODO: add file function, make sure it doesn't let two files with the same databaseId
  fileIdsPrefix = 'fileIds'

  def __init__( self, databaseId=None, fileType = '', title = '', description = '',
               metadata = '', relatedFileIds = '', uploadInfo = '' ):
    self.files = []
    if databaseId == None:
      databaseId = databaseFunctions.getNewDatabaseId()

    self.databaseId = databaseId

    self.fileType       = fileType
    self.title          = title
    self.description    = description
    self.metadata       = metadata
    self.relatedFileIds = relatedFileIds
    self.uploadInfo     = uploadInfo

  def addNewFile( self, databaseId, objType ):
    for f in self.files:
      if f.databaseId == databaseId:
        print "ERROR: file with id exists"
        return

    self.files.append( databaseFunctions.createNewFile( databaseId, objType  ) )

  def save( self ):
    for f in self.files:
      f.save()

    databaseFunctions.storeSerializedObjects( self.simpleSerialize() )

  def load( self ):
    self.files = []
    fileIds = []
    serializedObj = databaseFunctions.getSerializedObject( self.databaseId )
    data = serializedObj[ dataPrefix ]
    fileIds = serializedObj[ dataPrefix ].get( self.fileIdsPrefix, [] )
    for fileId in fileIds:
      f = databaseFunctions.getFile( fileId )
      self.files.append( f )

  #TODO: explain
  #this serializes just the easy to serialize variables, it ignores stuff like self.files
  def simpleSerialize( self ):
    info = {
          'fileType':       self.fileType,
          'title':          self.title,
          'description':    self.description,
          'metadata':       self.metadata,
          'relatedFileIds': self.relatedFileIds,
          'uploadInfo':     self.uploadInfo,
      }
    fileIds = []
    for f in self.files:
      fileIds.append( f.databaseId )

    return self.createSerializeObj( {
          self.simpleInstantVarsPrefix : info,
          self.fileIdsPrefix: fileIds
      } )

  def serialize( self ):
    result  = []
    for f in self.files:
      result.append( f.serialize() )

    result.append( self.simpleSerialize() )

    return result


class uploadInfo( StorableObject ):
  pass


class BasicFile( StorableObject ):

  #TODO: something about the init
  def __init__( self, databaseId=None, originalFile = '', fileHash = '', filename = '',
               fileLocation = '', extension = '', mimetype = '', fileMetadata = ''):
    if databaseId == None:
      databaseId = databaseFunctions.getNewDatabaseId()


    self.originalFile = originalFile
    self.fileHash     = fileHash
    self.filename     = filename
    self.fileLocation = fileLocation
    self.extension    = extension
    self.mimetype     = mimetype
    self.fileMetadata = fileMetadata

  def serializeBasicFile( self ):
    return {
      'originalFile': self.originalFile,
      'fileHash':     self.fileHash,
      'filename':     self.filename,
      'fileLocation': self.fileLocation,
      'extension':    self.extension,
      'mimetype':     self.mimetype,
      'fileMetadata': self.fileMetadata
    }

  def serialize( self ):
    return self.createSerializeObj( { self.simpleInstantVarsPrefix: self.serializeBasicFile() } )


class ImageFile( BasicFile ):
  pass


class VideoFile( BasicFile ):
  pass


class SoundFile( BasicFile ):
  pass
