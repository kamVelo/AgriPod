from flask import Flask, render_template,redirect,request, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "asdjfosjdofjoijfo"

db = SQLAlchemy(app)
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
class data(db.Model):
    """
    data table
    """

    # table name
    __tablename__ = "data"

    # Columns
    id = db.Column("record_no", db.Integer, primary_key=True)
    uuid = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    network_id = db.Column(db.Integer,db.ForeignKey("networks.network_id"))
    device_id = db.Column(db.Integer,db.ForeignKey("devices.device_id"))
    moisture = db.Column("moisture", db.Integer)
    humidity = db.Column("humidity", db.Float)
    temperature = db.Column("temperature", db.Float)
    pH = db.Column("pH", db.Float)

    # constructor
    def __init__(self, owner_id:int, network_id:int, device_id:int, moisture:int, humidity:int, temperature:int, pH:int):
        self.uuid = owner_id
        self.network_id = network_id
        self.device_id = device_id
        self.moisture = moisture
        self.humidity = humidity
        self.temperature = temperature
        self.pH = pH

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
    """
    return "wassup dargie"
@app.errorhandler(403)
def forbidden():
    return "Wrong Network Name/Password/ID", 403

@app.errorhandler(500)
def badData():
    return "data was invalid", 500
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
    if "test" in request.form.keys() and request.form["test"] == "True": # for testing
        return request.form["data"]
    else:
        uuid = request.form["uuid"]
        name = request.form["n_name"]
        password = request.form["n_password"]
        device_id = request.form["device_id"]
        n_id = request.form["network_id"]
        # verification of input:
        acq_uuid = networks.query.with_entities(networks.owner_id).filter(networks.network_name == name, networks.network_password == password, networks.id == n_id).all()
        if acq_uuid == None:  # this implies no record was find so the network information provided is false
            abort(403)  # forbidden error
        acq_uuid = acq_uuid[0][0]  # gets the individual id
        if acq_uuid != int(uuid):  # i.e verification failed
            abort(403)  # forbidden error
        else:
            successful = saveData(uuid, n_id, device_id,request.form["moisture"], request.form["humidity"], request.form["temperature"], request.form["pH"])
            if not successful:
                abort(500)  # internal server error problem with saving data
        return "data accepted"
def saveData(uuid:str, network_id:str, device_id:str, moisture:str, humidity:str, temperature:str,pH:str) -> bool:
    """
    this function saves the data provided above into the sql data table
    :return: True/False for successful or not
    """

    uuid = int(uuid)
    network_id = int(network_id)
    device_id = int(device_id)
    moisture = int(moisture)
    humidity = float(humidity)
    temperature = float(temperature)
    pH = float(pH)

    if humidity > 1 or humidity < 0 or pH > 14 or pH < 0:
        return False
    datum = data(uuid, network_id, device_id, moisture, humidity,temperature, pH)
    db.session.add(datum)
    db.session.commit()
    datas = data.query.all()
    for datum in datas:
        print(datum.id)
        print(datum.humidity)
    return True
def processData():
    """
    this function processes the data
    :return: Something
    """

    # do something
    return "poo" # placeholder value
if __name__ == '__main__':
    app.run(port=5000,debug=True)