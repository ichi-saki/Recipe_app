from flask import Blueprint, request, redirect, url_for, flash, session
from helpers import db_connection, is_owner
from functools import wraps

comments_blueprint = Blueprint('comments', __name__)

def login_needed(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login needed to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_func

@comments_blueprint.route('/recipe/<int:recipe_id>/comment', methods=['POST'])
@login_needed
def make_comment(recipe_id):
    comment_text = request.form['comment_text'].strip()

    if not comment_text:
        flash('No comment text', 'error')
        return redirect(url_for('recipes.recipe', recipe_id=recipe_id))
    connection = db_connection()

    try:
        connection.execute('''INSERT INTO comment (user_id, recipe_id, comment_text)
                            VALUES (?, ?, ?)''', (session['user_id'], recipe_id, comment_text))
        connection.commit()
        flash('Comment successfully added', 'success')
    except Exception as e:
        flash(f'Error making comment: {str(e)}', 'error')
    finally:
        connection.close()
    
    return redirect(url_for('recipes.recipe', recipe_id=recipe_id))

@comments_blueprint.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_needed
def delete_comment(comment_id):
    connection = db_connection()
    recipe_id = None

    try:
        comment = connection.execute('SELECT * FROM comment WHERE comment_id = ?', (comment_id,)).fetchone()

        if not comment:
            flash('Comment not found', 'error')
            connection.close()
            return redirect(url_for('recipes.index'))
        
        recipe_id = comment['recipe_id']

        if comment['user_id'] == session['user_id'] or is_owner(recipe_id):
            connection.execute('DELETE FROM comment WHERE comment_id = ?', (comment_id,))
            connection.commit()
            flash('Comment deleted successfully', 'success')
        else:
            flash('Only comment creater can delete their comments', 'error')

    except Exception as e:
        flash(f'Error deleting comment: {str(e)}', 'error')
    finally:
        connection.close()

    return redirect(url_for('recipes.recipe', recipe_id=recipe_id))