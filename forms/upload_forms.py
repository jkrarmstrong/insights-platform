from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    """
    Form for uploading files.
    """
    file = FileField('Upload CSV', validators=[DataRequired()])
