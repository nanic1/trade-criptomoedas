from binance.client import Client
from password import api_key, api_secret

client = Client(api_key, api_secret)

status = client.get_account_status()
print(status)

# COMANDOS IMPORTANTES!!! 'buyerCommission' 'canTrade' 'canWithdraw' 'canDeposit' 'uid' 'balances' 'accountType

# puxar info da conta do usuario utilizando o bot
info = client.get_account()
for i in info:
    print(i)

# puxar saldo de TODAS as moedas
lista_ativos = info["balances"]

# puxar saldos de TODOS os ativos do usuario
for ativo in lista_ativos:
    if float(ativo["free"]) > 0:
        print(ativo)

# venda
from binance.enums import *
order = client.create.order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_MARKET,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001'
)

# mostra se o cliente pode tradar ou não
# print(info["canTrade"])