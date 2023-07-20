import random
import json

import torch
import requests

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('C:/WebDev/bff_cryptomaniac/cryptomaniac/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "C:\\WebDev\\bff_cryptomaniac\\cryptomaniac\\data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def get_response(msg):
    if ("price" in msg)and("bitcoin" in msg):
        # Make a GET request to the Coinbase API to get the current price of Bitcoin in USD
        response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')

        # Parse the response JSON
        data = response.json()

        # Extract the price from the JSON
        price = data['data']['amount']

        # Print the price
        s = f"The current price of Bitcoin is {price} USD."
        return s

    if ("price" in msg) and ("binance" in msg):

        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Binance Coin is {price} USD."
        return s
    
    if ("price" in msg) and ("doge" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Dogecoin is {price} USD."
        return s
    if ("price" in msg) and ("polka" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=DOTUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Polkadot is {price} USD."
        return s
    if ("price" in msg) and ("ethereum" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT')
        data = response.json()
        price = data['price']
        s=  f"The current price of Ethereum is {price} USD."
        return s
    
    if ("price" in msg) and ("chain" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=LINKUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Chainlink is {price} USD."
        return s
    
    if ("price" in msg) and ("solana" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Solana is {price} USD."
        return s
    
    if ("price" in msg) and ("stellar" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=XLMUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Stellar is {price} USD."
        return s

    if ("price" in msg) and ("ripple" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Ripple is {price} USD."
        return s
    
    if ("price" in msg) and ("cardano" in msg):
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT')
        data = response.json()
        price = data['price']
        s = f"The current price of Cardano is {price} USD."
        return s


    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        resp =""
        sentence = input("You: ")
        
        if sentence == "quit":
            break
        
        else:
            resp = get_response(sentence)
       
        print(resp)