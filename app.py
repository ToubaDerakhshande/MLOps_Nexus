from flask import Flask
from flask import render_template,request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_required
import secrets



app = Flask(__name__)

# app configs
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite://users.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),nullable=False,unique=True)
    password = db.Column(db.String(150),nullable=False)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf_8')

        new_user = User(username = username,password = hashed_pass)
        db.session.add(new_user)
        db.session.commit()

        flash('Registeration was successful, please log in.','success')
        return redirect(url_for('login'))
    

    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and password.check_password_hash(user.password,password):
            session['username'] = user.username
            flash('Log in succesful!','success')
            return redirect(url_for('input'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('username')
    flash('You have been logged out!','info')
    return redirect(url_for('login'))

@app.route("/input",methods =['POST','GET'])
@login_required
def input():
    return render_template('input.html')

@app.route('/result')
def result():
    return render_template('result.html')





if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)