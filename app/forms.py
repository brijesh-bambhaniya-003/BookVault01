"""WTForms for the Library Management System."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    IntegerField, DecimalField, SelectField, BooleanField,
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Optional, NumberRange, ValidationError,
)
from app.models import User


# ─── Auth Forms ─────────────────────────────────────────────

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


# ─── Admin Forms ────────────────────────────────────────────

class BookForm(FlaskForm):
    """Form for adding/editing books."""
    title = StringField('Book Title', validators=[DataRequired(), Length(max=250)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    genre_id = SelectField('Genre', coerce=int, validators=[Optional()])
    price = DecimalField('Price (₹)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    rent_per_day = DecimalField('Rent per Day (₹)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Book')


class AuthorForm(FlaskForm):
    """Form for adding/editing authors."""
    name = StringField('Author Name', validators=[DataRequired(), Length(max=150)])
    bio = TextAreaField('Biography', validators=[Optional()])
    submit = SubmitField('Save Author')


class GenreForm(FlaskForm):
    """Form for adding/editing genres."""
    name = StringField('Genre Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Genre')


class SettingsForm(FlaskForm):
    """Form for library settings."""
    late_fee_per_day = DecimalField(
        'Late Fee per Day (₹)', places=2,
        validators=[DataRequired(), NumberRange(min=0)]
    )
    max_books_per_user = IntegerField(
        'Max Books per User',
        validators=[DataRequired(), NumberRange(min=1)]
    )
    submit = SubmitField('Save Settings')


# ─── User Forms ─────────────────────────────────────────────

class RentForm(FlaskForm):
    """Form for renting a book."""
    rental_period = SelectField(
        'Rental Period',
        choices=[
            ('1', '1 Day'),
            ('2', '2 Days'),
            ('3', '3 Days'),
            ('4', '4 Days'),
            ('5', '5 Days'),
            ('6', '6 Days'),
            ('30', '1 Month'),
            ('60', '2 Months'),
            ('90', '3 Months'),
            ('120', '4 Months'),
            ('150', '5 Months'),
            ('180', '6 Months'),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField('Rent Book')


class ProfileForm(FlaskForm):
    """Form for updating user profile."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Update Profile')
