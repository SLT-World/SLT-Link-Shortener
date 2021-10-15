# -*- coding: utf-8 -*-

import random, json
from datetime import datetime
from flask import *
from werkzeug.exceptions import HTTPException
from slugify import slugify

app = Flask(
	__name__,
	template_folder='public',
	static_folder='static'
)

@app.route('/')
def index_page():
  return render_template(
    'index.html',
  )

@app.errorhandler(Exception)
def error(e):
	code = 500
	if isinstance(e, HTTPException):
		code = e.code
	return render_template("error.html", error=str(e)), code

@app.route("/<NAME>/", methods=["GET"])
def Link_Page(NAME):
  with open("Database.json", "r") as file:
    database = json.load(file)

  for item in database["links"]:
    if (item["name"] == NAME):
      return redirect(item["url"])

  return redirect(f"../")

@app.route("/new", methods=["POST"])
def new():
  with open("Database.json", "r") as file:
    database = json.load(file)

  _name = request.form.get("name")
  _url = request.form.get("url")

  _name = slugify(_name)

  for item in database["links"]:
    if (item["name"] == _name):
	    return render_template("error.html", error="Name is already used.")
  
  LinkObject = {"name": _name, "url": _url}
  
  database["links"].append(LinkObject)

  with open("Database.json","w") as f:
    json.dump(database, f, indent=2)

  return render_template("link.html", name=_name, url=_url, short_url="https://slshort.sltworld.cf/"+_name)

if __name__ == "__main__":
  app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000)
)