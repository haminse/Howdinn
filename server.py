from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


# to debug in local
app.run(debug = True, port = 5004)

# to deploy
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)