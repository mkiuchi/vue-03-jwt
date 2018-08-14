#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Damn simple IPTV Server for Kodi's IPTV Simple client addon
#
# Install
#  $ python3 -m pip install flask --user
# Start
#  $ FLASK_APP=start.py python3 -m flask run --host=0.0.0.0
# Start(Debug Mode)
#  $ FLASK_APP=start.py FLASK_DEBUG=1 python3 -m flask run --host=0.0.0.0
from flask import Flask, Response, request
from flask_cors import CORS
import os, sys, json, logging
import MySQLdb

logging.getLogger('flask_cors').level = logging.DEBUG
app = Flask(__name__)
CORS(app, resources={"/auth*": {"origins": "http://localhost:8080"}})

@app.route('/')
def pong():
    return 'Pong'

@app.route('/auth')
def auth():
    flg = False
    uname = request.args.get('username', '')
    upass = request.args.get('password', '')
    
    db = MySQLdb.connect(host="localhost",user="vuejs",passwd="vuejs",db="vuejs",charset="utf8")
    cur = db.cursor()
    qstr = "SELECT password FROM auth WHERE name = '"+uname+"';"
    cur.execute(qstr)
    rows = cur.fetchall()
    for row in rows:
        if upass == row[0]:
            return json.dumps({"result": "success"})
    return json.dumps({"result": "fail"})
