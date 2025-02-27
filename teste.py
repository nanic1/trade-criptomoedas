from binance.client import Client
from password import api_key, api_secret

client = Client(api_key, api_secret, testnet =True)

# COMANDOS IMPORTANTES!!! 'buyerCommission' 'canTrade' 'canWithdraw' 'canDeposit' 'uid' 'balances' 'accountType

# puxar info da conta do usuario utilizando o bot
info = client.get_account()

# puxar saldo de TODAS as moedas
lista_ativos = info["balances"]

# seleciona a moeda desejada
criptomoeda = input('Digite o código da moeda que deseja tradar (ex: BTC, ETH, etc): ').upper()
encontrado = False

# puxa o saldo do ativo seleciodado pelo usuario
for ativo in lista_ativos:
    if ativo['asset'] == criptomoeda:
        print(f'{criptomoeda} = {ativo['free']} {criptomoeda}')
        encontrado = True
        break

