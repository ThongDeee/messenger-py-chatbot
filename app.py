import credentials
import requests
import json
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'สอบถามบริการของร้านได้ครับ'



# Adds support for GET requests to our webhook
@app.route('/webhook',methods=['GET'])
def webhook_authorization():
    verify_token = request.args.get("EAAYXNRGZCYRUBAFiTa0Qvcz1E8Hw91Cav4KLIYZBq3hIh5G1wStqYn0GnEk1m6EsWWrpCh8ZBQhZBAbcUbLo06YpvsvgsybgdFU8aAGaQOlHdVWvSDDulN4s1jZB6stuKznqz6eO5DFw1GeE2I1kbG1md26fDxev2mAbByNYjZBe10GLTZCgDuq")
    # Check if sent token is correct
    if verify_token == credentials.WEBHOOK_VERIFY_TOKEN:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorize.'


@app.route("/webhook", methods=['POST'])
def webhook_handle():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
                'recipient': {
                    'id': sender_id
                },
                'message': {"text":"hello, world!"}
            }
        response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+credentials.TOKEN,json=request_body).json()
        return response
    return 'ok'

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
