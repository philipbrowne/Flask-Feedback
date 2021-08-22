from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    feedback = db.relationship('Feedback', cascade = 'all,delete', backref='user')


    @classmethod
    def register(cls, username, password):
        """Register usedr with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(password)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')
        # Return instance of user with username and hashed password 
        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct
        
        Return user if valid; otherwise return False.
        """
        # Queries for unique username from database
        user = User.query.filter_by(username=username).first()
        # If valid user and if password check lines up with database hash
        if user and bcrypt.check_password_hash(user.password, password):
            # Return User instance
            return user
        else:
            return False 
        
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Feedback(db.Model): 
    """Feedback Model"""
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username', onupdate='CASCADE', ondelete='CASCADE'))
        