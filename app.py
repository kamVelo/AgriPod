from flask import Flask, render_template,redirect,request, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "asdjfosjdofjoijfo"

db = SQLAlchemy(app)
class users(db.Model):
    id = db.column("user_id", db.Integer, primary_key=True)
    fName = db.column("f_name", db.String(100))
    lName = db.column("l_name", db.String(100))
    networkName = db.column("NName", db.String(100)) # name of agripod network
    networkPassword = db.column("NPassword", db.string(100)) # password of agripod network
    numDevices = db.column("num_devices", db.Integer)

    devices = db.relationship("devices", backref="owner_id", lazy=True)
    devices = db.relationship("networks", backref="owner_id", lazy=True)

class networks(db.Model):
    id = db.column("network_id", db.Integer, primary_key=True)
    owner_id = db.column(db.Integer,db.ForeignKey("users.user_id"))
    numDevices = db.column()

class devices(db.Model):
    id = db.column("device_id", db.Integer, primary_key=True)
    owner_id = db.column(db.Integer, db.ForeignKey("users.user_id"))
    network_name = db.column
@app.route("/index/")
@app.route("/")
def index():
    return "wassup dargie"

@app.route("/inputData/", methods=["POST"])
def inputData():
    """
    this takes in data from post request, saves it and processes it and returns the output to the device
    data:
    - humidity
    - temperature
    - pH
    - soil moisture
    :return: output of processing
    """
    if request.form["test"] == "True": # for testing
        return request.form["data"]
    else:

        return processData(request.form["data"])

def processData():
    """
    this function processes the data
    :return: Something
    """

    # do something
    return "poo" # placeholder value
if __name__ == '__main__':
    app.run(port=5000,debug=True)