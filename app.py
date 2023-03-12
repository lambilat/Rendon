import os
from mediafire import MediaFireApi
from flask import Flask, request,Response
#from dotenv import load_dotenv
#load_dotenv()
app = Flask(__name__)

mediafire_api = MediaFireApi()

mediafire_session = None
def start_mediafire_client():
    global mediafire_session
    if not mediafire_session:
        try:
            mediafire_session = mediafire_api.user_get_session_token(
                email='putotoy@icloud.com',
                password='blacklist01',
                app_id='42511')

        except Exception as e:
            mediafire_session = None
            return e
        if mediafire_session:
            try:
                mediafire_api.session = mediafire_session
            except Exception as e:
                return e
    else:
        print("Already Got Session")
        return mediafire_api.session

start_mediafire_client()


@app.route('/')
def root_page():
    client_status = start_mediafire_client()
    if client_status:
        return Response(str(client_status), status=201, mimetype="text/plain")
    else:
        return Response("Hello World!", status=201, mimetype="text/plain")
    #print(ytid)
    #return Response("Hello World!", status=201, mimetype="text/plain")
    #return "Hello World!"

#if __name__ == '__main__':
#    app.run(debug=True)
