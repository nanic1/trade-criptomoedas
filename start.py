from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

user = 'admin'
password = 'senhasegura123'

@app.route('/login')
def login():
    return render_template ('login.html')

@app.route('/valid_login', methods=['POST',])
def valid_login():
    if request.form['password'] == password  and request.form['username'] == user:

        session['loginPage'] = request.form ['username']

        return redirect('/mainPage')
    else:
        return redirect('/login')
    
app.run(debug=True)