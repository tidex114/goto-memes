from flask import Flask, render_template, request, redirect, session
import sqlite3
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = "SK*HbPI]AMToPzt*8WycvXS$:nRbB"
memes = None


@app.route('/')
def main():
    conn = sqlite3.connect('memes.db')
    c = conn.cursor()
    c2 = conn.cursor()
    c.execute("SELECT * FROM memeTable")
    result = c.fetchall()
    c2.execute("SELECT * FROM comments")
    result2 = c2.fetchall()

    return render_template('main.html', memes=result, comments=result2)


@app.route('/add')
def add_form():
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def adding():
    if request.form.get('url', '') != '':
        conn = sqlite3.connect('memes.db')
        c = conn.cursor()
        memeURL = request.form.get('url', '')
        memeDESCSR = request.form.get('descr', '')
        userID = session['login']
        c.execute("INSERT INTO memeTable (url, descr, time, userID) VALUES (?, ?, ?, ?)",
                  (memeURL,
                   memeDESCSR,
                   int(time.time()),
                   userID))
    print("added")
    print(session['login'])
    conn.commit()
    conn.close()
    return redirect("/")


@app.route('/delete')
def delete():
    conn = sqlite3.connect('memes.db')
    c = conn.cursor()
    deleteID = request.args.get('id', '')
    c.execute("DELETE FROM memeTable WHERE id = ?", [deleteID])
    c.execute("DELETE FROM comments WHERE meme_id = ?", [deleteID])
    conn.commit()
    conn.close()

    return redirect("/")


@app.route('/search', methods=['POST'])
def find():
    conn = sqlite3.connect('memes.db')
    c = conn.cursor()
    search = request.form.get('search', '')
    if search:
        c.execute("SELECT * FROM memeTable WHERE descr = ? OR id LIKE ?", [search, "%" + search + "%"])
    else:
        c.execute('SELECT * FROM memeTable')
    memes = c.fetchall()
    conn.close()

    return render_template("main.html", memes=memes, search=search)


@app.route('/add_comment', methods=['POST'])
def add_comment():
    conn = sqlite3.connect('memes.db')
    c = conn.cursor()
    comment = request.form.get('newcomm', '')
    memeID = request.args.get('memeID', '')

    if comment != '':
        c.execute("INSERT INTO comments (text, meme_id, userLogin) VALUES (?,?, ?)", (comment, memeID, session['login']))

        print("commented")
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete_comment')
def delete_comment():
    conn = sqlite3.connect('memes.db')
    c = conn.cursor()
    comment_id = request.args.get('id', '')
    c.execute("DELETE FROM comments WHERE id = ?", [comment_id])
    conn.commit()
    conn.close()
    print("wasted")
    return redirect("/")


@app.route('/register', methods=['POST'])
def register():
    conn = sqlite3.connect('memes.db')
    c = conn.cursor()
    login = request.form.get('login', '')
    password = request.form.get('pass', '')

    try:
        c.execute("INSERT INTO users (login, password) VALUES (?,?)", [login, password])
        c.execute("SELECT * FROM users WHERE login = ? AND password = ?", [login, password])
        user = c.fetchone()
        if user:
            session['id'] = user[0]
            session['login'] = login
            session['logged'] = True
            print("registered")
            conn.commit()
            conn.close()
            return redirect('/')
    except:
        conn.close()
        return render_template("error.html")


@app.route('/register')
def reg_form():
    return render_template('register.html')


@app.route('/login', methods=["POST"])
def login():
    conn = sqlite3.connect('memes.db')
    c = conn.cursor()
    login = request.form.get('login', '')
    password = request.form.get('password', '')
    c.execute("SELECT * FROM users WHERE login = ? AND password = ?", [login, password])
    user = c.fetchone()
    print(c.fetchone())
    if user:
        session['id'] = user[0]
        session['login'] = login
        session['logged'] = True
        print('logged')
        return redirect('/')
    conn.commit()
    conn.close()
    return redirect('/login')


@app.route('/login')
def login_form():
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('id', None)
    session['logged'] = False
    return redirect("/login")


app.run(debug=True)
