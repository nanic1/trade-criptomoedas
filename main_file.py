from binance.client import Client
from password import api_key, api_secret
import time

client = Client(api_key, api_secret, testnet =True)

# COMANDOS IMPORTANTES!!! 'buyerCommission' 'canTrade' 'canWithdraw' 'canDeposit' 'uid' 'balances' 'accountType

# puxar info da conta do usuario utilizando o bot
info = client.get_account()

# puxar saldo de TODAS as moedas
lista_ativos = info["balances"]

# variaveis para definicao de valores para compra e venda de cripto
symbol = 'BTCUSDT'
compra = 84000
venda = 85500
qnt_trade = 0.01

# funcao para pegar o preco do valor de mercado da moeda em tempo REAL
def pegar_preco_atual(symbol):
    spot = client.get_symbol_ticker(symbol=symbol)
    return float(spot['price'])

# funcao para dar ordem para COMPRA
def ordem_compra(symbol, quantity):
    order = client.order_market_buy(symbol=symbol, quantity = quantity)
    print(f"Ordem de compra feita: {order}")

# funcao para dar ordem de VENDA
def ordem_venda(symbol, quantity):
    order = client.order_market_sell(symbol=symbol, quantity = quantity)
    print(f"Ordem de venda feita: {order}")

# funcao para o funcionamento do trading bot
def trading_bot():
    in_position = False

    while True:
        preco_atual = pegar_preco_atual(symbol)
        print(f"Preço atual da {symbol}: {preco_atual}")

        if not in_position:
            if preco_atual < compra:
                print(f"Preco está abaixo de ${compra}. Criando ordem de compra.")
                ordem_compra(symbol, qnt_trade)
                in_position = True
        else:
            if preco_atual > venda:
                print(f"Preco está acima de ${venda}. Criando ordem de venda")
                ordem_venda(symbol, qnt_trade)
                in_position = False
        
        time.sleep(3)


if __name__ == '__main__':
    trading_bot()