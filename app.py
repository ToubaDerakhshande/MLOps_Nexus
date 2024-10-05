from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from form import CancerDataForm
from datetime import datetime
from models import predict  
import secrets

app = Flask(__name__)

# Configuring app
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cancer_recognition.db'

# Initialize the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define User Model for user tracking
class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),nullable=False,unique=True)
    password = db.Column(db.String(150),nullable=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

# Define Prediction Model for storing inputs and results
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Store each feature input separately
    mean_radius = db.Column(db.Float, nullable=False)
    mean_perimeter = db.Column(db.Float, nullable=False)
    mean_area = db.Column(db.Float, nullable=False)
    mean_concavity = db.Column(db.Float, nullable=False)
    mean_concave_points = db.Column(db.Float, nullable=False)
    worst_radius = db.Column(db.Float, nullable=False)
    worst_perimeter = db.Column(db.Float, nullable=False)
    worst_area = db.Column(db.Float, nullable=False)
    worst_concavity = db.Column(db.Float, nullable=False)
    worst_concave_points = db.Column(db.Float, nullable=False)
    
    # Store the result 
    result = db.Column(db.String(50), nullable=False)
    
    # Timestamp (when the prediction was made)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    # Link prediction to the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
# login_required method
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
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
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/input' , methods=['GET', 'POST'])
@login_required
def input_data():
    form = CancerDataForm()
    if form.validate_on_submit():
        features = {
            'mean radius': form.mean_radius.data,
            'mean perimeter': form.mean_perimeter.data,
            'mean area': form.mean_area.data,
            'mean concavity': form.mean_concavity.data,
            'mean concave points': form.mean_concave_points.data,
            'worst radius': form.worst_radius.data,
            'worst perimeter': form.worst_perimeter.data,
            'worst area': form.worst_area.data,
            'worst concavity': form.worst_concavity.data,
            'worst concave points': form.worst_concave_points.data
        }

        prediction = predict(features)
        result = 'Malignant' if prediction == 1 else 'Benign'
        
        # Save the prediction to the database
        if 'user_id' in session:
            new_prediction = Prediction(
                mean_radius=features['mean radius'],
                mean_perimeter=features['mean perimeter'],
                mean_area=features['mean area'],
                mean_concavity=features['mean concavity'],
                mean_concave_points=features['mean concave points'],
                worst_radius=features['worst radius'],
                worst_perimeter=features['worst perimeter'],
                worst_area=features['worst area'],
                worst_concavity=features['worst concavity'],
                worst_concave_points=features['worst concave points'],
                result=result,
                user_id= session['user_id']
            )
        
            db.session.add(new_prediction)
            db.session.commit()
            
        # Store the result in the session
        session['result'] = result

        return redirect(url_for('result'))
        
    return render_template('input.html', form= form)

@app.route('/result')
@login_required
def result():
    result = session.get('result')  # Get result from query parameter
    if result is None:
        # Handle case where result is not provided, redirect back to input or an error page
        flash('No result available. Please input the data first.', 'warning')
        return redirect(url_for('input_data'))
    return render_template('result.html', result= result)

@app.route('/history')
@login_required
def history():
    # Fetch the predictions made by the current user
    predictions = Prediction.query.filter_by(user_id=session['user_id']).order_by(Prediction.date_created.desc()).all()
    # Pass the predictions to the history template
    return render_template('history.html', predictions=predictions, username= session['username'])

if __name__ == '__main__':
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)