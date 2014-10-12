#import urlHandler
import search
import filesAPI
import urlHandler
import thumbnailGenerator
from databaseBuilder import build

from flask import Flask, render_template, request, send_file
app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/home/")
@app.route("/index.html")
def showIndex():
  return render_template("home.html")


@app.route("/upload/")
@app.route("/upload")
def showUpload():
  return render_template("upload.html")

@app.route("/file", methods=['GET', 'POST'])
def file():
  uploadResults = filesAPI.hanldeUploadFormSubmit( request )
  return render_template("uploadResult.html", uploadResults=uploadResults)

@app.route("/s")
@app.route("/s/")
def showSearchWithGetQuery():
  #TODO: this 'q' shouldn't be hardcoded
  query = request.args.get('q')
  if( query == None ):
    return render_template("search.html", searchResults = 'test' )
  else:
    searchResults = search.getSearchResultsWithQuery( query = query )
    return render_template( "search.html", searchResults = searchResults )


@app.route("/s/<query>")
def showSearchWithUrlQuery(query):
  searchResults = search.getSearchResultsWithQuery( query = query )
  return render_template( "search.html", searchResults = searchResults )


@app.route("/thumb")
def handleThumbnailRequest():
  return thumbnailGenerator.handleThumbnailRequest( request )

@app.route("/build")
def showBuildPage():
  imageFilenamesListString = build.handlePageLoad( request )
  return render_template("build.html", imageFilenamesListString=imageFilenamesListString)

if __name__ == "__main__":
  app.debug = True
  app.run()
