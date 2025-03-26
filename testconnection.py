from binance.client import Client
from password import api_key, api_secret
client = Client(api_key, api_secret)

try:
    info = client.get_account()
    print("Conectado com sucesso!")
except Exception as e:
    print("Erro: Nao foi possivel conectar", e)