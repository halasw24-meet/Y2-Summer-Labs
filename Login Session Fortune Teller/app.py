from flask import Flask, render_template, request, redirect, url_for, session

import random

app = Flask(__name__, template_folder="templates")
app.secret_key = 'supersecretkey'  

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['month'] = request.form['month']
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/fortune')
def fortune():
    fates = [
        'you have to run around the basketball court 5 times',
        'Lilach the dragon blew fire on you',
        'you won instant ramen',
        'you have to attend 5 cs classes in row',
        'youll get kicked out of meet',
        'youll sleep in the bathroom',
        'you won a trip to Kazakhstan',
        'your cerfew is at 2am',
        'nothing changes',
        'youre gonna live in iasa forever'
    ]
    month_chosen = session.get('month', '')
    length = len(month_chosen)
    if length > len(fates) - 1:
        selected_fortune = fates[0]
        return render_template("fortune.html", selected=selected_fortune)
    else:
        selected_fortune = fates[length]
        return render_template("fortune.html", selected=selected_fortune)
   

@app.route('/home')
def home():
    name = session.get('name', 'Guest')
    return render_template('home.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)