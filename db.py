import sqlite3

import click
from flask import current_app, g
# g is a special object that is unique for each request. Is used to store data that might be accessed by multiple functions during the request.
# current_app is also a special object, which points to the flask application handling therequest. "Since [we] used an application factor, there is no application object when writing the rest of [our] code"
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

admin_password = "password" #SUPER NOT OKAY, CHANGE THIS IMMEDIATELY. WHAT AM I EVEN THINKING

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
			)
		g.db.row_factory = sqlite3.Row  #Row method tells the connection to return rows that behave like dicts, allowing us to access columns by name
	return g.db

def close_db(e=None):
	# if a db connection was established by the current request, close it
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_db():
	# Set the database to an initial state
	db = get_db()

	with current_app.open_resource('schema.sql') as f: #basically a with open, but aware of where the app is running
		db.executescript(f.read().decode('utf8'))

@click.command('init-db') # defines a command line command called 'init-db' which will call the init_db function and return a success message
@with_appcontext
def init_db_command():
	# Clear the existing data and create new tables.
	init_db()
	db = get_db()
	db.execute('INSERT INTO user (username, password, privileges, credits) VALUES ("admin", ?, 42, 1000)', (generate_password_hash(admin_password),))
	db.commit()
	click.echo('Initialized the datbase.')

def init_app(app):
	app.teardown_appcontext(close_db) #tells flask to run close_db after returning a response
	app.cli.add_command(init_db_command)

