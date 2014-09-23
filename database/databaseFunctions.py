
#TODO: sound should be called 'audio'
#TODO: CLEAN UP, MAKE IT LOOK NICER
#this file keeps all the databases in sync
import objectInfoDatabase
import keywordDatabase
import databaseObjects
import websiteInfoDatabase
import fileHashDatabase

databaseKeyFormat = '{0}_{1}'

def getNewDatabaseId():
  return websiteInfoDatabase.getNewDatabaseId()

#TODO: explain difference between this and getObjectType
#FIXME: shouldn't be hardcoded
def getFileType( databaseId ):
  objType = getObjectType( databaseId )
  if objType == None:
    return None

  if objType   == databaseObjects.ImageFile.getClassId():
    return 'image'
  elif objType == databaseObjects.VideoFile.getClassId():
    return 'video'
  elif objType == databaseObjects.SoundFile.getClassId():
    return 'sound'
  else:
    print "ERROR: create new file, bad objType given"
    print objType

def getObjectType( databaseId ):
  data = objectInfoDatabase.getVal( databaseKeyFormat.format( databaseId, databaseObjects.objectTypePrefix ) )
  return data

def getFileInfo( databaseId ):#TODO: this should return non if the databaseId doesn't exist
  f = getFile( databaseId )
  if not f:
    return None
  result = f.serialize()
  return result['_data_info']#FIXME: THIS SHOULD NOT BE hardcoded

#check if file exists
def isFile( databaseId ):
  #FIXME: clean up
  if getFileType( databaseId ) == None:
    return None
  else:
    return getFileType( databaseId )

def getFile( databaseId ):
  if not isFile( databaseId ):
    return None

  newFile = createNewFile( databaseId, { 'type': getFileType( databaseId ) } )
  newFile.load()
  return newFile

def addTags( databaseId, tagsList ):
  keywordDatabase.addTags( databaseId, tagsList )

def createNewFile( databaseId, fileInfo ):
  fileType = fileInfo['type']
  if   fileType == 'image':
    return databaseObjects.ImageFile( databaseId, fileInfo )
  elif fileType == 'video':
    return databaseObjects.VideoFile( databaseId, fileInfo )
  elif fileType == 'sound':
    return databaseObjects.SoundFile( databaseId, fileInfo)
  else:
    print "ERROR: create new file, bad objType given"

def getSerializedObject( databaseId ):
  #TODO: this could cause problems if the keyFormat in objectInfoDatabase changes, because it won't be a stub
  result = objectInfoDatabase.getMultiWithStub( databaseId+'_' )
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
    #FIXME: HACKS HACKS
    new = {}
    for k, v in serializedObj.iteritems():
      key = databaseKeyFormat.format( databaseId, k )
      new.update({ key: v })

  objectInfoDatabase.setMutli( new )

def createSerializeObj( data, databaseId, classId ):
  result = {
      databaseObjects.databaseIdPrefix: databaseId,
      databaseObjects.objectTypePrefix: classId
    }
  for k, v in data.iteritems():
    key = databaseObjects.dataPrefix + k
    result.update( { key : v } )

  return result

def getFileIdWithHash( hash ):
  return fileHashDatabase.getRelatedIds( hash )

#stores a file in the database
def addFileToDatabase( fileInfo, fileDatabaseId=None, searchableInfo={} ):
  searchableDatabaseId = getNewDatabaseId()
  if fileDatabaseId == None:
    fileDatabaseId = getNewDatabaseId()

  fileHashDatabase.set( fileInfo['hash'], searchableDatabaseId, fileDatabaseId )
  #TODO: look over these inputs for searchable object, anyway to simplify ?
  s = databaseObjects.SearchableObject( databaseId=searchableDatabaseId, fileType=fileInfo['type'], metadata=str( fileInfo['metadata'] ) )
  s.addNewFile( fileDatabaseId, fileInfo )
  s.save()

  return {
      'databaseId': searchableDatabaseId,
      'fileLocation': fileDatabaseId
    }

#search
###############################################################################################

def getObjectInfo( databaseId ):
  data = getSearchableObject( databaseId )
  return data.serialize()

def getSearchableObject( databaseId ):
  s = databaseObjects.SearchableObject( databaseId )
  s.load()
  return s

def getIntersection( keywords ):
  return keywordDatabase.getIntersection( keywords )

#this function also removes bad Matches, sort of overComplicated
def getMatchingFiles( keyword ):
  matches = keywordDatabase.getMatchingFiles( keyword )
  matches = removeNonExistentFilesFromKeywordDatabse( matches, keyword )
  return matches

#TODO: is this way of removing the files stupid and overComplicated ??
def removeNonExistentFilesFromKeywordDatabse( matches, keyword ):
  #use getImageInfo to check if the image exists, if it doesn't remove it from the list
  return matches
