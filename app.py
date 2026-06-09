from flask import Flask, render_template, request
from models import db
from models import User
from forms import RegisterForm, LoginForm
import os
from analyzer import extract_text, detect_skills, suggest_career, calculate_score

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        user = User(

            username=form.username.data,

            email=form.email.data,

            password=form.password.data
        )

        db.session.add(user)

        db.session.commit()

        return "User Registered Successfully"

    return render_template(

        'register.html',

        form=form
    )
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(

            email=form.email.data,

            password=form.password.data

        ).first()

        if user:

            return "Login Successful"

        else:

            return "Invalid Email or Password"

    return render_template(

        'login.html',

        form=form
    )

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        file = request.files['resume']

        filepath = os.path.join('uploads', file.filename)

        file.save(filepath)

        text = extract_text(filepath)

        skills = detect_skills(text)

        career, missing = suggest_career(skills)

        score = calculate_score(skills)

        return render_template(

            'result.html',

            skills=skills,

            career=career,

            missing=missing,

            score=score
        )

    return render_template('dashboard.html')
with app.app_context():

    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)