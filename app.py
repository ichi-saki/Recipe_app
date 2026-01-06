from flask import Flask
from routes.auth import auth_blueprint
from routes.collections import collections_blueprint
from routes.comments import comments_blueprint
from routes.recipes import recipes_blueprint

app = Flask(__name__)
app.config['SECRET_KEY']='recipe332app'

app.register_blueprint(auth_blueprint)
app.register_blueprint(collections_blueprint)
app.register_blueprint(comments_blueprint)
app.register_blueprint(recipes_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
