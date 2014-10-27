#TODO: be able to save user UPLOAD DATA(ip addr and stuff)
#TODO: change SearchableObject name

#FIXME: the whole type/imageFile class thing is totally messed up, fix it
import objectInfoDatabase
import databaseFunctions

acceptedFileTypes = ['image','video','sound']#TODO: MOVE THIS TO A CONFIG
databaseIdPrefix = '_databaseId'
dataPrefix = '_data_'

#TODO: explain
class StorableObject( object ):

  localPrimitivesKey = 'info'
  serializablePrimitives = {}

  @classmethod
  def getClassId( cls ):
    return cls.__name__

  def __init__( self, databaseId ):
    if databaseId == None:
      databaseId = databaseFunctions.getNewDatabaseId()

  #get a dict of the local primitive vars
  #(i.e. the variables that can be grouped and stored in a redis hash)
  def serializePrimitives( self ):
    return self.serializablePrimitives  

  def save( self ):
    data = self.serialize()
    databaseFunctions.storeObjectInfo( data, self.serializablePrimitives['databaseId'], self.getClassId() )#FIXME:

  def load( self ):
    keys = [ self.localPrimitivesKey ]
    serializedObj = databaseFunctions.getSerializedObject( self.serializablePrimitives['databaseId'], keys )
    self.deserialize( serializedObj[ self.localPrimitivesKey ] )

  def serialize( self ):
    return self.createDatabaseObj( {} )

  def deserialize( self, serializedObj ):
    for key, val in serializedObj.iteritems():
      if isinstance( val, (int, long, float, complex, basestring, list) ):
        self.serializablePrimitives[key] = val
      else:
        print "ERROR: bad var type"#TODO: learn errors


class SearchableObject( StorableObject ):
  #TODO: add file function, make sure it doesn't let two files with the same databaseId
  fileIdsKey = 'fileIds_'
  tagsKey    = 'tags_'
  searchableObjectString = 'searchableObject'
  serializablePrimitives = {
    'fileType':       '',
    'title':          '',
    'description':    '',
    'metadata':       '',
    'relatedFileIds': '',
    'uploadInfo':     ''
  }

  #TODO
  def __init__( self, databaseId, fileType = '', title = '', description = '',
               metadata = '', relatedFileIds = '', uploadInfo = '', tags=[] ):
    self.files = []

    self.tags                   = tags
    self.serializablePrimitives = {} #FIXME: see basicFile for details
    self.serializablePrimitives['databaseId']     = databaseId
    self.serializablePrimitives['fileType']       = fileType
    self.serializablePrimitives['title']          = title
    self.serializablePrimitives['description']    = description
    self.serializablePrimitives['metadata']       = metadata
    self.serializablePrimitives['relatedFileIds'] = relatedFileIds
    self.serializablePrimitives['uploadInfo']     = uploadInfo

  def addNewFile( self, fileInfo,databaseId=None ):
    for f in self.files:
      if f.serializablePrimitives['databaseId'] == databaseId:
        print "ERROR: file with id exists"
        return

    self.files.append( databaseFunctions.createNewFile( databaseId, fileInfo ) )

  def save( self ):
    fileIds = []
    for f in self.files:
      f.save()
      fileIds.append( f.serializablePrimitives['databaseId'] )

    data = self.serialize()
    data.update( { self.fileIdsKey : fileIds } )
    data.update( { self.tagsKey : self.tags } )
    databaseFunctions.storeObjectInfo( data, self.serializablePrimitives['databaseId'], self.getClassId() )

  def load( self ):
    self.files = []

    keys = [ self.localPrimitivesKey, self.fileIdsKey, self.tagsKey ]#TODO: make a keys array maybe
    serializedObj = databaseFunctions.getSerializedObject( self.serializablePrimitives['databaseId'], keys )
    self.deserialize( serializedObj[ self.localPrimitivesKey ] )

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

  def serialize( self ):
    return { self.localPrimitivesKey: self.serializePrimitives() }


class uploadInfo( StorableObject ):
  pass



#instead of having a different class for each file type 
class BasicFile( StorableObject ):

  type = 'BasicFile'#FIXME: have some sort of global image type

  serializablePrimitives =   {
    'databaseId'  : '',
    'originalFile': '',
    'fileHash':     '',
    'filename':     '',
    'fileLocation': '',
    'extension':    '',
    'mimetype':     '',
    'fileMetadata': '',
    'type':         ''
  }

  #TODO: something about the init
  def __init__( self, databaseId=None, fileData={}):
    if databaseId == None:
      databaseId = databaseFunctions.getNewDatabaseId()

    #FIXME: there should be a way of allowing optional parameters 
    #but while still enforcing the user to fill the required ones
    #MAYBE just use the init to decide which ones are optional and not
    #BUT you should be able to add a new primitive with one line of code

    #FIXME: instead of this we should deep copy the class.serializablePrimitives and use that
    #to force the user to set certain vars
    self.serializablePrimitives = {} #FIXME: 
    self.serializablePrimitives['databaseId']   = databaseId
    self.serializablePrimitives['originalFile'] = fileData.get( 'originalFile' )
    self.serializablePrimitives['fileHash']     = fileData.get( 'fileHash' )
    self.serializablePrimitives['filename']     = fileData.get( 'filename' )
    self.serializablePrimitives['fileLocation'] = fileData.get( 'fileLocation' )
    self.serializablePrimitives['extension']    = fileData.get( 'extension' )
    self.serializablePrimitives['mimetype']     = fileData.get( 'mimetype' )
    self.serializablePrimitives['fileMetadata'] = fileData.get( 'metadata' )
    self.serializablePrimitives['type']         = self.getType()

  def getFileInfo( self ):
    return self.serializePrimitives()

  def serialize( self ):
    return { self.localPrimitivesKey: self.serializePrimitives() }

  def getType( self ):
    return self.getClassId()#FIXME: have some global nice way, use some sort of global enum

class ImageFile( BasicFile ):
  pass


class VideoFile( BasicFile ):
  pass


class SoundFile( BasicFile ):
  pass
