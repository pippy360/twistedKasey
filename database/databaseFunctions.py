
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
  #todo: what should this do if it get's none ????
  #todo: return error saying bad id
  objType = getObjectType( databaseId )

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
  data = objectInfoDatabase.getVal( databaseKeyFormat.format( databaseId, objectTypePrefix ) )
  return data


#check if file exists
#FIXME: this is all really messy
def isFile( databaseId ):
  #FIXME: clean up#THIS DOESN'T EVEN FUCKING CHECK IF IT'S A FILE !!!! GODDAM!
  if getFileType( databaseId ) == None:
      return False
  else:
    return True

def getFile( databaseId ):
  if not isFile( databaseId ):
    print "it's not a file"
    return 0, "ERROR: databaseId does not point to a file"#todo: lets try use this format for errors

  newFile = createNewFile( databaseId, { 'type': getFileType( databaseId ) } )
  newFile.load()
  return newFile

#TODO: this should return non PLUS AN ERROR (but not an exception) if the databaseId doesn't exist
def getFileInfo( databaseId ):
  f = getFile( databaseId )
  if not f:
    return None
  return f.getFileInfo()

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

def getSerializedObject( databaseId, keys ):
  result = {}
  for k in keys:
    result.update( { k: objectInfoDatabase.getVal( databaseKeyFormat.format( databaseId, k )) } )

  return result

objectTypePrefix = '_objectType'
def storeObjectInfo( dataOneDimensionalDict, databaseId, classId ):
  new = {}
  for k, v in dataOneDimensionalDict.iteritems():
    key = databaseKeyFormat.format( databaseId, k )
    new.update({ key: v })

  new.update({ databaseKeyFormat.format( databaseId, objectTypePrefix ): classId })
  objectInfoDatabase.setMutli( new )

def getFileIdWithHash( hash ):
  return fileHashDatabase.getRelatedIds( hash )

#stores a file in the database
def addFileToDatabase( fileInfo, fileDatabaseId=None, searchableInfo={}, tags=[] ):
  searchableDatabaseId = getNewDatabaseId()
  if fileDatabaseId == None:
    fileDatabaseId = getNewDatabaseId()

  #TODO: look over these inputs for searchable object, anyway to simplify ?
  s = databaseObjects.SearchableObject( databaseId=searchableDatabaseId, fileType=fileInfo['type'],
                                       metadata=str( fileInfo['metadata'] ), tags=tags )
  s.addNewFile( fileInfo, fileDatabaseId )
  s.save()
  fileHashDatabase.set( fileInfo['hash'], searchableDatabaseId, fileDatabaseId )#todo: make sure everything else worked before adding to the hashDB

  return {
      'databaseId': searchableDatabaseId,
      'fileLocation': fileDatabaseId
    }

#search
###############################################################################################

def getObjectInfo( databaseId ):
  s = getSearchableObject( databaseId )
  return s.getData()

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
