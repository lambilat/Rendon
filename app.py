import os
from mediafire.client import (MediaFireClient, File, Folder)
from flask import Flask, request,Response
#from dotenv import load_dotenv
#load_dotenv()
app = Flask(__name__)



client = None
def start_mediafire_client():
    global client
    try:
        client = MediaFireClient()
        client.login(email=os.getenv('mediafire_email'),
            password=os.getenv("mediafire_pass"),
            app_id="42511"
            )
    except Exception as e:
        client = None
        return str(e)
start_mediafire_client()




mediafire_files = []


@app.route('/files')
def get_files_page():
    global mediafire_files
    if not client:
        start_mediafire_client_resp = start_mediafire_client()

    if os.getenv('getfiles') == "1":
        print(mediafire_files)
        mediafire_files = []
        print("File Cleared")
    return Response("Internal Server Error.", status=404, mimetype="text/plain")

@app.route('/')
def root_page():
    global mediafire_files

    resp_err_txt = "<br> Error <br>"

    if not client:
        start_mediafire_client_resp = start_mediafire_client()
        if start_mediafire_client_resp:
            "<br> Mediafire Client: "+start_mediafire_client_resp+"<br>"


    ytid = request.args.get("ytid")

    resp_err_txt += "<br> Youtube ID: "+str(request.args.get("ytid"))+"<br>"
    isgood = False
    if ytid and client:
        print("Youtube ID:",ytid)
        #resp_err_txt += " Youtube ID: "+ytid+"<br>"
        if not mediafire_files:
            try:
                for item in client.get_folder_contents_iter("mf:/karaoke"):
                    if type(item) is File:
                        mediafire_files.append(item['filename'])
                        #print("File: {}".format(item['filename']))
            except Exception as e:
                resp_err_txt += str(e)+"<br>"
                pass


        if mediafire_files:
            if ytid in mediafire_files:
                resp_err_txt += " File Found<br>"
                print("File Found, Getting DL Url.")
                try:
                    dl_url = client.get_file_dl_url("mf:/karaoke/"+ytid)
                    if dl_url:
                        isgood = True
                except Exception as e:
                    resp_err_txt += str(e)+"<br>"
                    pass
            else:
                resp_err_txt += " File Not Found<br>"
                print("File Not Found")

    if isgood:
        return Response(dl_url, status=201, mimetype="text/plain")
    else:
        resp_err_txt += "<br> ENV Email: "+str(os.getenv('mediafire_email'))+"<br>"
        return Response(resp_err_txt, status=404, mimetype="text/plain")

    #print(ytid)
    #return Response("Hello World!", status=201, mimetype="text/plain")
    #return "Hello World!"

#if __name__ == '__main__':
#    app.run(debug=True)
