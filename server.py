from flask import Flask, render_template, request, redirect,jsonify,session,url_for
from flask_cors import CORS
import gpt4_api
from firebase import firebase
import firebase_admin
from firebase_admin import credentials,firestore

import os
import json
import pyrebase

import asyncio
import cv2
import numpy as np
import time
from hume import HumeStreamClient, StreamSocket
from hume.models.config import FaceConfig
from typing import Any, Dict, List



cred = credentials.Certificate("howdinn-firebase-adminsdk-bzquq-90df7b7751.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://howdinn.firebaseio.com' 
})
pb = pyrebase.initialize_app(json.load(open(("fbConfig.json"))))
db = firestore.client()
useref = db.collection("users")
auth = pb.auth()


app = Flask(__name__)
app.secret_key = "abc123"
CORS(app)

final_emotion = {"Sympathy" : 0, "Surprise (positive)" : 0, "Sadness" : 0, "Romance" : 0, "Pride" : 0, "Pain" : 0, "Nostalgia" : 0, "Love" : 0, "Joy" : 0, "Horror" : 0, "Fear" : 0, "Excitement" : 0, "Doubt" : 0, "Disgust" : 0, "Determination" : 0, "Contentment" : 0, "Confusion" : 0, "Boredom" : 0, "Awe" : 0, "Anger" : 0, "Amusement" : 0, "Adoration" : 0}
final_statement = ""
camera = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
global t
t = 0

gpt4_api.setup_gpt4()
@app.route("/", methods = ['GET', 'POST'])
def index():

    interaction = False
    if ( "user" not in session ):
        redirect(url_for('login'))
    entry =gpt4_api.get_entry_question()  
    return render_template('index.html', entry = entry)

@app.route("/signup",  methods=['GET','POST'])
def signup():
    if ( request.method == "POST" ):
        print("post")
        email=request.form['email']   #get the email from json
        password=request.form['password'] #get the password from json
        try:
            useref.document().set(request.form)
            return jsonify({'message': f'Successfully created user and send verification link please activate your account '}),200
        except Exception as e:
            print(e.args)
            return "error"
    return render_template("form.html",signup={True})


@app.route("/login",methods=['GET','POST'])
def login():
    if ( "user" in session ):
       redirect(url_for("/"))
    if ( request.method == "POST" ):
        print("post")
        email=request.form['gemail']   #get the email from json
        password=request.form['password'] #get the password from json
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session["user"] = email
        except Exception as e:
            print(e.args)
            return "failed to login"
    return render_template("login.html",signup={False}) 

@app.route("/start_interaction", methods=['GET', 'POST'])
def start_interaction():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Start Recording') == 'Start Recording':
            session["interacting"] = True
    if session["interacting"] == True:
        # instruction
        out = cv2.VideoWriter('output.avi', fourcc, 30, (640,  480))

        def gen_frames():
            t_end = time.time() + 5
            while time.time() < t_end:
                ret, frame = camera.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                #frame = cv2.flip(frame, 0)
                # write the flipped frame
                out.write(frame)
                #cv2.imshow('frame', frame)
            out.release()
        
        async def main():
            client = HumeStreamClient("3yfgKQI2BO49t8Mr8oSg2qnv0QPTAvdH1xBBluugSk5JeWdG")
            config = FaceConfig(identify_faces=True)
            gen_frames()
            async with client.connect([config]) as socket:
                result = await socket.send_file("output.avi")
                #print(result)
                n = 0
                while n < 10:
                    emotions = result["face"]["predictions"][n]["emotions"]
                    print_emotions(emotions)
                    n += 1
            

        def print_emotions(emotions: List[Dict[str, Any]]) -> None:
            emotion_map = {e["name"]: e["score"] for e in emotions}
            for emotion in ["Sympathy", "Surprise (positive)", "Sadness", "Romance", "Pride", "Pain", "Nostalgia", "Love", "Joy", "Horror", "Fear", "Excitement", "Doubt", "Disgust", "Determination", "Contentment", "Confusion", "Boredom", "Awe", "Anger", "Amusement", "Adoration"]:
                final_emotion[emotion] += emotion_map[emotion]
                #print(f"- {emotion}: {final_emotion[emotion]:4f}")

        while True:
                global t
                asyncio.run(main())
                t += 1
                print(t)
        
final_list = []
@app.route("/end_interaction", methods=['GET', 'POST'])
def end_interaction():
    global t
    if request.form.get('Stop Recording') == 'Stop Recording':

        if t > 0:
            final_emotion_sorted = dict(sorted(final_emotion.items(), key=lambda x:x[1], reverse=True))
            no = 0
           
            for emotion in final_emotion_sorted.keys():
                if no < 5: 
                    final_list.append({"emotion" : emotion, 
                                    "percentage" : int(final_emotion_sorted[emotion] /(t*14)*100)})
                    no += 1
                print(final_list)
                camera.release()
                cv2.destroyAllWindows()
        session["interacting"] = False
        redirect(url_for("results"))
        with open("chart_data(example).json", "w") as outfile:
        outfile.write(json.dumps(final_list))
        return json.dumps(final_list)
    



# @app.route("/therapy")
# # record video and send data to firebase // hume api 


# @app.route("/fetchScore")
# #???

# # Outputs


@app.route("/results")
def results():
    return "nothing"
# #get recommendations based on the final score
# #General advice through open ai api and getting in movie recommendation etc.



# to debug in local
app.run(debug = True, port = 5004, threaded=True)

# to deploy
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)