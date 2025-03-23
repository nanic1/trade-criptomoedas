from flask import Flask, render_template, jsonify, request, redirect, session
from flask_socketio import SocketIO
from binance.client import Client
from password import api_key, api_secret
import threading
import time
import requests

app = Flask(__name__)

client = Client(api_key, api_secret)
socketio = SocketIO(app, cors_allowed_origins='*')

user = 'admin'
password = 'senhasegura123'
app.secret_key = 'Batat@12!'
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']

# Pagina de Login
@app.route('/')
def login():
    return render_template ('login.html')

# Funcao para definir precos de diversas criptomoedas em tempo real
def fetch_prices():
    while True:
        prices = {}
        for symbol in symbols:
            try:
                ticker = client.get_symbol_ticker(symbol=symbol) # Atualiza todas as moedas dentro de symbols
                prices[symbol] = float(ticker['price'])
            except Exception as e:
                prices[symbol] = f"Erro: {str(e)}"
        socketio.emit('update_prices', prices)
        time.sleep(1)  # Atualiza a cada 2 segundos

# Pagina Principal
@app.route('/mainPage')
def main_page():
    return render_template('mainpage.html')

# Validacao de Login
@app.route('/validate', methods=['POST',])
def valid_login():
    if request.form['password'] == password  and request.form['username'] == user:

        session['loginPage'] = request.form ['username']

        return redirect('/mainPage')
    else:
        return redirect('/login')
    
# Start app
if __name__ == '__main__':
    threading.Thread(target=fetch_prices, daemon=True).start()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
