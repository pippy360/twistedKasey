#TODO: all this should be renamed to tag database
import redis

#only this module should know about this keyword prefix
keyStringPrefix = 'k_'
keyFormat = '{0}_{1}'# '_keyword_' + the tag

keywordRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )


def addTags( databaseID, tagsList ):
  if isinstance( tagsList, basestring):
    tagsList = [ tagsList ]

  for tag in tagsList:
    keywordRedisDB.sadd( keyFormat.format( keyStringPrefix, tag ), databaseID )

def getIntersection( keywords ):
  fixed = []
  for keyword in keywords:
    fixed.append( keyFormat.format( keyStringPrefix, keyword ) )

  return keywordRedisDB.sinter( fixed )

def removeFileIdFromTag( databaseID, tag ):
  #TODO: what happens if it doesn't exist ??
  keywordRedisDB.srem( keyFormat.format( keyStringPrefix, tag ), databaseID )


def getMatchingFiles( keyword ):
  return keywordRedisDB.smembers( keyFormat.format( keyStringPrefix, keyword ) )
