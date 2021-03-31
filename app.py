import os
import requests
from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__, instance_relative_config=True)

# https://exploreflask.com/en/latest/configuration.html
app.config.from_object("config.Config")


@app.route('/', methods=['GET'])
def proxy_get():
    url = 'https://ropsten.infura.io/v3/a59bcf7866054389bf76c4653674302e'
    return send_from_directory('templates','index.html')

@app.route('/eth-proxy', methods=['POST'])
def proxy_post():
    """
    an experiment
    :return:
    """
    return jsonify(message = "Posted")

@app.route('/etherscan/gas.json')
def gas_estimate():
    # https: // api.etherscan.io / api?module = gastracker & action = gasestimate & gasprice = 2000000000 & apikey = YourApiKeyToken
    # https: // api.etherscan.io / api?module = gastracker & action = gasoracle & apikey = YourApiKeyToken
    fields = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": app.config.get('ETHERSCAN_API_KEY')
    }
    res = requests.get(app.config.get('ETHERSCAN_API_URL'), params=fields)
    oracle = res.json()
    fields = {
        "module": "stats",
        "action": "ethprice",
        "apikey": app.config.get('ETHERSCAN_API_KEY')
    }
    res = requests.get(app.config.get('ETHERSCAN_API_URL'), params=fields)
    ethprice = res.json()
    return jsonify({"oracle":oracle, "ethprice": ethprice})

if __name__ == '__main__':
    app.run()
