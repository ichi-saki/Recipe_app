from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from helpers import db_connection, add_ratings, rating_average
from functools import wraps

recipes_blueprint = Blueprint('recipes', __name__)

def login_needed(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login needed to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_func

#for home page
@recipes_blueprint.route('/')
def index():
    try:
        connection = db_connection()
        recipes = connection.execute('''SELECT r.*, u.username
                                        FROM recipe r
                                        JOIN user u ON r.user_id = u.user_id
                                        ORDER BY r.created DESC''').fetchall()
        users = connection.execute('''SELECT username
                                    FROM user
                                    ORDER BY RANDOM()
                                    LIMIT 10''').fetchall()

        connection.close()
        recipes_and_ratings = add_ratings(recipes)
        return render_template('index.html', recipes=recipes_and_ratings, users=users)
    
    except Exception as e:
        return f"Error: {str(e)}", 500

#for a single user 
@recipes_blueprint.route('/user/<username>')
def profile(username):
    connection = db_connection()

    user = connection.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

    if user is None:
        connection.close()
        return 'User not found', 404
    
    recipes = connection.execute('''SELECT r.*
                            FROM recipe r
                            WHERE r.user_id = ?
                            ORDER BY r.created DESC''', (user['user_id'],)).fetchall()
    
    recipes_and_ratings = add_ratings(recipes)

    collections = connection.execute('''SELECT c.*, COUNT(rc.recipe_id) as recipe_count
                                        FROM collection c
                                        LEFT JOIN recipe_collection rc ON c.collection_id = rc.collection_id
                                        WHERE c.user_id = ?
                                        GROUP BY c.collection_id
                                        ORDER BY c.created DESC''', (user['user_id'],)).fetchall()
    connection.close()

    own_profile = 'user_id' in session and session['user_id'] == user['user_id']

    return render_template('profile.html', user=user, recipes=recipes_and_ratings,collections=collections, own_profile=own_profile)

#for individual recipe page with comments and ratings
@recipes_blueprint.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    connection = db_connection()

    recipe = connection.execute('''SELECT r.*, u.username
                                    FROM recipe r
                                    JOIN user u ON r.user_id = u.user_id
                                    WHERE r.recipe_id = ?''', (recipe_id,)).fetchone()
    if recipe is None:
        connection.close()
        return redirect(url_for('recipes.index'))
    
    rating_ave, rating_count = rating_average(recipe_id)

    user_has_rated = False
    user_rating = None
    user_collections = []

    if 'user_id' in session:
        user_rating_data = connection.execute('SELECT value FROM rating WHERE user_id = ? AND recipe_id = ?', (session['user_id'], recipe_id)).fetchone()
        if user_rating_data:
            user_has_rated = True
            user_rating = user_rating_data['value']
        user_collections = connection.execute('''SELECT collection_id, name FROM collection 
                                                WHERE user_id = ? ORDER BY name''', (session['user_id'],)).fetchall()
        

    comments = connection.execute('''SELECT c.*, u.username
                                    FROM comment c
                                    JOIN user u ON c.user_id = u.user_id
                                    WHERE c.recipe_id = ?
                                    ORDER BY c.created DESC''', (recipe_id,)).fetchall()
    
    collections = connection.execute('''SELECT c.*
                                        FROM collection c
                                        JOIN recipe_collection rc on c.collection_id = rc.collection_id
                                        WHERE rc.recipe_id = ? AND c.user_id = ?''', (recipe_id, recipe['user_id'])).fetchall()
    
    connection.close()

    return render_template('recipe.html', recipe=recipe, rating_ave=rating_ave, rating_count=rating_count, user_has_rated=user_has_rated, user_rating=user_rating, user_collections=user_collections, comments=comments, collections=collections)