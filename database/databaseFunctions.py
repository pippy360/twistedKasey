#TODO: CLEAN UP, MAKE IT LOOK NICER
#this file keeps all the databases in sync
import objectInfoDatabase
import keywordDatabase
import databaseObjects
import websiteInfoDatabase

databaseKeyFormat = '{0}_{1}'

def getNewDatabaseId():
  return websiteInfoDatabase.getNewDatabaseId()

def getObjectType( databaseId ):
  data = objectInfoDatabase.getVal( databaseKeyFormat.format( databaseId, databaseObjects.objectTypePrefix ) )
  return data

def getFile( databaseId ):
  newFile = createNewFile( databaseId, getObjectType( databaseId ) )
  newFile.load()
  return newFile

def addTags( databaseId, tagsList ):
  keywordDatabase.addTags( databaseId, tagsList )

def createNewFile( databaseId, objectType ):
  if objectType   == databaseObjects.ImageFile.getClassId():
    return databaseObjects.ImageFile( databaseId )
  elif objectType == databaseObjects.VideoFile.getClassId():
    return databaseObjects.VideoFile( databaseId )
  elif objectType == databaseObjects.SoundFile.getClassId():
    return databaseObjects.SoundFile( databaseId )
  else:
    print "ERROR: create new file, bad objectType given"

def getSerializedObject( databaseId ):
  #TODO: this could cause problems if the keyFormat in objectInfoDatabase changes, because it won't be a stub
  result = objectInfoDatabase.getMultiWithStub( databaseId )
  data = {}
  for k,v in result.iteritems():
    if databaseObjects.dataPrefix in k:
      data.update( { k.replace( databaseObjects.dataPrefix, '' ): v } )

  result.update( { databaseObjects.dataPrefix : data } )

  return result

def storeSerializedObjects( serializedObjs ):#TODO: write for multiple objs
  if not type( serializedObjs ) is list:
    serializedObjs = [ serializedObjs ]

  for serializedObj in serializedObjs:
    databaseId = serializedObj[ databaseObjects.databaseIdPrefix ]
    del serializedObj[ databaseObjects.databaseIdPrefix ]
    objectInfoDatabase.setMutli( serializedObj )

def createSerializeObj( data, databaseId, classId ):
  result = {
      databaseObjects.databaseIdPrefix: databaseId,
      databaseKeyFormat.format( databaseId, databaseObjects.objectTypePrefix ): classId
    }
  for k, v in data.iteritems():
    key = databaseKeyFormat.format( databaseId, databaseObjects.dataPrefix + k )
    result.update( { key : v } )

  return result

def deserializeObj( serializeObj ):
  databaseId = serializedObj[ databaseObjects.databaseIdPrefix ]
  objType    = serializedObj[ databaseObjects.objectTypePrefix ]

  if objType == StorableObject.getClassId():
    result = StorableObject( databaseId )
    result.deserialize( serializedObj )
  elif objType == ImageFile.getClassId():
    result = ImageFile( databaseId )
    result.deserialize( serializedObj )
  elif objType == VideoFile.getClassId():
    result = VideoFile( databaseId )
    result.deserialize( serializedObj )
  elif objType == SoundFile.getClassId():
    result = SoundFile( databaseId )
    result.deserialize( serializedObj )

  return result


#search
###############################################################################################

def getSearchableObject( databaseId ):
  s = databaseObjects.SearchableObject( databaseId )
  s.load()
  return s

def getIntersection( keywords ):
  keywordDatabase.getIntersection( keywords )

#this function also removes bad Matches, sort of overComplicated
def getMatchingFiles( keyword ):
  matches = keywordDatabase.getMatchingFiles( keyword )
  matches = removeNonExistentFilesFromKeywordDatabse( matches, keyword )
  return matches

#TODO: is this way of removing the files stupid and overComplicated ??
def removeNonExistentFilesFromKeywordDatabse( matches, keyword ):
  #use getImageInfo to check if the image exists, if it doesn't remove it from the list
  return matches
