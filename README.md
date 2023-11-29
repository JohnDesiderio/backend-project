# Queue music from Groupme to Spotify!

## What's happening?

Using GroupMe, Spotify's API, and Python, I have setup an 
application where users can queue music to one's person's
device through a groupchat. That way, if someone asks for
aux and you don't know where the phone is controlling the
speaker, you can use the groupchat to sign into their 
Spotify account, queue music, and provide other people
with the opportunity to queue music as well.

## How does it work?

For this application, I setup a GroupMe groupchat. I wanted
to use GroupMe because they offer a bot that I can use to
ping my server every time someone sends a message in the
groupchat. That bot also has a 'bot_id' that I can use to
send messages from the server posing as the bot. In the 
server, using Flask, the server provides two functionalities
to the groupchat: the Spotify signin page, and the ability
to queue music from the groupchat. Using render.com to host
my server, the application waits for users to send correctly
coded messages (messages that start with '/signin' and '/queue')
before starting any action. I setup environment variables 
through render.com so anyone can download this repository
and create their own versions of the app using. This is a 
template to demonstrate how to write a simple backend
application.

## What libraries do I need?

Flask, requests, and gunicorn.
