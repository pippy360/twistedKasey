import keywordDatabase
import json


def getSearchResultsWithQuery( query ):
  keywordsList = getKeywordsFromQuery( query )
  mathingImages = getMatchingImagesList( keywordsList )
  sortedImageIdList = getListSortedByRelevance( mathingImages )
  return json.dumps( sortedImageIdList )

  #return sortedImageIdList


#TODO: give a better name
def jsonEncode( imageIdList ):
  return imageIdList


def getKeywordsFromQuery( query ):
  query = query.lower()

  return query.split()

def getMatchingImagesList( keywordsList ):
  result = []
  for keyword in keywordsList:

    matchingImages = keywordDatabase.getMatchingImages( keyword )
    result.append( (keyword, matchingImages) )

  return result


#TODO: explain what it returns
def getListSortedByRelevance( keywordsWithImages ):
  result = []
  for imageIdTuple in keywordsWithImages:

    imageIdList = imageIdTuple[1]
    for imageId in imageIdList:

      pos = getPosOfKeyInResult( imageId, result )
      if pos != -1:
        result[ pos ] = ( imageId, result[pos][1] + 1 )#increments immutable value of result[pos][1]
      else:
        result.append( ( imageId, 1 ) )

  return sorted(result, key=lambda tup: tup[1], reverse=True)


def getPosOfKeyInResult( key, result ):
  for j in range( len( result ) ):#check against the results

    if result[j][0] == key:
      return j

  return -1
