#TODO: all this should be renamed to tag database
import redis

#only this module should know about this keyword prefix
keyStringPrefix = 'k_'
keyFormat = '{0}{1}'# '_keyword_' + the tag

keywordRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )


#TODO: explain what the fileId is
def addTags( fileId, tagsList ):
  if isinstance( tagsList, basestring):
    tagsList = [ tagsList ]

  for tag in tagsList:
    keywordRedisDB.sadd( keyFormat.format( keyStringPrefix, tag ), fileId )

def getIntersection( keywords ):
  return keywordRedisDB.sinter( keywords )

def removeFileIdFromTag( fileId, tag ):
  #TODO: what happens if it doesn't exist ??
  keywordRedisDB.srem( keyFormat.format( keyStringPrefix, tag ), fileId )


def getMatchingFiles( keyword ):
  return keywordRedisDB.smembers( keyFormat.format( keyStringPrefix, keyword ) )
