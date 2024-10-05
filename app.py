from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets

from models import  predict  

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

# login_required method
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.name = f.name
    return wrap

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # If username does not exist, proceed with registration
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf_8')
        new_user = User(username=username, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration was successful, please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user:
            if bcrypt.check_password_hash(user.password, password):
                # If password is correct
                session['username'] = user.username
                session['user_id'] = user.id
                flash('Log in successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                # If password is incorrect
                flash('Incorrect password. Please try again.', 'warning')
        else:
            # If the user does not exist
            flash('Username not found. Please register first.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    flash('You have been logged out!','info')
    return redirect(url_for('login'))

@app.route('/input' , methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        # Retrieve data from the form
        features = {
            'mean radius': float(request.form['mean_radius']),
            'mean perimeter': float(request.form['mean_perimeter']),
            'mean area': float(request.form['mean_area']),
            'mean concavity': float(request.form['mean_concavity']),
            'mean concave points': float(request.form['mean_concave_points']),
            'worst radius': float(request.form['worst_radius']),
            'worst perimeter': float(request.form['worst_perimeter']),
            'worst area': float(request.form['worst_area']),
            'worst concavity': float(request.form['worst_concavity']),
            'worst concave points': float(request.form['worst_concave_points'])
        }
    
        # Make a prediction using the predict function 
        prediction = predict(features)
        # Interpret the result
        result = 'Malignant' if prediction == 1 else 'Benign'
        # Redirect to the result page with the prediction
        return render_template('result.html', prediction=result)

    return render_template('input.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(debug=True)

 
    


