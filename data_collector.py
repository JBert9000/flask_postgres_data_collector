from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func
# from sqlalchemy import exc
# from sqlalchemy.exc import IntegrityError
# import psycopg2

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zeta_g:postgres123@localhost/height_collector'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer,primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]

        data=Data(email,height)
        if db.session.query(Data).filter(Data.email_==email).count==0:
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            # try:
            #     db.session.commit()
            # except IntegrityError:
            #     db.session.rollback()
            return render_template("success.html")
    return render_template('index.html',text="Looks like this email was already used.")


if __name__ == '__main__':
    app.debug=True
    app.run() #default is always port:5000
