from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from datetime import datetime
from . import db
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

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
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