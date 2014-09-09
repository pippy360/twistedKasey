#TODO: this code doesn't work at all if the layout of FileInfo class changes while the database already has files in it
#TODO: RENAME AS FILEINFODATABASE
import redis
import databaseObjects
import copy

#only this module should know about this key prefix
keyStringPrefix = '_objectInfo_'
keyFormat = '{0}{1}_{2}'#TODO: explain this

objectInfoRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )


#this is sort of overComplicated
def storeSerializedObject( databaseId, serializedDict ):
  for k, value in serializedDict.iteritems():
    key = keyFormat.format( keyStringPrefix, k, databaseId )

    if isinstance( value, (int, long, float, complex, basestring) ):
      objectInfoRedisDB.set( key, value )#set proper names
    elif type( value ) is list:
      objectInfoRedisDB.delete( key )#clear list
      for e in value:
        objectInfoRedisDB.lpush( key, e )
    elif type( value ) is dict:
      objectInfoRedisDB.hmset( key, value )
    else:
      print "ERROR"#TODO: learn errors


def removeSerializedObject( fileId ):
  pass


def getSerializedObject( databaseId, skeletonSerializedDict ):

  s = copy.deepcopy( skeletonSerializedDict )
  #FIXME: kind of dirty fix here because i want to go to bed
  for k, value in skeletonSerializedDict.iteritems():
    key = keyFormat.format( keyStringPrefix, k, databaseId )

    if isinstance( value, (int, long, float, complex, basestring) ):
      s[k] = objectInfoRedisDB.get( key )#set proper names
    elif type( value ) is list:
      s[k] = objectInfoRedisDB.lrange( key, 0, -1 )
    elif type( value ) is dict:
      s[k] = objectInfoRedisDB.hgetall( key )
    else:
      print "ERROR"#TODO: learn errors

  return s


def getBasicFile():
  pass

