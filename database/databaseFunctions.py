#this file keeps all the databases in sync
import objectInfoDatabase


def addFile( fileInfo ):
  keywordDatabase.addTags( fileInfo.fileId, fileInfo.tagsList )
  objectInfoDatabase.addFile( fileInfo )


def removeFile( fileId ):
  #NOTE: big warning here, when files are removed they stay in the Keyword database
  #and aren't remove until they are returned in a search, see getMatchingImages
  objectInfoDatabase.removeFile( fileInfo )


#this function also removes bad Matches, sort of overComplicated
def getMatchingFiles( keyword ):
  matches = keywordDatabase.getMatchingFiles()
  matches = removeNonExistentFilesFromKeywordDatabse( matches, keyword )
  return matches


#TODO: is this way of removing the files stupid and overComplicated ??
def removeNonExistentFilesFromKeywordDatabse( matches, keyword ):
  #use getImageInfo to check if the image exists, if it doesn't remove it from the list
  return matches


def getImageInfo( fileId ):
  return objectInfoDatabase.getImageInfo( fileId )


def getSerializedObject( databaseId, skeletonSerializedDict ):
  return objectInfoDatabase.getSerializedObject( databaseId, skeletonSerializedDict )


def storeSerializedObject( databaseId, serializedDict ):
  return objectInfoDatabase.storeSerializedObject( databaseId, serializedDict )
