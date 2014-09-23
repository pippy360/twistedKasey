from database import databaseFunctions
import json


def getSearchResultsWithQuery( query ):
  keywordsList = getKeywordsFromQuery( query )
  sortedImageIdList = databaseFunctions.getIntersection( keywordsList )

  result = []
  print sortedImageIdList
  for imageId in sortedImageIdList:
    print 'image id : '
    print imageId
    objData = databaseFunctions.getObjectInfo( imageId[0] )
    result.append( objData )

  return json.dumps( result )

  #return sortedImageIdList


#TODO: give a better name
def jsonEncode( fileIdList ):
  return fileIdList


def getKeywordsFromQuery( query ):
  query = query.lower()

  return query.split()

def getMatchingFilesList( keywordsList ):
  result = []
  for keyword in keywordsList:
    matchingFiles = databaseFunctions.getMatchingFiles( keyword )
    result.append( (keyword, matchingFiles) )

  return result

#TODO: explain what it returns
def getListSortedByRelevance( keywordsWithFiles ):
  result = []
  for fileIdTuple in keywordsWithFiles:

    fileIdList = fileIdTuple[1]
    for fileId in fileIdList:

      pos = getPosOfKeyInResult( fileId, result )
      if pos != -1:
        result[ pos ] = ( fileId, result[pos][1] + 1 )#increments immutable value of result[pos][1]
      else:
        result.append( ( fileId, 1 ) )

  return sorted(result, key=lambda tup: tup[1], reverse=True)


def getPosOfKeyInResult( key, result ):
  for j in range( len( result ) ):#check against the results

    if result[j][0] == key:
      return j

  return -1
