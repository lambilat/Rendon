import os,sys
from mediafire.client import (MediaFireClient, File, Folder)
from flask import Flask, request,Response
#from dotenv import load_dotenv
#load_dotenv()
app = Flask(__name__)

try:
    client = MediaFireClient()
    client.login(email=os.environ.get('mediafire_email'),
        password=os.environ.get('mediafire_pass'),
        app_id="42511"
        )
except Exception as e:
    client = None


mediafire_files = []


@app.route('/files')
def get_files_page():
    global mediafire_files
    if os.environ.get('getfiles') == "1":
        print(mediafire_files)
        mediafire_files = []
        print("File Cleared")
    return Response("Internal Server Error.", status=404, mimetype="text/plain")

@app.route('/')
def root_page():
    global mediafire_files

    ytid = request.args.get("ytid")
    isgood = False
    if ytid and client:
        print("Youtube ID:",ytid)
        if not mediafire_files:
            try:
                for item in client.get_folder_contents_iter("mf:/karaoke"):
                    if type(item) is File:
                        mediafire_files.append(item['filename'])
                        #print("File: {}".format(item['filename']))
            except Exception as e:
                pass


        if mediafire_files:
            if ytid in mediafire_files:
                print("File Found, Getting DL Url.")
                try:
                    dl_url = client.get_file_dl_url("mf:/karaoke/"+ytid)
                    if dl_url:
                        isgood = True
                except Exception as e:
                    pass
            else:
                print("File Not Found")

    if isgood:
        return Response(dl_url, status=201, mimetype="text/plain")
    else:
        return Response("Error Getting Url.", status=404, mimetype="text/plain")

    #print(ytid)
    #return Response("Hello World!", status=201, mimetype="text/plain")
    #return "Hello World!"

#if __name__ == '__main__':
#    app.run(debug=True)
