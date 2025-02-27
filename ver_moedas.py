from binance.client import Client
from password import api_key, api_secret

client = Client(api_key, api_secret, testnet =True)

# COMANDOS IMPORTANTES!!! 'buyerCommission' 'canTrade' 'canWithdraw' 'canDeposit' 'uid' 'balances' 'accountType

# puxar info da conta do usuario utilizando o bot
info = client.get_account()

active_list = info["balances"]
for i in active_list:
    print(i)