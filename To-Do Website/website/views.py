from flask import Blueprint, render_template, request, url_for, flash, jsonify, redirect
from flask_login import  login_required, current_user
from .models import Todo
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        todo = request.form.get('todo')

        if len(todo) < 1:
            flash('Item is too short!', category='error')
        else:
            new_todo = Todo(data=todo, user_id=current_user.id)
            db.session.add(new_todo)
            db.session.commit()
            flash('Item added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/update/<int:id>', methods=['GET','POST'])
def update_todo(id):
    todo = Todo.query.get(id)

    if request.method == 'POST':
        data = todo.data
        todo.data = request.form.get('todo')
        db.session.commit()

        flash("Item updated successfully", category='success')
        return render_template("home.html", user=current_user)

    return render_template('update.html', todo=todo, user=current_user)

@views.route('/delete-todo', methods=['POST'])
def delete_todo():
    todo = json.loads(request.data)
    todoId = todo['todoId']
    todo = Todo.query.get(todoId)

    if todo:
        if todo.user_id == current_user.id:
            db.session.delete(todo)
            db.session.commit()

    return jsonify({})

