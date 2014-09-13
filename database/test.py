import databaseObjects
import databaseFunctions


tom = databaseFunctions.createSerializeObj( {'here':'test'}, '401', 'testObj' )
#print tom
#databaseFunctions.storeSerializedObject( tom )
bob = databaseFunctions.getSerializedObject( '401' )
#print bob

tom = databaseObjects.SearchableObject( getNewDatabaseId() )

tom.files = []
bob = databaseObjects.ImageFile( getNewDatabaseId(), '1', '2', '3', '4' )

tom.files.append( bob )

tom.save()

tom = databaseObjects.SearchableObject( 'id_333', '5', '6', '7', '8' )

tom.load()

print databaseFunctions.getObjectType( 'id_444' )
