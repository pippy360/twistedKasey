import redis

#only this module should know about this keyword prefix
keywordStringPrefix = '_keyword_'
keywordRedisDB = redis.StrictRedis( '127.0.0.1', 6379)

#TODO: explain what the imageId is
def addTags( imageId, tagsList ):

  if isinstance( tagsList, basestring):
    tagsList = [ tagsList ]

  for tag in tagsList:
    keywordRedisDB.sadd( keywordStringPrefix + tag, imageId )

  return


def getMatchingImages( keyword ):
  return keywordRedisDB.smembers( keywordStringPrefix + keyword )
