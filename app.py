from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets
from model import load_model, predict  

app = Flask(__name__)


model = load_model()

#app configs
app.config['SECRET_KEY'] = secrets.token_hex(16)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():    
    return render_template('login.html')

@app.route('/logout')
def logout():
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
    app.run(debug=True)
