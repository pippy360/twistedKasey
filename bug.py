class fileStore():

  files = []

  def __init__( self ):
    pass

  def addFile( self, newFile ):
    self.files.append( newFile )

  #erase All Files And Add A New One
  def eraseAllFilesAndAddANewOne( self, newFile ):
    self.files = []
    self.files.append( newFile )


#code
tom  = fileStore()
john = fileStore()

tom.eraseAllFilesAndAddANewOne( 'file1' )
john.eraseAllFilesAndAddANewOne( 'file2' )

print tom.files