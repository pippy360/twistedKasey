import redis

keyStringPrefix = 'i_'
keyFormat = '{0}_{1}'
currentDatabaseIdKey = 'currentDatabaseId'

websiteInfoRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

def getNewDatabaseId():
  key = keyFormat.format( keyStringPrefix, currentDatabaseIdKey )
  result = websiteInfoRedisDB.get( key )
  if result == None or result == '':#FIXME: which one is it ? None or '' ?
    result = '0'

  websiteInfoRedisDB.set( key, int( result ) + 1 )

  return result
