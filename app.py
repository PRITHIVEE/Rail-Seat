from flask import Flask,request,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import sshtunnel

app=Flask(__name__)
app.config['DEBUG']=True
app.secret_key=b'h87lubd878hiash'

tunnel= sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),ssh_username='BuvanPrithivee', ssh_password='8uvan-9R!+#1v33',
    remote_bind_address=('BuvanPrithivee.mysql.pythonanywhere-services.com',3306)
)
tunnel.start()

#app.config['SQLALCHEMY_DATABASE_URI']='mysql://BuvanPrithivee:RailSeat@127.0.0.1:{}/BuvanPrithivee$RailSeat'.format(tunnel.local_bind_port)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///RailSeat.db'
db=SQLAlchemy(app)

class SelfUsage():
    pass

class PersonalDetails(db.Model):
    __tablename__="personalDetails"
    ID = db.Column(db.Integer,primary_key=True)
    userName = db.Column(db.String(30))
    email = db.Column(db.String(30))
    dob = db.Column(db.String(10))
    gender = db.Column(db.String(7))
    password = db.Column(db.String(30))
    def __repr__(self):
        return "PersonalDetails<{},{}>".format(self.ID,self.userName)


@app.route('/',methods=['GET','POST'])
@app.route('/index')
def index():
    if request.method == 'POST':
        SelfUsage.createAcc={}
        SelfUsage.createAcc['userName']=request.form['userName']
        SelfUsage.createAcc['email']=request.form['SEmail']
        SelfUsage.createAcc['dob']=request.form['dob']
        SelfUsage.createAcc['gender']=request.form['gender']
        SelfUsage.createAcc['password']=request.form['SPassword']
        if PersonalDetails.query.filter_by(email=SelfUsage.createAcc['email']).all():
            flash('Account Already registered')
            flash(SelfUsage.createAcc['email'])
            redirect('/')
        SelfUsage.newAcc = PersonalDetails(userName=SelfUsage.createAcc['userName'],email=SelfUsage.createAcc['email'],dob=SelfUsage.createAcc['dob'],gender=SelfUsage.createAcc['gender'],password=SelfUsage.createAcc['password'])
        db.session.add(SelfUsage.newAcc)
        db.session.commit()
    return render_template('index.html')

@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        try:
            SelfUsage.currUserMail=request.form['LEmail']
            SelfUsage.currUserPassword=request.form['LPassword']
        
            SelfUsage.currUser=db.session.query(PersonalDetails).filter_by(email=SelfUsage.currUserMail).first()
            if(SelfUsage.currUser.password == SelfUsage.currUserPassword):
                SelfUsage.currUserName=SelfUsage.currUser.userName
            else:
                flash('Incorrect Password')
                flash(SelfUsage.currUserMail)
                return redirect('/')
        except:
            flash('Account Not registered')
            return redirect('/')
    return render_template('home.html',userName=SelfUsage.currUserName)

@app.route('/trainResults')
def trainResults():
    allTrains=[{}]
    allTrains[0]['trainName']='Coimbatore Express'
    allTrains[0]['trainID']=1244
    allTrains[0]['fromStation']='Coimbatore'
    allTrains[0]['toStation']='Chennai'
    return render_template('trainResults.html',allTrains=allTrains)

@app.route('/seatSelect')
def seatSelect():
    train={}
    train['trainName']='Coimbatore Express'
    train['trainID']='12345'
    return render_template('seatSelect.html',train=train,userName=SelfUsage.currUserName)

@app.route('/ticket')
def ticket():
    return render_template('ticket.html',userName=SelfUsage.currUserName)

@app.route('/profile',methods=['POST','GET'])
def profile():
    user={}
    try:
        user['userName']=request.form["userName"]
        db.session.query(PersonalDetails).filter_by(ID=SelfUsage.currUser.ID).update({PersonalDetails.userName:user['userName']})
        db.session.commit()
    except:
        user['userName']=SelfUsage.currUser.userName
    try:
        user['email']=request.form['email']
        db.session.query(PersonalDetails).filter_by(ID=SelfUsage.currUser.ID).update({PersonalDetails.email:user['email']})
        db.session.commit()
    except:
        user['email'] = SelfUsage.currUser.email
    try:
        user['dob'] =request.form['dob']
        db.session.query(PersonalDetails).filter_by(ID=SelfUsage.currUser.ID).update({PersonalDetails.dob:user['dob']})
        db.session.commit()
    except:
        user['dob'] = SelfUsage.currUser.dob
    try:
        user['gender'] = request.form['gender']
        db.session.query(PersonalDetails).filter_by(ID=SelfUsage.currUser.ID).update({PersonalDetails.gender:user['gender']})
        db.session.commit()
    except:
        user['gender'] = SelfUsage.currUser.gender
    try:
        user['password']= request.form['password']
        db.session.query(PersonalDetails).filter_by(ID=SelfUsage.currUser.ID).update({PersonalDetails.password:user['password']})
        db.session.commit()
    except:
        user['password']=SelfUsage.currUser.password
    return render_template('profile.html',user=user)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=6006)
