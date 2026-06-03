"""Database models for the Library Management System."""

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """User model for both admin and normal users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.Enum('admin', 'user', name='user_role'), default='user', nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    rentals = db.relationship('Rental', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        """Check if user is admin."""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


class Author(db.Model):
    """Author model."""
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    books = db.relationship('Book', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<Author {self.name}>'


class Genre(db.Model):
    """Genre / Category model."""
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    books = db.relationship('Book', backref='genre', lazy='dynamic')

    def __repr__(self):
        return f'<Genre {self.name}>'


class Book(db.Model):
    """Book model."""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    rent_per_day = db.Column(db.Numeric(10, 2), nullable=False, default=10.00)
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)
    cover_image = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    rentals = db.relationship('Rental', backref='book', lazy='dynamic')

    @property
    def is_available(self):
        """Check if book has copies available."""
        return self.available_copies > 0

    def __repr__(self):
        return f'<Book {self.title}>'


class Rental(db.Model):
    """Rental / Borrowing model."""
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    rented_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_on = db.Column(db.DateTime, nullable=True)
    rental_days = db.Column(db.Integer, nullable=False)
    rental_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    late_fee = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    status = db.Column(
        db.Enum('active', 'returned', 'overdue', name='rental_status'),
        default='active',
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def calculate_late_fee(self, fee_per_day=5.00):
        """Calculate late fee based on overdue days."""
        if self.returned_on and self.returned_on > self.due_date:
            overdue_days = (self.returned_on - self.due_date).days
            if overdue_days < 1:
                overdue_days = 1  # Minimum 1 day charge
            self.late_fee = round(overdue_days * fee_per_day, 2)
        else:
            self.late_fee = 0.00
        return self.late_fee

    @property
    def total_charge(self):
        """Total charge = rental amount + late fee."""
        return float(self.rental_amount) + float(self.late_fee)

    @property
    def is_overdue(self):
        """Check if rental is overdue."""
        if self.status == 'returned':
            return False
        return datetime.utcnow() > self.due_date

    @property
    def overdue_days(self):
        """Get number of overdue days."""
        if not self.is_overdue:
            return 0
        return (datetime.utcnow() - self.due_date).days

    def __repr__(self):
        return f'<Rental {self.id} - User:{self.user_id} Book:{self.book_id}>'


class Settings(db.Model):
    """Global library settings."""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    late_fee_per_day = db.Column(db.Numeric(10, 2), nullable=False, default=5.00)
    max_books_per_user = db.Column(db.Integer, default=5)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Settings late_fee={self.late_fee_per_day}>'
