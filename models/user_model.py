# --- Imports ---
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# --- Setup SQLAlchemy and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()


class UserData(db.Model):
    """
    Stores data for the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    data = db.Column(db.JSON, nullable=False)

    user = db.relationship("User", back_populates="data_entries")


class User(db.Model):
    """
    Defines a user in the application. This model stores the users email and password.
    """

    # Define columns in the user table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    data_entries = db.relationship('UserData', back_populates='user')


    def __repr__(self):
        # Helps for debugging
        return f"<User {self.email}>"
    
    def save_data(self, data):
        """
        Save the given data for the user.
        Converts the DataFrame to JSON-format.
        """

        data_json = data.to_dict(orient="records")

        user_data = UserData(data=data_json, user_id=self.id)
        db.session.add(user_data)
        db.session.commit()

    def get_data(self):
        return [entry.data for entry in self.data_entries]


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