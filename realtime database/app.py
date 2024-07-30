from flask import Flask, render_template, request, redirect, session, url_for, flash
import pyrebase

config = {
    "apiKey": "AIzaSyD2-JSUqMqir1NZl2SODzA8g4iBbspy4pc",
    "authDomain": "auth-lab2-e3841.firebaseapp.com",
    "projectId": "auth-lab2-e3841",
    "storageBucket": "auth-lab2-e3841.appspot.com",
    "messagingSenderId": "372611925185",
    "appId": "1:372611925185:web:bd4f1193e1527920300040",
    "databaseURL": "https://auth-lab2-e3841-default-rtdb.firebaseio.com/"
}

app = Flask(__name__, template_folder='Templates', static_folder='Static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            user_data = {
                "full_name": full_name,
                "email": email,
                "username": username
            }
            db.child("Users").child(uid).set(user_data)
            session['user'] = uid
            return redirect('/home')
        except:
            flash("Authentication failed")
    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['quote']
        said_by = request.form['said_by']
        uid = session['user']
        quote = {
            "text": text,
            "said_by": said_by,
            "uid": uid
        }
        db.child("Quotes").push(quote)
    return render_template('home.html')

@app.route('/display')
def display():
    quotes = db.child("Quotes").get().val()
    return render_template('display.html', quotes=quotes)

if __name__ == '__main__':
    app.run(debug=True)