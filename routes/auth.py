from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from helpers import db_connection, verify
from werkzeug.security import generate_password_hash


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not email or not password:
            flash('All fields required!', 'error')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        
        if len(password) < 8:
            flash('At least 8 characters needed for password!', 'error')
            return render_template('signup.html')
        
        connection = db_connection()
        try:
            exists = connection.execute('SELECT user_id FROM user WHERE username = ? OR email = ?', (username, email)).fetchone()

            if exists:
                flash('User with Username or email already exists!', 'error')
                return render_template('signup.html')
            
            hashed_password =  generate_password_hash(password)
            connection.execute('''INSERT INTO user (username, email, hashed_password, type)
                                VALUES (?, ?, ?, ?)''', (username, email, hashed_password, 'user'))
            
            connection.commit()
            flash('Signup Successful! You can now log in!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Signup error: {str(e)}', 'error')
        finally:
            connection.close()

    return render_template('signup.html')