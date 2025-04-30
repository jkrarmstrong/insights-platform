# --- Imports ---
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# --- Setup SQLAlchemy and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """
    Defines a user in the application. This model stores the users email and password.
    """

    # Define columns in the user table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        # Helps for debugging
        return f"<User {self.email}>"


    def check_password(self, password):
        """
        Check if password given matches the hashed password stored in the database.
        Returns True if it matches.
        """

        return bcrypt.check_password_hash(self.password, password)
    
    def set_password(self, password):
        """
        Generates a hashed password.
        Returns it in a utf-8 string.
        """

        self.password = bcrypt.generate_password_hash(password).decode("utf-8")


    def get_id(self):
        """
        Returns the user ID for Flask-Login to use for session management.
        This method is required by Flask-Login.
        """
        return str(self.id)
    
    @property
    def is_authenticated(self):
        """
        Returns whether the user is authenticated.
        This is required by Flask-Login.
        """
        return True  # Since the user is authenticated upon login