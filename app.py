from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import SQLAlchemyError
from models import db, UpdateDetails, User
from forms import StudentData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'projo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jo12hn34@localhost/project'
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        regno = request.form.get('regno')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'danger')
        else:
            # hashed_password = generate_password_hash(password, method="sha256")
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(email=email, name=name, regno=regno, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# student data
@app.route('/', methods=['GET', 'POST'])
def add_student():
    form = StudentData()
    if form.validate_on_submit():
        new_student = UpdateDetails(
            work=form.work.data,
            week=form.week.data,
            day=form.day.data,
            date=form.date.data
        )

        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully', 'success')
        return redirect(url_for('index'))

    students = UpdateDetails.query.all()
    return render_template('add_student.html', form=form, students=students)


# update the existing user
# Update function
@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = UpdateDetails.query.get_or_404(student_id)
    form = StudentData(obj=student)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash('Student updated successfully', 'success')
        return redirect(url_for('add_student'))

    return render_template('update_student.html', form=form)

# viewing the data student enters
# @app.route('/', methods=['GET', 'POST'])
@app.route('/view')
def view():
    students = UpdateDetails.query.all()
    return render_template('view.html', students=students)

# delete a student
@app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    try:
        student = UpdateDetails.query.get_or_404(student_id)
        # student = UpdateDetails.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect(url_for('view'))
        
        else:
            return f"Details with id {student_id} not found."
    except SQLAlchemyError as e:
        db.session.rollback()
        # return f"Error deleting student: {str(e)}"
    return render_template('view.html')
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)