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
