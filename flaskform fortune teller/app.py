from flask import Flask, render_template

import random
app = Flask(__name__, template_folder = "templates")
fates= [ 'you have to run around the basketball court 5 times', 
'Lilach the dragon blew fire on you',
'you won instant ramen',
'you have to attend 5 cs classes in row',
'you got kicked out of meet',
'youll sleep in the bathroom',
'you won a trip to Kazakhstan',
'your cerfew is at 2am',
'nothing changes',
'youre gonna live in iasa forever' ]

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/fortune')
def fortune():
    selected_fortune = random.choice(fates)
    return render_template("fortune.html", selected= selected_fortune)
    

if __name__ == '__main__':
    app.run(debug=True)