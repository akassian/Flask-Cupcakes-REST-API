"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Cupcake(db.Model):
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    flavor = db.Column(db.String, nullable = False)
    size = db.Column(db.String, nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.String, nullable = False, default = 'https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg')

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)