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

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/query/<string:licenseNumber>')
def query(licenseNumber):
    licenseOwner=base.classes.LicenseOwner
    data = session.query(licenseOwner).filter(licenseOwner.license == int(licenseNumber)).first()
    return {'number':data.number,'class':data.majorAndClass,'name':data.name,'phone':data.phone}
