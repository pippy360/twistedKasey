import redis

#only this module should know about this keyword prefix
keyStringPrefix = 'h_'
keyFormat = '{0}{1}'

fileHashRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )

#returns a list containing the fileDatabaseId and the id of the related searchable object
def getRelatedIds( fileHash ):
  vals = _get( fileHash )
  if not vals:
    return None

  print 'vals'
  print vals
  return vals

#TODO: this private getter setter should be copied across all files
def _get( key ):
  return fileHashRedisDB.hgetall( keyFormat.format( keyStringPrefix, key ) )

def set( fileHash, searchableDatabaseId, fileDatabaseId ):
  return _set( fileHash, { 'searchableId':searchableDatabaseId, 'fileId':fileDatabaseId } )

def _set( key, vals ):
  fileHashRedisDB.delete( key )
  return fileHashRedisDB.hmset( keyFormat.format( keyStringPrefix, key ), vals )
