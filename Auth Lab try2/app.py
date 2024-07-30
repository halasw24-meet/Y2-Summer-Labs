from flask import Flask, render_template, request, redirect, session, url_for, flash
import pyrebase

config = {
    'apiKey': "AIzaSyDNR3B8JKLIUSUrjno-ZntP71jCpsZR4Qs",
    'authDomain': "auth-lab-83c52.firebaseapp.com",
    'projectId': "auth-lab-83c52",
    'storageBucket': "auth-lab-83c52.appspot.com",
    'messagingSenderId': "1024499666034",
    'appId': "1:1024499666034:web:10a38df68d6a841751c6eb",
    "databaseURL": ""
}

app = Flask(__name__, template_folder='Templates', static_folder='Static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            session['user'] = auth.create_user_with_email_and_password(email, password)
            session['quotes'] = []
            return redirect(url_for('home'))
        except Exception as e:
            error = "Authentication failed: " + str(e)
            flash(error)
    return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            session['user'] = auth.sign_in_with_email_and_password(email, password)
            session['quotes'] = []
            return redirect(url_for('home'))
        except Exception as e:
            error = "Authentication failed: " + str(e)
            flash(error)
    return render_template("signin.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        quote = request.form['quote']
        session['quotes'].append(quote)
        return redirect(url_for('thanks'))
    
    return render_template("home.html")

@app.route('/thanks', methods=['GET'])
def thanks():
    return render_template("thanks.html")

@app.route('/display', methods=['GET'])
def display():
    if 'quotes' not in session:
        session['quotes'] = []
    return render_template("display.html", quotes=session['quotes'])

if __name__ == '__main__':
    app.run(debug=True)