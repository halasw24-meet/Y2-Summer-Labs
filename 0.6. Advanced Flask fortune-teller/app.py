from flask import Flask, render_template, request, redirect, url_for

import random
app = Flask(__name__, template_folder = "templates")


@app.route('/fortune/<month_chosen>')
def fortune(month_chosen):
    fates= [ 'you have to run around the basketball court 5 times', 
    'Lilach the dragon blew fire on you',
    'you won instant ramen',
    'you have to attend 5 cs classes in row',
    'youll get kicked out of meet',
    'youll sleep in the bathroom',
    'you won a trip to Kazakhstan',
    'your cerfew is at 2am',
    'nothing changes',
    'youre gonna live in iasa forever']
    length = len(month_chosen)
    if length > len(fates) - 1:
        selected_fortune = fates[0]
        return render_template("fortune.html", selected=selected_fortune)
    else:
        selected_fortune = fates[length]
        return render_template("fortune.html", selected=selected_fortune)

@app.route('/home', methods=['GET','POST'])
def home():

    if request.method == 'GET':
        return render_template('home.html')
    else:
        month = request.form['month']
        return redirect(url_for('fortune', month_chosen= month))

if __name__ == '__main__':
    app.run(debug=True)