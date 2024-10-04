from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets

app = Flask(__name__)

#app configs
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),nullable=False,unique=True)
    password = db.Column(db.String(150),nullable=False)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            session['username'] = user.username
            flash('Log in succesful!','success')
            return redirect(url_for('input_data'))
        # else:
        #      flash('You must register!','danger') 
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    flash('You have been logged out!','info')
    return redirect(url_for('login'))

@app.route('/input' , methods=['GET', 'POST'])
def input_data():
    return render_template('input.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)