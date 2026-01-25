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

@collections_blueprint.route('/collection/new', methods=['GET', 'POST'])
@login_needed
def create_collection():
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()

        if not name:
            flash('Collection name is needed', 'error')
            return render_template('create_collection.html')
        
        connection = db_connection()
        try:
            connection.execute('''INSERT INTO collection (user_id, name, description)
                               VALUES (?, ?, ?)''', (session['user_id'], name, description))
            connection.commit()
            flash('Collection successfully created', 'success')
            return redirect(url_for('recipes.profile', username=session['username']))
        except Exception as e:
            flash(f'Collection creation error: {str(e)}', 'error')
        finally:
            connection.close()

    return render_template('create_collection.html')
@collections_blueprint.route('/collection/<int:collection_id>/delete', methods=['POST'])
@login_needed
def delete_collection(collection_id):
    connection = db_connection()

    try:
        collection = connection.execute('SELECT * FROM collection WHERE collection_id = ? AND user_id = ?', (collection_id, session['user_id'])).fetchone()

        if not collection:
            flash('Collection access denied or not found', 'error')
            connection.close()
            return redirect(url_for('recipes.profile', username=session['username']))
        
        connection.execute('DELETE FROM recipe_collection WHERE collection_id = ?', (collection_id,))

        connection.execute('DELETE FROM collection WHERE collection_id = ?', (collection_id,))

        connection.commit()
        flash('Collection deletion successful!', 'success')
    
    except Exception as e:
        flash(f'Collection deletion error: {str(e)}', 'error')
    finally:
        connection.close()

    return redirect(url_for('recipes.profile', username=session['username']))

@collections_blueprint.route('/recipe/<int:recipe_id>/add_to_collection', methods=['POST'])
@login_needed
def add_to_collection(recipe_id):
    
    collection_id = request.form['collection_id']

    if not collection_id:
        flash('Select a collection!', 'error')
        return redirect(url_for('recipes.recipe', recipe_id=recipe_id))
    
    connection = db_connection()

    try:
        collection = connection.execute('SELECT * FROM collection WHERE collection_id = ? AND user_id = ?', (collection_id, session['user_id'])).fetchone()

        if not collection:
            flash('Collection access denied or not found', 'error')
            connection.close()
            return redirect(url_for('recipes.recipe', recipe_id=recipe_id))
        
        exists = connection.execute('SELECT * FROM recipe_collection WHERE recipe_id = ? AND collection_id = ?', (recipe_id, collection_id)).fetchone()

        if exists:
            flash('Recipe already in collection', 'info')
        else:
            connection.execute('''INSERT INTO recipe_collection (recipe_id, collection_id)
                                VALUES (?, ?)''', (recipe_id, collection_id))
            connection.commit()
            flash('Recipe successfully added to collection', 'success')
    except Exception as e:
        flash(f'Error adding recipe to collection: {str(e)}', 'error')
    finally:
        connection.close()

    return redirect(url_for('recipes.recipe', recipe_id=recipe_id))

@collections_blueprint.route('/collection/<int:collection_id>/remove_recipe/<int:recipe_id>', methods=['POST'])
@login_needed
def remove_from_collection(collection_id, recipe_id):
    connection = db_connection()

    try:
        collection = connection.execute('SELECT * FROM collection WHERE collection_id = ? AND user_id = ?', (collection_id, session['user_id'])).fetchone()

        if not collection:
            flash('Collection access denied or not found', 'error')
            return redirect(url_for('recipes.recipe', recipe_id=recipe_id))
        
        connection.execute('''DELETE FROM recipe_collection
                            WHERE recipe_id = ? AND collection_id = ?''', (recipe_id, collection_id))
        connection.commit()
        flash('Recipe successfully removed from collection', 'success')

    except Exception as e:
        flash(f'Removing recipe from collection error: {str(e)}', 'error')
    finally:
        connection.close()

    return redirect(url_for('collections.view_collection', collection_id=collection_id))


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