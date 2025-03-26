from flask import Flask, render_template, jsonify, request, redirect, session, flash
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
moedas = {
            'Bitcoin': 'BTCUSDT', 
            'Ethereum': 'ETHUSDT',
            'BNB': 'BNBUSDT',
            'Solana': 'SOLUSDT',
            'XRP': 'XRPUSDT'
        }

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
@app.route('/mainPage', methods=['GET', 'POST'])

def main_page():

    # BUY / SELL ORDER

    if request.method == 'POST':
        moeda = request.form['moeda']
        valor = float(request.form['valor'])
        simbolo = moedas[moeda]
        acao = request.form['acao']

        preco = float(client.get_symbol_ticker(symbol=simbolo)["price"])
        quantidade = round(valor / preco)
        quantidade = float(f"{quantidade:.6f}") 

        if acao == "buy":
            ordem = client.order_market_buy(symbol=simbolo, quantity=quantidade)
            flash(f'Compra realizada: {quantidade} de {moeda}', 'sucess')
        elif acao == "sell":
            ordem = client.order_market_sell(symbol=simbolo, quantity=quantidade)
            flash(f'Venda realizada: {quantidade} de {moeda}', 'sucess')

    return render_template('mainpage.html', moedas=moedas)
    

# Validacao de Login
@app.route('/validate', methods=['POST',])
def valid_login():
    if request.form['password'] == password  and request.form['username'] == user:

        session['loginPage'] = request.form ['username']

        return redirect('/mainPage')
    else:
        return redirect('/')
    
# Start app
if __name__ == '__main__':
    threading.Thread(target=fetch_prices, daemon=True).start()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
