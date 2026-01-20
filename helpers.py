from flask import session
from werkzeug.security import check_password_hash
import sqlite3

def db_connection():
    connection = sqlite3.connect('database/recipes.db')
    connection.row_factory = sqlite3.Row
    return connection

def rating_average(recipe_id):

    connection = db_connection()
    result = connection.execute('''
        SELECT AVG(value) as rating_ave, COUNT(*) as rating_count
        FROM rating
        WHERE recipe_id = ?    
                                ''', (recipe_id,)).fetchone()
    connection.close()

    if result['rating_ave']:
        return round(result['rating_ave'], 1), result['rating_count']
    return 0, 0

def add_ratings(recipes):
    recipes_and_ratings = []
    for r in recipes:
        rating_ave, rating_count = rating_average(r['recipe_id'])
        r_dict = dict(r)
        r_dict['rating_ave'] = rating_ave
        r_dict['rating_count'] = rating_count
        recipes_and_ratings.append(r_dict)

    return recipes_and_ratings

def current_user():
    if 'user_id' in session:
        connection = db_connection()
        user = connection.execute('SELECT * FROM user WHERE user_id = ?', (session['user_id'],)).fetchone()
        connection.close()
        return user
    return None


def is_owner(recipe_id):
    curr_user = current_user()
    if not curr_user:
        return False
    
    connection = db_connection()
    try:
        recipe = connection.execute('SELECT user_id FROM recipe WHERE recipe_id=?', (recipe_id,)).fetchone()
        connection.close()
        return recipe and recipe['user_id'] == curr_user['user_id']
    except Exception as e:
        return False