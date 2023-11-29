from flask import Flask, request, Response
import os
import requests
from funcs import send_message, QueueMaster, spotify_authorization_flow

app = Flask(__name__)

controller = QueueMaster()

@app.route('/groupme', methods=['GET', 'POST'])
def groupme():
    data = request.get_json()

    if data['text'].startswith('/signin'):
        spotify_authorization_flow()
    elif data['text'].startswith('/queue'):
        controller.queue_a_song(data['text'][6:])
    
    return Response(
        '<h1>Most people prolly will not be able to see this</h1>',
        mimetype='text/html'
    )

        
@app.route('/token', methods=['GET'])
def receive_token():
    data = request.values.to_dict()

    controller.retrieve_access_token(data['code'])

    return Response(
        '<h1>The groupchat is connected to Spotify. You can exit this webpage.</h1>',
        mimetype='text/html'
    )

if __name__ == '__main__':
    app.run()
