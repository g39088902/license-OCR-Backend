#Time
import time
def curTime():
    return time.asctime(time.localtime(time.time()))+"  "

#SQL
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.automap import automap_base
try:
    print(curTime()+"开始连接SQL，请稍等")
    engine = create_engine("postgresql://postgres:MeiYouMiMa!@infiiinity.xyz:5432/license",echo=False)
    base = automap_base()
    base.prepare(engine, reflect=True)

    print(curTime()+"开始打印Table")
    for theClass in base.classes:
        print(theClass)

    
except Exception as err:
    print(curTime()+str(err)+"数据库连不上了")

#SQL session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#Json
def ownerToJson(self):
    return {
            'number': self.number,
            'majorAndClass': self.majorAndClass,
            'name': self.name,
            'phone': self.phone,
            'license': self.license
            }

def violationToJson(self):
    return {
            'violationNumber': self.violationNumber,
            'license': self.license,
            'date': 
            str(self.date.year)+"-"+
            str(self.date.month)+"-"+
            str(self.date.day),
            'detail': self.detail
            }

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/query/<string:licenseNumber>')
def query(licenseNumber):
    licenseOwner=base.classes.LicenseOwner
    data = session.query(licenseOwner).filter(licenseOwner.license == int(licenseNumber)).first()
    return ownerToJson(data)

@app.route('/queryViolation/<string:licenseNumber>')
def queryViolation(licenseNumber):
    violation=base.classes.Violation
    datas = session.query(violation).filter(violation.license == int(licenseNumber)).all()
    temp = []
    for data in datas:
        temp.append(violationToJson(data))
    return jsonify(objects = temp),200,{"ContentType":"application/json"}

@app.route('/addViolation/<string:licenseNumber>', methods=["POST"])
def addViolation(licenseNumber):
    #TODO: 加密码鉴权
    violation=base.classes.Violation
    session.add(violation(license=int(licenseNumber),detail=request.form["detail"]))
    session.commit()
    return "succeed"