from flask import render_template, request, redirect, url_for , session, flash
from app import app
from passlib.hash import sha256_crypt
from pymongo import MongoClient
from app.removeScripts import specialchar
from bson import ObjectId

# table = create a table instance
cluster = MongoClient("mongodb+srv://<username>:<password>@<clustername>-g5z92.mongodb.net/<db_name>?retryWrites=true&w=majority")
db = cluster.get_database('<db_name>')
table = db.fakebook

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method =="POST":
        mail = request.form["Email"]
        username = request.form["username"]
        user = table.find_one({"username": username})
        sp = specialchar()
        if sp.spRemover(username) == False:
            flash("special characters are not allowed in username except '_'", "danger")
            return redirect(url_for('register'))
        else:
            if user is not None:
                flash("user already exsists", "warning")
                return redirect(url_for('register'))
            else:
                key = request.form["key"]
                key2 = request.form["confirm"]
                if key != key2:
                    flash("password didn't match", "warning")
                    return redirect(url_for('register'))
                else:
                    encryptKey = sha256_crypt.encrypt(str(key))
                    dictonary = {
                        'username': username,
                        'mail': mail,
                        'password': encryptKey
                    }
                    table.insert_one(dictonary)
                    return redirect(url_for(login))

    return render_template('registration.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["userName"]
        password = request.form["pass"]
        user = table.find_one({"username": username})
        if user is None:
            flash("Username not found..!", "danger")
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(password, user["password"]):
                userID = str(user["_id"])
                session['id'] = userID
                flash("you are logged in", "success")
                return redirect(url_for('profile1'))
            else:
                flash("wrong password , check your password", "danger")
                return redirect(url_for('login'))


    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop("id", None)
    flash("you are logged out", "info")
    return redirect(url_for('login'))

@app.route('/details')
def details():
    return render_template('details.html')

#routes after login
@app.route('/profile1')
def profile1():
    if "id" in session:
        id = session.get("id")
        id = ObjectId(id)
        person = table.find_one({"_id": id})
        per = person["username"]
        return render_template("logged/user.html", a = per)
    else:
        return redirect(url_for('login'))

@app.route('/profile2')
def profile2():
    if "id" in session:
        return render_template("logged/user2.html")
    else:
        return redirect(url_for('login'))