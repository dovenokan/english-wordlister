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
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'srt'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
################################################################################################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu SAYFA girceksen Giriş yap","danger")
            return redirect(url_for("home"))
    return decorated_function
################################################################################################
class ArticleForm(Form):
    text = TextAreaField("")
    mongo_title = TextAreaField("")
    username = StringField("Kullanıcı Adı")
    email = StringField("Mail Adresi")
    password = PasswordField("Şifre")
################################################################################################
def MongoSave(cargo):
    client = pymongo.MongoClient("mongodb+srv://eUCEE8DPZYKR6zcY:eUCEE8DPZYKR6zcY@cluster0.ttarq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["oxfdb"]
    col = db["data"]
    col.insert_one(cargo)
################################################################################################
@app.route("/",methods = ["GET","POST"])
# @login_required   
def wordlisterarea():
    session["username"] = "Count"
    form = ArticleForm(request.form)
    if request.method=="POST":
        file = 0
        try:
            file = request.files['file']
        except:
            pass
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "srt.txt"))
            job = wordlister(coType="file")
            wordlist = job[0]
            stats = job[1]
            allWordsCount = job[2]
            mongo_title = form.mongo_title.data.lower()
            
            if len(mongo_title) > 3:
                MongoSave(
                    {mongo_title:stats}
                ) 
            return render_template("index.html",lenned=len(wordlist),wordlist=wordlist,stats=stats,allWordsCount=allWordsCount,form=form,seans=session["username"])
        else:
            text = form.text.data
            mongo_title = form.mongo_title.data.lower()
            job = wordlister(co=text)
            wordlist = job[0]
            stats = job[1]

            if len(mongo_title) > 3:
                MongoSave(
                    {mongo_title:stats}
                )  
            return render_template("index.html",lenned=len(wordlist),wordlist=wordlist,stats=stats,form=form,seans=session["username"])
    return render_template("index.html",form=form,seans=session["username"])
################################################################################################
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join("", app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)
################################################################################################
@app.route('/stats')
def readStats():
    client = pymongo.MongoClient("mongodb+srv://eUCEE8DPZYKR6zcY:eUCEE8DPZYKR6zcY@cluster0.ttarq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["oxfdb"]
    col = db["data"]
    data = []
    for d in col.find():
        data.append( list(d.items()) )
    return render_template("stats.html",data=data)
################################################################################################
if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=9191)