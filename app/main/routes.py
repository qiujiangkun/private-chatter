from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
import random


@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        room = form.room.data
        return redirect(url_for('.chat', room=room))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = request.args.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat/<room>')
def chat(room):
    name = session.get('name', '')
    if name == '' or room == '':
        return redirect(url_for('.index', room=room))
    return render_template('chat.html', name=name, room=room)


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.index'))
