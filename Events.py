from flask import Flask, render_template, request
import psycopg2
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, BooleanField, TextField, validators, SubmitField
from wtforms.validators import DataRequired
import os
from sqlalchemy_queries import *
import json
from flask import Flask, request, Response
from json import dumps, loads
from flask_pymongo import PyMongo
from flask import jsonify
from bson.json_util import dumps
import ast

app = Flask(__name__)
mongo = PyMongo(app)
Bootstrap(app)

#events data
with open("event_titles.txt", "r") as f:
	data= ast.literal_eval(f.read())

#performers data
with open("performer_names.txt", "r") as pdata:
	pdata = ast.literal_eval(pdata.read())
WTF_CSRF_ENABLED = False


@app.route('/api/v1/logcomment')
def get_eventsdata():
	
	query = request.args.get('comment')
	print(query)
	add_comment(query)
	return "<h1> Thanks for Submitting the comment </h1>"

class CommentsForm(Form):
	event = TextField("Comment", [validators.Length(min=0, max=100)])
	submit = SubmitField("Submit")

@app.route('/commentsubmission', methods=['GET', 'POST'])
def login():
    form = CommentsForm(csrf_enabled=False)
    return render_template('comments.html', 
                           title='Comments',
                           form=form)

@app.route("/aboutus")
def about():
	return render_template("about.html")

@app.route("/upcomingevent")
def upcomingEvent():
	eventlist = list_all_events()
	return render_template("upcomingevents.html", eventlist=eventlist)


@app.route("/")
def eventsHome():
	eventrequested = request.args.get('select_event')

	return render_template("home.html", performersdata = data, pdata=pdata)
@app.route("/events")
def searchEvent():
	eventrequested = request.args.get('select_event')
	performers= who_is_performing_at_event(eventrequested)
	#2-tuple:(performer,list_of_events)
	return render_template("events.html", participants=performers)


@app.route("/performers", methods=['GET'])
def searchPerformer():
	performerrequested = request.args.get('select_performer')

	per_events= performing_at(performerrequested)

	return render_template("performers.html", per_events=per_events)
@app.route("/generalsearch")
def genSearch():
	query = request.args.get('searchtext')
	eventPerformers = who_is_performing_at_event(query, True)
	performerEvents = performing_at(query, True)
	
	return render_template("generalsearch.html", eventPerformers=eventPerformers, performerEvents=performerEvents)
@app.route("/api/v1/eventsperformers", methods=["GET", "POST"])
def get_events():
	req = request.args.get('data')
	val = {"performer":[], "bio":[], "event":[], "description":[]}
	perdata = who_is_performing_at_event(req, True)
	qdata = performing_at(req, True)
	for performer, events in qdata:
		for event in events:
			val["performer"].append(performer.name)
			val["bio"].append(performer.shortBio)
			val["event"].append(event.title)
			val["description"].append(event.description)
	for event, performers in perdata:
		for performer in performers:
			val["performer"].append(performer.name)
			val["bio"].append(performer.shortBio)
			val["event"].append(event.title)
			val["description"].append(event.description)
	res=Response(dumps(val))
	res.headers['Access-Control-Allow-Origin'] = '*'
	res.headers['Content-type'] = 'application/json'
	return res
@app.route("/api/request")
def api_request():
	return render_template("api.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8088)

