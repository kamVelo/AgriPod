from flask import Flask, render_template,redirect,request, session, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from twilio.twiml.messaging_response import MessagingResponse
import ast
from dataclasses import dataclass
import os
import json
import html
from datetime import datetime
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "asdjfosjdofjoijfo"

db = SQLAlchemy(app)

#TODO: time-index data
@dataclass
class users(db.Model):
    """
    user data table
    """
    # table name
    __tablename__ = "users"
    # Columns
    id = db.Column("user_id", db.Integer, primary_key=True)
    f_name = db.Column("f_name", db.String(100))
    l_name = db.Column("l_name", db.String(100))
    username = db.Column("username", db.String(100))
    password = db.Column("password", db.String(100))
    network_name = db.Column("n_name", db.String(100)) # name of agripod network
    num_devices = db.Column("num_devices", db.Integer)

    # Foreign key relationships
    devices = db.relationship("devices",  lazy=True)
    networks = db.relationship("networks",  lazy=True)
    data = db.relationship("data",  lazy=True)

    # constructor
    def __init__(self, f_name:str, l_name:str, username:str,password:str, network_name:str,num_devices:int):
        self.f_name = f_name
        self.l_name = l_name
        self.username = username
        self.password = password
        self.network_name = network_name
        self.num_devices = num_devices

