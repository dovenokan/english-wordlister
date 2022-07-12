# -*- coding: UTF-8 -*-
################################################################################################
import functools
import pymongo
from flask import Flask,send_from_directory,render_template,flash,redirect,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from functools import wraps
from wordlister import *
import time
from werkzeug.utils import secure_filename
import os
from passlib.hash import sha256_crypt
import sqlite3 as sql
################################################################################################
app = Flask(__name__,static_folder="templates/static")
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
    username = StringField("Kullanıcı Adı")
    email = StringField("Mail Adresi")
    password = PasswordField("Şifre")
################################################################################################
@app.route("/")
def index():
    return render_template("index.html")
################################################################################################
@app.route("/",methods = ["POST"])
def wordlisterarea():
    form = ArticleForm(request.form)
    text = form.text.data
    data = wordlister(co=text)
    return {"info":len(data),"data": data}
################################################################################################
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join("", app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)
    # return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename)
################################################################################################
if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=1453)