from flask import Flask, render_template, request, redirect,jsonify,session
from flask_cors import CORS
import gpt4_api
from firebase import firebase
import firebase_admin
from firebase_admin import credentials,firestore
from dotenv import load_dotenv
import os
import json
import pyrebase
load_dotenv()

cred = credentials.Certificate(os.getenv("CREDENTIALS_LOCATION"))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://howdinn.firebaseio.com' 
})
pb = pyrebase.initialize_app(json.load(open(("fbConfig.json"))))
db = firestore.client()
useref = db.collection("users")
auth = pb.auth()


app = Flask(__name__)
CORS(app)



gpt4_api.setup_gpt4()
@app.route("/", methods = ['GET', 'POST'])
def index():
    entry =gpt4_api.get_entry_question()
    return render_template('index.html', entry = entry)


# @app.route("/login")
# #compare data to firebase and serve pages accordingly

@app.route("/signup",  methods=['GET','POST'])
def signup():
    if ( request.method == "POST" ):
        print("post")
        email=request.form['email']   #get the email from json
        password=request.form['password'] #get the password from json
        if email is None or password is None:
            return "error1"
        try:
            useref.document().set(request.form)
            # user = auth.create_user_with_email_and_password(
            #     email=email,
            #     password=password
            # )
            # session["user"] = email
            return jsonify({'message': f'Successfully created user and send verification link please activate your account '}),200
        except Exception as e:
            print(e.args)
            return "error"
    return render_template("form.html",signup={True})



@app.route("/result", methods = ['GET', 'POST']) #change th the only POST later
def result():
    #humm code here  : return json file
    chart_data = gpt4_api.read_json("chart_data(example).json")
    return render_template("result.html", chart_data = chart_data)



# @app.route("/therapy")
# # record video and send data to firebase // hume api 


# @app.route("/fetchScore")
# #???

# # Outputs


# @app.route("/recommendations")
# #get recommendations based on the final score
# #General advice through open ai api and getting in movie recommendation etc.



# to debug in local
app.run(debug = True, port = 5004)

# to deploy
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)