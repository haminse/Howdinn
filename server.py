from flask import Flask, render_template, request, redirect
import gpt4_api

app = Flask(__name__)
gpt4_api.setup_gpt4()
@app.route("/", methods = ['GET', 'POST'])
def index():
    entry =gpt4_api.get_entry_question()
    return render_template('index.html', entry = entry)


# to debug in local
app.run(debug = True, port = 5004)

# to deploy
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)