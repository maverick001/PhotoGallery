from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, SelectField, IntegerField
from wtforms.fields import TextAreaField, DecimalField
from wtforms.fields import DateTimeLocalField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Email



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    user_type = SelectField('Login as', choices=[('client', 'Client'), ('photographer', 'Photographer'), ('admin', 'Administrator')], validators=[InputRequired()])
    submit = SubmitField('Login')


class ClientRegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Phone', validators=[InputRequired()])
    address = TextAreaField('Address', validators=[InputRequired()])
    submit = SubmitField('Register')


class PhotographerRegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Phone', validators=[InputRequired()])
    specialization = StringField('Specialization', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price_per_hr = DecimalField('Price Per Hour', validators=[InputRequired()])
    submit = SubmitField('Register')


class BookingForm(FlaskForm):
    photographer_id = StringField('Photographer ID', validators=[InputRequired()])
    category_id = StringField('Category ID', validators=[InputRequired()])
    descriptions = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    duration = IntegerField('Duration (hours)', validators=[InputRequired()])
    submit = SubmitField('Book Session')


class ImageUploadForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    category_id = SelectField('Category', validators=[InputRequired()])
    image_file = FileField('Image File', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    visibility = SelectField('Visibility', choices=[('Published', 'Published'), ('Hidden', 'Hidden')], validators=[InputRequired()])
    submit = SubmitField('Upload Image')


class PaymentForm(FlaskForm):
    payment_method = SelectField('Payment Method',
                                 choices=[('Visa', 'Visa'), ('MasterCard', 'MasterCard'),
                                          ('Paypal', 'Paypal'), ('Afterpay', 'Afterpay'), ('ZIP', 'ZIP')],
                                 validators=[InputRequired()])
    submit = SubmitField('Complete Payment')


class AddPhotographerForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Phone', validators=[InputRequired()])
    specialization = StringField('Specialization', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price_per_hr = DecimalField('Price Per Hour', validators=[InputRequired()])
    submit = SubmitField('Add Photographer')
