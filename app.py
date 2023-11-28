from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    return "Ok", 200

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    data = request.get_json()
    
    return "Ok", 200


if __name__ == '__main__':
    app.run()