@dataclass
class networks(db.Model):
    """
    networks table
    """

    # table name
    __tablename__ = "networks"

    # Columns
    id = db.Column("network_id", db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    network_name = db.Column("network_name", db.String(100))
    network_password = db.Column("network_password", db.String(100))
    num_devices = db.Column("num_devices", db.Integer)

    # Foreign key relationships
    devices = db.relationship("devices", lazy=True)
    data = db.relationship("data",  lazy=True)

    # constructor
    def __init__(self, owner_id:int, network_name:str, network_password:str, num_devices:int):
        self.owner_id = owner_id
        self.network_name = network_name
        self.network_password = network_password
        self.num_devices = num_devices

@dataclass
class devices(db.Model):
    """
    devices table
    """

    # table name
    __tablename__ = "devices"

    # Columns
    id = db.Column("device_id", db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    network_id = db.Column(db.Integer,db.ForeignKey("networks.network_id"))
    # need a location variable too

    # Foreign key relationships
    data = db.relationship("data", lazy=True)

    # constructor
    def __init__(self, owner_id:int, network_id:int):
        self.owner_id = owner_id
        self.network_id = network_id

@dataclass
class data(db.Model):
    """
    data table
    """
    id: int
    uuid: int
    network_id: int
    device_id: int
    moisture: float
    humidity: float
    temperature: float
    time: datetime
    # table name
    __tablename__ = "data"

    # Columns
    id = db.Column("record_no", db.Integer, primary_key=True)
    uuid = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    network_id = db.Column(db.Integer,db.ForeignKey("networks.network_id"))
    device_id = db.Column(db.Integer,db.ForeignKey("devices.device_id"))
    moisture = db.Column("moisture", db.Float)
    humidity = db.Column("humidity", db.Float)
    temperature = db.Column("temperature", db.Float)
    time = db.Column("time", db.DateTime)
    # constructor
    def __init__(self, owner_id:int, network_id:int, device_id:int, moisture:float, humidity:int, temperature:int, time=datetime):
        self.uuid = owner_id
        self.network_id = network_id
        self.device_id = device_id
        self.moisture = moisture
        self.humidity = humidity
        self.temperature = temperature
        self.time = time

db.create_all()

@app.route("/index/")
@app.route("/")
def index():
    """
    current test run data:
    fName = Simul
    lName = Test
    username = Abi
    password = Shek
    network name = fakeNetwork
    network password = I was agent orange that was me
    numDevices = 1
    owner id = 1
    network id = 1

    user =  users("Simul", "Test", "Abi", "Shek", "fakeNetwork", 1)
    db.session.add(user)
    db.session.commit()
    network = networks(1, "fakeNetwork", "I was agent orange that was me", 1)
    db.session.add(network)
    db.session.commit()
    device = devices(1, 1)
    db.session.add(device)
    db.session.commit()


    # database has com

    """
    imgs = ["/static/img/explodeReverseFrames/0 (%s).jpg" % n for n in range(1,49)]
    imgs = [html.unescape(img) for img in imgs]

    imgs = json.dumps(imgs)
    return render_template("index.html", imgs=imgs)
@app.errorhandler(403)
def forbidden(e):
    return "Wrong Network Name/Password/ID", 403

@app.errorhandler(500)
def badData(e):
    return "data was invalid", 500
@app.route("/inputData/", methods=["POST"])
def inputData():
    """
    this takes in data from post request, saves it and processes it and returns the output to the device
    data:
    - humidity
    - temperature
    - soil moisture
    :return: output of processing
    """
    if len(request.form) > 0:
        json_obj = request.form
    else:
        json_obj = ast.literal_eval(request.data.decode("utf-8"))
    if "test" in json_obj.keys() and json_obj["test"] == "True": # for testing
        return json_obj["data"]
    else:
        uuid = json_obj["uuid"]
        name = json_obj["n_name"]
        password = json_obj["n_password"]
        device_id = json_obj["device_id"]
        n_id = json_obj["network_id"]
        # verification of input:
        acq_uuid = networks.query.with_entities(networks.owner_id).filter(networks.network_name == name, networks.network_password == password, networks.id == n_id).all()
        if acq_uuid == None:  # this implies no record was find so the network information provided is false
            abort(403)  # forbidden error
        acq_uuid = acq_uuid[0][0]  # gets the individual id
        if acq_uuid != int(uuid):  # i.e verification failed
            abort(403)  # forbidden error
        else:
            successful = saveData(uuid, n_id, device_id,json_obj["moisture"], json_obj["humidity"], json_obj["temperature"])
            if not successful:
                abort(500)  # internal server error problem with saving data
        return "data accepted"
def saveData(uuid:str, network_id:str, device_id:str, moisture:str, humidity:str, temperature:str) -> bool:
    """
    this function saves the data provided above into the sql data table
    :return: True/False for successful or not
    """

    uuid = int(uuid)
    network_id = int(network_id)
    device_id = int(device_id)
    moisture = float(moisture)
    humidity = float(humidity)
    temperature = float(temperature)

    if humidity > 100 or humidity < 0:
        return False
    datum = data(uuid, network_id, device_id, moisture, humidity,temperature, datetime.now())
    db.session.add(datum)
    db.session.commit()
    return True
def processData():
    """
    this function processes the data
    :return: Something
    """

    # do something
    return "poo" # placeholder value
@app.route("/getLast/", methods=["POST"])
def getLatestRecord():
    if len(request.form) > 0:
        json_obj = request.form
    else:
        json_obj = ast.literal_eval(request.data.decode("utf-8"))
    uuid = json_obj["uuid"]
    datum = data.query.filter(data.uuid == uuid).all()[-1] # gets latest record
    resp = {
        "record id" : datum.id,
        "humidity" : datum.humidity,
        "moisture" : datum.moisture,
        "temperature" : datum.temperature
    }
    return resp

@app.route("/getAllData/", methods=["POST"])
def getAllData():
    if len(request.form) > 0:
        json_obj = request.form
    else:
        json_obj = ast.literal_eval(request.data.decode("utf-8"))
    uuid = json_obj["uuid"]
    acq_network_name = users.query.with_entities(users.network_name).filter(users.id == uuid).first()[0]
    network_name = json_obj["network name"]
    network_password = json_obj["network password"]
    if acq_network_name is not None:
        if network_name == acq_network_name:
            acq_network_password = networks.query.with_entities(networks.network_password).filter(network_name == network_name).first()[0]
            if acq_network_password == network_password:
                downloadable = data.query.filter(data.uuid == uuid).all()
                return jsonify(downloadable)
            else:
                abort(403)
        else:
            abort(403)

@app.route("/smsIn/", methods=["GET", "POST"])
def receiveSMS():
    resp = MessagingResponse()
    body = request.values.get("Body", None)
    body = body.lower().strip()
    varReq = body.split(" ")[-1]
    if "?" in varReq:
        varReq = varReq[:-1]

    datum = data.query.filter(data.uuid == 1).all()[-1]  # gets latest record
    content = {
        "record id": datum.id,
        "humidity": datum.humidity,
        "moisture": datum.moisture,
        "temperature": datum.temperature
    }
    units = {
        "humidity" : "%",
        "temperature" : " Degrees Celsius"
    }
    var = str(round(content[varReq]) + units[varReq])
    resp.message(var)

    return str(resp)



if __name__ == '__main__':
    app.run(port=5000,debug=True)