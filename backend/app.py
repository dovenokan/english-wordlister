# -*- coding: UTF-8 -*-
################################################################################################
import functools
import pymongo
from collections import Counter
import json
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, send_from_directory,render_template,flash,redirect,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from functools import wraps
from wordlister import *
import time
from werkzeug.utils import secure_filename
import os
import sqlite3 as sql
################################################################################################
app = Flask(__name__,static_folder="templates/static")
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
################################################################################################
app.secret_key = "secret key" 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
################################################################################################
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
################################################################################################
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
################################################################################################
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'srt'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
################################################################################################
class ArticleForm(Form):
    text = TextAreaField("")
    mongo_title = TextAreaField("")
################################################################################################
def Infere(data):
    oxford = [w["oxford"] for w in data if w["oxford"] != "other"]
    typical = [w["type"] for w in data]
    data_len = len(data)
    oxford_len = len(oxford)
    oxford_level_count = dict(Counter(oxford))
    oxford_level_count["total"] = oxford_len
    typical_count = dict(Counter(typical))
    typical_count["total"] = data_len

    stats = {
        "oxford_count_by_level":oxford_level_count,
        "typical_count":typical_count,
        "percentage": {
            "oxford": {
                "total": (oxford_len/data_len)*100,
                "a1": (oxford_level_count["a1"]/data_len)*100,
                "a2": (oxford_level_count["a2"]/data_len)*100,
                "b1": (oxford_level_count["b1"]/data_len)*100,
                "b2": (oxford_level_count["b2"]/data_len)*100,
                "c1": (oxford_level_count["c1"]/data_len)*100,
                "other":((data_len-oxford_len)/data_len)*100,
            },
            "typical":{
                "verb": (typical_count["verb"]/data_len)*100,
                "noun": (typical_count["noun"]/data_len)*100,
                "adjective": (typical_count["adj"]/data_len)*100,
                # "phrasal_verb": (typical_count["phrverb"]/data_len)*100,
            }
        }
    }
    return stats
################################################################################################
@app.route("/")
def index():
    return render_template("index.html")
################################################################################################
@app.route("/api",methods = ["GET","POST"])
# @cross_origin(allow_headers=['Content-Type'])
def api():
    TIME_START = time.time()
    form = ArticleForm(request.form)
    text = form.text.data
    data = wordlister(content=text)
    stats = Infere(data["wordlist"])
    TIME_END = time.time() - TIME_START
    info = {
        "time": TIME_END,
        "count": len(data["wordlist"])
    }
    response = json.dumps({"info":info, "wordlist":data["wordlist"], "stats":stats})
    return response
################################################################################################
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join("", app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)
################################################################################################
if __name__ == '__main__':
    app.run()