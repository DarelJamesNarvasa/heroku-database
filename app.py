from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tkjjzsdmyjpbmh:3227ca576c0d9900588c49e06c749a6ed6dd9b74d38ca8b9c1a712ec846f0707@ec2-3-210-173-88.compute-1.amazonaws.com:5432/d8j3o78461he2i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@app.route('/')
def index():
    # Query all users from the database
    users = User.query.all()

    # Render the template with the list of users
    return render_template('index.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Check if users already exist
        existing_user1 = User.query.filter_by(username='john_doe').first()
        existing_user2 = User.query.filter_by(username='jane_doe').first()

        # Add users only if they don't exist
        if not existing_user1:
            user1 = User(username='john_doe', email='james@example.com')
            db.session.add(user1)

        if not existing_user2:
            user2 = User(username='jane_doe', email='jane@example.com')
            db.session.add(user2)

        db.session.commit()

    app.run(debug=True)
