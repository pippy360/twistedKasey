#the urls should really go here.....but i can't do that atm the moment because i don't know how :/
from flask.ext.classy import FlaskView, route
from flask import request, current_app, redirect

@route("/test")
def testSomething():
  return "hello world"
