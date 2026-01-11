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

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('recipes.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Both username and password are required!', 'error')
            return render_template('login.html')
        
        connection = db_connection()
        try:
            user = connection.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

            if user and verify(user['hashed_password'], password):
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                flash(f'You are now logged in {user['username']}', 'success')
                
                return redirect(url_for('recipes.index'))
            else:
                flash('Username or password are invalid!', 'error')
        
        except Exception as e:
            flash(f'Login error: {str(e)}', 'error')
        finally:
            connection.close()

    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You\'re successfully logged out', 'success')

    return redirect(url_for('recipes.index'))