from flask import Flask, request, Response
import os
import requests
from funcs import send_message, QueueMaster, spotify_authorization_flow

app = Flask(__name__)

controller = QueueMaster()

@app.route('/', methods=['GET', 'POST'])
def webhook():
    return "Ok", 200

@app.route('/groupme', methods=['GET', 'POST'])
def groupme():
    data = request.get_json()

    if data['text'].startswith('/signin'):
        spotify_authorization_flow()
    elif data['text'].startswith('/queue'):
        controller.queue_a_song(data['text'][6:])
    
    return Response(
        'Most people prolly will not be able to see this',
        mimetype='application/json'
    )

        
@app.route('/token', methods=['GET'])
def receive_token():
    data = request.values.to_dict()

    controller.retrieve_access_token(data['code'])

    return Response(
        'The groupchat is connected to Spotify. You can exit this webpage.',
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run()
