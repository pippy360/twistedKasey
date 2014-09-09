#TODO: all this should be renamed to tag database
import redis

#only this module should know about this keyword prefix
keyStringPrefix = '_keyword_'
keyFormat = '{0}{1}'# '_keyword_' + the tag

keywordRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )


#TODO: explain what the fileId is
def addTags( fileId, tagsList ):
  if isinstance( tagsList, basestring):
    tagsList = [ tagsList ]

  for tag in tagsList:
    keywordRedisDB.sadd( keyword.format( keyFormat, tag ), fileId )


def removeFileIdFromTag( fileId, tag ):
  #TODO: what happens if it doesn't exist ??
  keywordRedisDB.srem( keyword.format( keyFormat, tag ), fileId )


def getMatchingFiles( keyword ):
  return keywordRedisDB.smembers( keyword.format( keyFormat, keyword ) )
