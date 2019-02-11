import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
	)
from flask.ext.session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from itb_incremental.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


#create a view to handle registrations throuhg /auth/register

@bp.route('/register', methods=('GET','POST')) #associates /register URL with the following function
def register():
	if request.method == 'POST':
		username = request.form['username'] #request.form is a special dict mapping user-submitted form data
		password = request.form['password']
		db = get_db ()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password: 
			error = 'Password is required.'
		elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
			error = 'User {} is already registered'.format(username)
			# two interesting things: ? is a placeholder in SQL statements that gets filled in by the variable it gets passed
			# and {} does something similar with strings 

		if error is None:
			db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password))) # acts kinda like sprintf in PHP
			db.commit()
			return redirect(url_for('auth.login'))

		flash(error)
		
	return render_template('auth/register.html')	


@bp.route('/login', methods=('GET','POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

		if user is None: 
			error: 'Incorrect username'
		elif not check_password_hash(user['password'], password):
			error('Incorrect password')

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			session['username'] = user['username']
			session['privileges'] = user['privileges']
			session['ships'] = list(user['ship1'],user['ship2']) #should become a while loop to iterate over all ships, but for now this works TECHDEBT
			session['jobs'] = list(user['ship1job'],user['ship2job']) #TECHDEBT
			return redirect(url_for('index'))

		flash(error)
	return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute('select * from user where id = ?',(user_id,)).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view