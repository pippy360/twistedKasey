import redis

#only this module should know about this key prefix
keyStringPrefix = 'o'
keyFormat = '{0}_{1}'

objectInfoRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )#TODO: move to config file

def getObjectType( databaseId ):
  pass

def setMutli( inputDict ):
  for k, val in inputDict.iteritems():
    key = keyFormat.format( keyStringPrefix, k )
    _setVal( key, val )

def setVal( k, v ):
  key = keyFormat.format( keyStringPrefix, k )
  return _setVal( key, v )

def _setVal( key, val ):
  if isinstance( val, (int, long, float, complex, basestring) ):
    objectInfoRedisDB.set( key, val )#set proper names
  elif type( val ) is list:
    objectInfoRedisDB.delete( key )#clear list
    for e in val:
      objectInfoRedisDB.lpush( key, e )
  elif type( val ) is dict:
    objectInfoRedisDB.hmset( key, val )
  else:
    print "ERROR bad set"#TODO: learn errors


#TODO: comment
def getMulti( keys ):
  result = {}
  for k in keys:
    key = keyFormat.format( keyStringPrefix, k )
    result.update( { k: _getVal( key ) } )

  return result

def getVal( k ):
  key = keyFormat.format( keyStringPrefix, k )
  return _getVal( key )

def _getVal( key ):
  redisType = objectInfoRedisDB.type( key )
  if redisType == 'string':
    return objectInfoRedisDB.get( key )
  elif redisType == 'list':
    return objectInfoRedisDB.lrange( key, 0, -1 )
  elif redisType == 'hash':
    return objectInfoRedisDB.hgetall( key )
  else:
    return None

def getObject( databaseId ):
  pass
