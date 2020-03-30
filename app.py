"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, redirect, flash, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake, default_img

app = Flask(__name__)

app.config["SECRET_KEY"] = "Shhhhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# const for responses
status_ok = 200
status_updated = 201


def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


@app.route('/')
def index():
    '''Return index page showing all cupcakes'''
    return render_template('index.html')


@app.route("/api/cupcakes")
def list_all_cupcakes():
    '''Grab all cupcakes from cupcakes DB'''

    cupcakes = Cupcake.query.all()

    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:id>")
def list_single_cupcake(id):
    '''Grab single cupcake from cupcakes DB using Id'''

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    '''Create new cupcake and add to cupcakes DB'''

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    # If empty input, provide default image
    if image == '':
        image = default_img

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=serialize_cupcake(new_cupcake)), status_updated)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    '''Update single cupcake from cupcakes DB'''

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = flavor
    cupcake.size = size
    cupcake.rating = rating
    cupcake.image = image

    db.session.commit()
    return (jsonify(cupcake=serialize_cupcake(cupcake)), status_ok)


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    '''Delete single cupcake from cupcakes DB'''

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(message="Deleted"), status_ok)
