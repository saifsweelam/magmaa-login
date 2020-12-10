from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request,
    flash,
    get_flashed_messages,
    jsonify
)
from models import bind_database, User
import config

app = Flask(__name__)
app.config.from_object('config')
bind_database(app)


@app.route('/')
def index():
    if 'profile' not in session:
        return render_template('landing.html')
    return render_template('details.html')


@app.route('/login', methods=['GET'])
def get_login_form():
    if 'profile' in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def get_register_form():
    if 'profile' in session:
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    if 'profile' in session:
        return redirect(url_for('index'))

    email = request.form.get('email')
    password = request.form.get('password')

    if not (email and password):
        flash('The data you entered are missing or invalid.')
        return redirect(url_for('get_login_form'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('The Email Address you entered is invalid.')
        return redirect(url_for('get_login_form'))

    if not user.verify_password(password):
        flash('Either the Email Address or the Password is incorrect.')
        return redirect(url_for('get_login_form'))

    session['profile'] = {
        'name': user.name,
        'email': user.email,
        'phone': user.phone
    }
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def add_user():
    if 'profile' in session:
        return redirect(url_for('index'))

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    phone = request.form.get('phone')

    if not (name and email and password and confirm_password):
        flash('The data you entered are missing or invalid.')
        return redirect(url_for('get_register_form'))

    if password != confirm_password:
        flash('The two passwords mismatch.')
        return redirect(url_for('get_register_form'))
    
    user = User(
        name=name,
        email=email,
        phone=phone
    )
    user.hash_password(password)
    user.insert()

    session['profile'] = {
        'name': user.name,
        'email': user.email,
        'phone': user.phone
    }
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
