from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from helpers import db_connection, add_ratings
from functools import wraps

collections_blueprint = Blueprint('collections', __name__)

def login_needed(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login needed to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_func


@collections_blueprint.route('/collection/<int:collection_id>')
def view_collection(collection_id):
    connection = db_connection()

    collection = connection.execute('''SELECT c.*, u.username
                                    FROM collection c
                                    JOIN USER u ON c.user_id = u.user_id
                                    WHERE c.collection_id = ?''', (collection_id,)).fetchone()
    
    if not collection:
        flash('Collection not found', 'error')
        connection.close()
        return redirect(url_for('recipes.index'))
    
    recipes = connection.execute('''SELECT r.*, u.username
                                    FROM recipe r
                                    JOIN recipe_collection rc ON r.recipe_id = rc.recipe_id
                                    JOIN user u ON r.user_id = u.user_id
                                    WHERE rc.collection_id = ?
                                    ORDER BY rc.added DESC''', (collection_id,)).fetchall()
    
    recipes_with_ratings = add_ratings(recipes)
    connection.close()

    return render_template('collection.html', collection=collection, recipes=recipes_with_ratings)