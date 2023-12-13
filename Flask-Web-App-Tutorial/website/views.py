# views.py

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from datetime import datetime
from . import db
from flask import redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_text = request.form.get('note')
        
        if len(note_text) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note_text, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            
            user_first_name = current_user.first_name
            note_date = datetime.utcnow().strftime('%B %d, %Y %I:%M %p')
            flash(f'{user_first_name} posted on {note_date}', category='success')

    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, notes=notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})

@views.route('/update-note', methods=['POST'])
def update_note():
    data = json.loads(request.data)
    note_id = data.get('noteId')
    updated_content = data.get('updatedContent')
    note = Note.query.get(note_id)

    if note and note.user_id == current_user.id:
        note.data = updated_content
        db.session.commit()
        return jsonify({"message": "Note updated successfully"})
    else:
        return jsonify({"error": "Unable to update note"})

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        new_first_name = request.form.get('first_name')

        if new_email:
            current_user.email = new_email

        if new_password:
            # Check if the new password is not empty
            if new_password.strip():
                # Use set_password to hash the password
                current_user.set_password(new_password)

        if new_first_name:
            current_user.first_name = new_first_name

        db.session.commit()
        flash('Profile updated successfully!', category='success')

    return redirect(url_for('views.profile'))
