#import urlHandler
import search
import filesAPI
#import thumbnailGenerator

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
  filesAPI.uploadFileFromForm( request )
  return render_template("home.html")

@app.route("/s")
@app.route("/s/")
def showSearchWithGetQuery():
  #TODO: this 'q' shouldn't be hardcoded
  query = request.args.get('q')
  if( query == None ):
    print "here1"
    return render_template("search.html", searchResults = 'test' )
  else:
    print "here2"
    searchResults = search.getSearchResultsWithQuery( query = query )
    print searchResults
    return render_template( "search.html", searchResults = searchResults )


@app.route("/s/<query>")
def showSearchWithUrlQuery(query):
  print "here3"
  searchResults = search.getSearchResultsWithQuery( query = query )
  print searchResults
  return render_template( "search.html", searchResults = searchResults )


@app.route("/thumb")
def handleThumbnailRequest():
  return send_file('./static/img/1.png', mimetype='image/gif')


if __name__ == "__main__":
  app.debug = True
  app.run()
