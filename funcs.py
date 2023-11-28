import requests
from requests.models import PreparedRequest
import os

DEBUG = False

GM_URL = "https://api.groupme.com/v3/bots/post"

def send_message(msg: str):
    data = {
        'bot_id': os.environ['GM_BOT_ID'],
        'text': msg,
    }

    requests.post(GM_URL, json=data)


"""
Returns a url that is used for the send message function.
Users must manually sign into Spotify to use the features
of this application.
"""
def spotify_authorization_flow() -> None:
    url = "https://accounts.spotify.com/authorize"

    params = {
        "client_id": os.environ['SPOTIFY_CLIENT_ID'],
        "response_type": "code",
        "redirect_uri": os.environ['SPOTIFY_REDIRECT_URI'],
        "scope": "user-read-private user-read-email user-modify-playback-state",
    }

    req = PreparedRequest()
    req.prepare_url(url, params)
    
    send_message(
        f"Please open this link to access the different Spotify features: {req.url}" 
    )

SPOTIFY_ACCOUNTS_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_USER_PROFILE = "https://api.spotify.com/v1/me"
SPOTIFY_ITEM_SEARCH = "https://api.spotify.com/v1/search"
SPOTIFY_REMOTE_QUEUE = "https://api.spotify.com/v1/me/player/queue"

class QueueMaster(object):

    def __init__(self):
        self.access_token = None

    def retrieve_access_token(self, auth_code: str):
        req = requests.post(SPOTIFY_ACCOUNTS_URL,
                            data={
                                'grant_type': 'authorization_code',
                                'code': auth_code,
                                'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI']
                            },
                            auth=(
                                os.environ['SPOTIFY_CLIENT_ID'],
                                os.environ['SPOTIFY_CLIENT_SECRET']
                            ))
        
        self.access_token = req.json()['access_token']

        self.get_user_profile()
        
        if DEBUG:
            self.queue_a_song("Madonna Hung Up")
        
    def get_user_profile(self):
        req = requests.get(SPOTIFY_USER_PROFILE,
                           headers={
                               'Authorization' : f"Bearer {self.access_token}",
                           })

        display_name = req.json()['display_name']
        
        send_message(f"{display_name}'s Spotify account has been linked!")
    
    """
    Since this project will remain small and among friends,
    this function will locate the first track
    submitted in a query from the groupchat. This
    endpoint is kinda shaky with how smaller artists might
    game the system by using copying relevant metadata
    from popular songs that would appear as an attractive
    alternative to what the user is looking for. For example,
    when looking up the song "This Must Be the Place" by
    The Talking Heads, if you forget 'The' in 'The Talking Heads',
    Spotify will return a song with an identical name but
    a different band. That search is still subject to change so it
    might be different going forward.
    """
    def locate_the_uri(self, query: str):
        data = {
            "q": query.replace(" ", "+"),
            "type": "track",
            "market": "US",
            "limit": "1",
        }

        req = requests.get(SPOTIFY_ITEM_SEARCH, params=data,
                           headers={
                               'Authorization': f"Bearer {self.access_token}"
                           })

        return req.json()['tracks']['items'][0]['uri']

    def queue_a_song(self, query : str):
        uri = self.locate_the_uri(query)

        data = {
            'uri': uri,
        }

        req = requests.post(SPOTIFY_REMOTE_QUEUE, params=data,
                            headers={
                                'Authorization': f"Bearer {self.access_token}"
                            })

        if req.status_code == 204:
            send_message('Song successfully added to the queue')
        else:
            send_message('Something went wrong, only Mary has access to these features...\nMake her sign in using the /signin command')
        
if __name__ == '__main__':
    spotify_authorization_flow()


    
