"""Email utilities for the Library Management System."""

from flask import render_template_string
from flask_mail import Message
from app import mail


def send_email(subject, recipient, html_body):
    """Send an email."""
    try:
        msg = Message(subject=subject, recipients=[recipient])
        msg.html = html_body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_rental_confirmation(user, book, rental):
    """Send rental confirmation email."""
    html = f"""
    <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #7c3aed;">📚 LibraVault — Rental Confirmation</h2>
        <hr style="border: 1px solid #eee;">
        <p>Hi <strong>{user.full_name}</strong>,</p>
        <p>You have successfully rented the following book:</p>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <p><strong>Book:</strong> {book.title}</p>
            <p><strong>Author:</strong> {book.author.name}</p>
            <p><strong>Rental Period:</strong> {rental.rental_days} days</p>
            <p><strong>Due Date:</strong> {rental.due_date.strftime('%d %B %Y')}</p>
            <p><strong>Amount:</strong> ₹{rental.rental_amount:.2f}</p>
        </div>
        <p style="color: #ef4444;"><strong>⚠️ Please return the book by the due date to avoid late fees.</strong></p>
        <p>Thank you,<br>LibraVault Team</p>
    </div>
    """
    return send_email(
        subject=f"Rental Confirmation — {book.title}",
        recipient=user.email,
        html_body=html,
    )


def send_overdue_reminder(user, rental):
    """Send overdue reminder email."""
    html = f"""
    <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #ef4444;">⚠️ LibraVault — Overdue Notice</h2>
        <hr style="border: 1px solid #eee;">
        <p>Hi <strong>{user.full_name}</strong>,</p>
        <p>The following book is <strong>overdue</strong>:</p>
        <div style="background: #fef2f2; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #ef4444;">
            <p><strong>Book:</strong> {rental.book.title}</p>
            <p><strong>Due Date:</strong> {rental.due_date.strftime('%d %B %Y')}</p>
            <p><strong>Days Overdue:</strong> {rental.overdue_days} days</p>
            <p><strong>Estimated Late Fee:</strong> ₹{rental.overdue_days * 5:.2f}</p>
        </div>
        <p>Please return the book as soon as possible to minimize late charges.</p>
        <p>Thank you,<br>LibraVault Team</p>
    </div>
    """
    return send_email(
        subject=f"Overdue Notice — {rental.book.title}",
        recipient=user.email,
        html_body=html,
    )


def send_due_date_reminder(user, rental):
    """Send due date reminder email (1 day before)."""
    html = f"""
    <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #f59e0b;">📅 LibraVault — Due Date Reminder</h2>
        <hr style="border: 1px solid #eee;">
        <p>Hi <strong>{user.full_name}</strong>,</p>
        <p>This is a friendly reminder that the following book is <strong>due tomorrow</strong>:</p>
        <div style="background: #fffbeb; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #f59e0b;">
            <p><strong>Book:</strong> {rental.book.title}</p>
            <p><strong>Due Date:</strong> {rental.due_date.strftime('%d %B %Y')}</p>
        </div>
        <p>Please return the book on time to avoid late fees.</p>
        <p>Thank you,<br>LibraVault Team</p>
    </div>
    """
    return send_email(
        subject=f"Due Date Reminder — {rental.book.title}",
        recipient=user.email,
        html_body=html,
    )


def send_approval_notification(user):
    """Send account approval notification email."""
    html = f"""
    <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #22c55e;">✅ LibraVault — Account Approved!</h2>
        <hr style="border: 1px solid #eee;">
        <p>Hi <strong>{user.full_name}</strong>,</p>
        <p>Great news! Your LibraVault account has been <strong>approved</strong> by an administrator.</p>
        <p>You can now browse and rent books from our library.</p>
        <p>Happy reading! 📚<br>LibraVault Team</p>
    </div>
    """
    return send_email(
        subject="Your LibraVault Account is Approved!",
        recipient=user.email,
        html_body=html,
    )
