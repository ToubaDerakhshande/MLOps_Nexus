# Team_MLOps
# Smart Website Project
A web-based application built with Python's Flask framework for cancer recognition. 
This project provides user registration, input, prediction results, and history tracking functionalities with a structured and modular design.
It offers a clean, responsive UI with an intuitive experience.

## Team Member 1
### Task Title: Setup Flask Application and Create Home Page
	- Set up the Flask project structure (app.py, templates, static folders).
	- Create a home page (/) that introduces the application and provides navigation links to the login, registration, and input pages.
	- Ensure proper routing and basic structure of the Flask application.
#### Follow the steps below to perform the project:
#### Installation
Follow these steps to set up the project:
1. Clone the repository:
```
git clone <repository-url>
```
2. Navigate to the project directory:
```
cd smart_website_project
```
3. Set up a virtual environment:
```
python3 -m venv venv
```
4. Activate the virtual environment:
```
source venv/bin/activate
```
5. Install the required packages:
```
pip install -r requirements.txt
```
#### Project Structure
```
smart_website_project/
│
├── app.py  # Main Flask application
├── models.py  # Models for cancer recognition
├──form.py 
├── templates/  # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── input.html
│   ├── result.html
│   ├── history.html
├── static/  # Static files (CSS, JS, images, etc.)
│   ├── css/
│   └── images/
├── venv/  # Virtual environment
└── requirements.txt  # Project dependencies
```
Follow these steps to create above structure:
```
1. touch app.py
2. mkdir templates
3. touch templates/base.html
4. touch templates/home.html
5. touch templates/input.html
6. touch templates/login.html
7. touch templates/register.html
8. touch templates/dashboard.html
9. touch templates/result.html
10. touch templates/history.html
11. mkdir static
12. mkdir static/css
13. mkdir static/images
14. touch models.py
15. touch form.py
```
