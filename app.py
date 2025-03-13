# import modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create the Flask application
app = Flask(__name__)

# === configure sqlite database ===
# db file name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wma_tracker.db' 
# disable modification tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the database
db = SQLAlchemy(app)

# === Define the WMA model(db table) ===
class WMA(db.Model):
    id = db.Column(db.Integer, primary_key=True) # unique id for wma's
    name = db.Column(db.String(200), nullable=False) # name of wma cannot be empty
    deer = db.Column(db.Boolean, default=False) # deer sighting? default is false
    turkey = db.Column(db.Boolean, default=False) # turkey sighting, default is false
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # timestamp for when wma was added

    # the string representation of the wma object
    def __repr__(self):
        return f'<WMA {self.name}>'

# if db tables do not already exist, create the db tables
with app.app_context():
    db.create_all()

# home route - display all the wmas
@app.route('/')
def index():
    # query all WMAs from the db, ordered by creation date - newest WMA shown first
    wmas = WMA.query.order_by(WMA.created_at.desc()).all()
    # render the index.html template and pass the WMAs to it
    return render_template('index.html', wmas=wmas)

# Route to add a new WMA
@app.route('/add', methods=['POST'])
def add():
    # Get the WMA name from the form submission
    name = request.form.get('name')

    # IF name is not empty, create a new WMA and add it to db
    if name:
        new_wma = WMA(name=name)
        db.session.add(new_wma)
        db.session.commit()
    # redirect back to homepage
    return redirect(url_for('index'))

# Route to update deer and turkey sightings
@app.route('/update/<int:wma_id>', methods=['POST'])
def update(wma_id):
    # Find the WMA by its ID or return a error if not found
    wma = WMA.query.get_or_404(wma_id)
    # update the deer/turkey fields based on form submission
    wma.deer = 'deer' in request.form # True boolean is deer box is checked
    wma.turkey = 'turkey' in request.form # True if the turkey checkbox checked

    # Save your changes to the db
    db.session.commit()
    # redirect user back to homepage
    return redirect(url_for('index'))

# Route to delete a WMA
@app.route('/delete/<int:wma_id>')
def delete(wma_id):
    # code to find wma by it's ID or return an error
    wma = WMA.query.get_or_404(wma_id)
    # delete wma from DB
    db.session.delete(wma)
    db.session.commit()
    # redirect back to homepage
    return redirect(url_for('index'))

# run FLASK in debug mode
if __name__ == '__main__':
    app.run(debug=True)

    




