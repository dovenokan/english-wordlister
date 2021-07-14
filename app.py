# -*- coding: UTF-8 -*-
from flask import Flask,send_from_directory,render_template,flash,redirect,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from functools import wraps
from wordlister import *
import time
from werkzeug.utils import secure_filename
import os
from passlib.hash import sha256_crypt
import sqlite3 as sql

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


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu SAYFA girceksen Giriş yap","danger")
            return redirect(url_for("home"))
    return decorated_function


class ArticleForm(Form):
    text = TextAreaField("")
    username = StringField("Kullanıcı Adı")
    email = StringField("Mail Adresi")
    password = PasswordField("Şifre")


@app.route("/",methods = ["GET","POST"])
# @login_required
def wordlisterarea():
    session["username"] = "Count"
    form = ArticleForm(request.form)
    if request.method=="POST":
        start = time.time()
        file = 0
        try:
            file = request.files['file']
        except:
            pass

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            import os
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "srt.txt"))
            wordlist = wordlister(coType="file")#[:30]
            end = time.time() - start
            import os, psutil; usedmemory = int(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
            return render_template("index.html",end=str(end)[:6],lenned=len(wordlist),wordlist=wordlist,form=form,usedmemory=usedmemory,seans=session["username"])
        else:
            text = form.text.data
            wordlist = wordlister(co=text)#[:30]
            end = time.time() - start
            import os, psutil; usedmemory = int(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
            return render_template("index.html",end=str(end)[:6],lenned=len(wordlist),wordlist=wordlist,form=form,usedmemory=usedmemory,seans=session["username"])
    return render_template("index.html",form=form,seans=session["username"])


@app.route("/home")
def home():
    form = ArticleForm(request.form)
    return render_template("home.html",form=form)


@app.route("/register",methods = ["GET","POST"])
def register():
    form = ArticleForm(request.form)
    try:
        if session["logged_in"]:
            return redirect(url_for('wordlisterarea'))
    except:
        pass
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.hash(form.password.data)
        # password = form.password.data
        with sql.connect("wordlisterdb.db") as check:
            try:
                cur = check.cursor()
                cur.execute('SELECT * FROM userlist WHERE email=? OR username=?', (email,username,))
                rows = cur.fetchall()[0]
                if rows[1]==username or rows[2]==email:
                    print("BAŞKA BİR ŞEY SEÇMEN GEREK!")
                else:
                    with sql.connect("wordlisterdb.db") as con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO userlist (username,email,password) VALUES (?,?,?)",(username,email,password) )
                        con.commit()
                        return redirect(url_for('login'))
            except:
                with sql.connect("wordlisterdb.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO userlist (username,email,password) VALUES (?,?,?)",(username,email,password) )
                    con.commit()
                    return redirect(url_for('login'))
    return render_template("register.html",form=form)


@app.route("/login",methods = ["GET","POST"])
def login():
    form = ArticleForm(request.form)
    try:
        if session["logged_in"]:
            return redirect(url_for('wordlisterarea'))
    except:
        pass
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        try:
            with sql.connect("wordlisterdb.db") as con:
                cur = con.cursor()
                cur.execute('SELECT * FROM userlist WHERE email=?', (email,))
                rows = cur.fetchall()[0]
                # if rows[3] == password:
                if sha256_crypt.verify(password, rows[3]):
                    session["logged_in"]=True
                    session["username"]=rows[1]
                    return redirect(url_for('wordlisterarea'))
        except:
            pass
    return render_template("login.html",form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/www",methods = ["GET","POST"])
def www():
    with sql.connect("wordlisterdb.db") as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM userlist')
        rows = cur.fetchall()
    return render_template("www.html",rows=rows)


@app.route("/dashboard",methods = ["GET","POST"])
def dashboard():
    with sql.connect("wordlisterdb.db") as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM userlist')
        rows = cur.fetchall()
    return render_template("dashboard.html",rows=rows)


@app.route("/delete/<string:id>",methods = ["GET","POST"])
def deleteuser(id):
    with sql.connect("wordlisterdb.db") as con:
        cur = con.cursor()
        rows = cur.fetchall()
        sorgu = "DELETE FROM userlist WHERE username=?"
        cur.execute(sorgu,(id,))
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html",rows=rows,userid=id)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join("", app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


#main()
if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=2323)
