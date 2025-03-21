from flask import Flask, render_template, render_template_string, request, redirect, session
from flask_socketio import SocketIO
from binance.client import Client
from password import api_key, api_secret
import threading
import time

app = Flask(__name__)

client = Client(api_key, api_secret)
socketio = SocketIO(app, cors_allowed_origins='*')

user = 'admin'
password = 'senhasegura123'
app.secret_key = 'Batat@12!'
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']

@app.route('/')
def login():
    return render_template ('login.html')

def fetch_prices():
    while True:
        prices = {}
        for symbol in symbols:
            try:
                ticker = client.get_symbol_ticker(symbol=symbol)
                prices[symbol] = float(ticker['price'])
            except Exception as e:
                prices[symbol] = f"Erro: {str(e)}"
        socketio.emit('update_prices', prices)
        time.sleep(1)  # Atualiza a cada 2 segundos

@app.route('/mainPage')
def main_page():
    return render_template('mainpage.html')

@app.route('/validate', methods=['POST',])
def valid_login():
    if request.form['password'] == password  and request.form['username'] == user:

        session['loginPage'] = request.form ['username']

        return redirect('/mainPage')
    else:
        return redirect('/login')
    

if __name__ == '__main__':
    threading.Thread(target=fetch_prices, daemon=True).start()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
