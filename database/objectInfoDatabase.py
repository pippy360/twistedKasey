#there's a problem here with that databaseId, should we be using a databaseId ? nope
import redis

#only this module should know about this key prefix
keyStringPrefix = 'o'
keyFormat = '{0}_{1}'

objectInfoRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )#TODO: move to config file

def getObjectType( databaseId ):
  pass

def setMutli( serializedObj ):
  for k, val in serializedObj.iteritems():
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

#def getMulti( keys ):
#  pass

#TODO: comment
def getMultiWithStub( keyStub, removeStub=True ):#TODO: rename this to what it actually does
  #FIXME: THERE IS AN ERROR HERE IF THE ID IS 2 NUMBERS LIKE 22 will be returned, fix ? maybe get with stub is a bad idea
  result = {}
  k = keyFormat.format( keyStringPrefix, keyStub )
  print objectInfoRedisDB.keys( k+'*' )
  for key in objectInfoRedisDB.keys( k+'*' ):
    if removeStub:
      resultKey = key.replace( k, '' )
    else:
      resultKey = key.replace( keyStringPrefix, '' )
    result.update( { key.replace( k, '' ) : _getVal( key ) } )

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
