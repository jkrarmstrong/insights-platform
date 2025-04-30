# --- Imports ---
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.auth_forms import RegistrationForm, LoginForm
from models.user_model import db, User, bcrypt
import pandas as pd
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from datetime import timedelta


# --- Flask App setup ---
app = Flask(__name__)


# --- Config application ---

# Database and secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "my_secret_key"

# Setup folder to store uploads
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["ALLOWED_EXTENSIONS"] = {"csv"}

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

app.config['WTF_CSRF_ENABLED'] = False


# --- Initialize Flask extensions
db.init_app(app)
bcrypt.init_app(app)

# --- Initialize LoginManager for handling login
login_manager = LoginManager(app)
login_manager.login_view = "login" # Redirect to login if user without account tries to access

# --- Initialize Flask-Migrate
migrate = Migrate(app, db)



# --- Helper functions ----

# user_loader is used by Flask-login to retrieve current user based on ther user ID in the session
# then queries the databse to return the right object
@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with ID: {user_id}")
    return User.query.get(int(user_id))


def allowed_file(filename):
    """
    Checks if file uploaded is allowed.
    """
    
    # If no file or file does not contain "."
    if not filename or "." not in filename:
        return False
    # Get file extension and convert til lower (CSV == csv)
    extension = filename.rsplit(".", 1)[1].lower()
    #Check if extension is allowed (i.e. in the list)
    return extension in app.config["ALLOWED_EXTENSIONS"]


# --- Routes ---
@app.route("/")
def home():
    return "It's working"


@app.route("/analyze_data", methods=["GET"])
@login_required
def analyze_data():
    """
    Analyzes the data. For now it calculates the mean of a given column.
    """
    data = current_user.get_data()
    if data is None:
        column_name = "value_column"
        if column_name in data.columns:
            average = data[column_name].mean()
            return jsonify({"average": average})
        else:
            flash("Column not found in data", "danger")
    else:
        flash("No data found for analyze", "danger")

    return redirect(url_for("dashboard"))


@app.route("/upload_data", methods=["GET", "POST"])
@login_required
def upload_data():
    """
    This function handles file uploads.
    """
    if request.method == "POST":
        if "file" not in request.files: # Check for files field in form
            flash("No file part", "danger")
            return redirect(request.url) # Redirect if no files field

        file = request.files["file"] # Get file from form
        if file.filename == "": # If no file is chosen
            flash("No selected file", "danger")
            return(redirect(request.url)) # Redirect again
        
        if file and allowed_file(file.filename): # If file exists and alloed file format
            filename = secure_filename(file.filename) # Secures the filename 
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename) # Generates full path for storage of file
            file.save(filepath) # Store file in desired folder

            # Read file with Pandas
            data = pd.read_csv(filepath)

            # Stores data for the current user
            current_user.save_data(data)

            flash("Data uploaded and saved successfully", "success")
            return redirect(url_for("dashboard"))
        
    # If method is GET, render upload_data.html
    return render_template("upload_data.html", title="Upload Data")



@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration of a new user.
    """
    
    form = RegistrationForm()
    if form.validate_on_submit(): # If form is valid
        print("Form is valid, processing data..") # testing purposes DELETE LATER
        # Check if the email already is in use
        existing_user = User.query.filter_by(email=form.email.data).first()

        # If the user already exists, redirect to register site
        if existing_user:
            flash("Email already exists", "danger")
            return redirect(url_for("register"))
        
        # Create user
        user = User(email=form.email.data)
        user.set_password(form.password.data)

        # Add user to database and commit changes
        db.session.add(user)
        db.session.commit()

        flash("Your account has succesfully been created! You can now login.", "success")
        return redirect(url_for("login")) # Send user to login
    
    if form.errors:
        print("form errors:", form.errors) # testing purposes

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login of a user.
    """

    form = LoginForm()
    if form.validate_on_submit(): # If form is valid
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data): # Checks the password
            login_user(user) # Login user
            print(f"{user.email} logged in succesfully")
            return redirect(request.args.get("next") or url_for("dashboard")) # Send user to the dashboard
    
        flash("Login failed. Check if email and/or password is correct", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/dashboard")
@login_required # User needs to be logged in
def dashboard():
    """
    Route displays dashboard.
    """
    print(f"Current user: {current_user.is_authenticated}, {current_user.email}")  # Debugging line
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("dashboard.html", title="Dashboard")


if __name__ == "__main__":
    app.run(debug=True)