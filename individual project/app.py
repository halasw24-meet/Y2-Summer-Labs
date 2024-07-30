from flask import Flask, render_template, request, redirect, session, url_for, flash
import pyrebase

config = {
  "apiKey": "AIzaSyAeqKdgzQamQS_293fT_J5KDbHx5ppgxkA",
  "authDomain": "authlab3-a9216.firebaseapp.com",
  "projectId": "authlab3-a9216",
  "storageBucket": "authlab3-a9216.appspot.com",
  "messagingSenderId": "941169770674",
  "appId": "1:941169770674:web:0d8e616c1e2ae1847c89ab",
  "databaseURL": "https://authlab3-a9216-default-rtdb.europe-west1.firebasedatabase.app/"
}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username= request.form['username']
        description= request.form['description']
        try:

            session['user'] = auth.create_user_with_email_and_password(email, password)
            UID= session['user']['localId']
            user= {"name": username, "email":email, "description": description, "password": password}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except Exception as e:
            error = "Authentication failed: " + str(e)
            flash(error)
    return render_template("signup.html")

@app.route('/profile')
def profile():
    if 'user' in session:
        UID= session['user']['localId']
        user= db.child("Users").child(UID).get().val()
        return render_template("profile.html", user_profile= user)
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except Exception as e:
            error = "Authentication failed: " + str(e)
            flash(error)
    return render_template("signin.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.clear()
    return redirect(url_for('signup'))

@app.route('/classics')
def classics():
    return render_template("classics.html")

@app.route('/fantasy')
def fantasy():
    return render_template("fantasy.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/lists')
def lists():
    return render_template("lists.html")

@app.route('/mentalhealth')
def mentalhealth():
    return render_template("mentalhealth.html")

@app.route('/mystery')
def mystery():
    return render_template("mystery.html")

@app.route('/romance')
def romance():
    return render_template("romance.html")



if __name__ =="__main__":
  app.run(debug=True)

