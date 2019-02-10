#Modified from the flaskr app tutorial; see http://flask.pocoo.org/docs/1.0/tutorial

#script assumes the following two environement variables ahve been set:

  # 84  export FLASK_APP=flaskr
  # 85  export FLASK_ENV=development

import os

from flask import Flask
def create_app(test_config=None):
	#create and configure the app
	app = Flask(__name__, instance_relative_config=True)
		# instance_relative_config=True -> allows the app to look for configs in a separate folder from the rest of the code (which allows for storage of data that doesn't go into version control, like configurataion secrets and the .sqlite file)	
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path,'incremental.sqlite'),
		SESSION_TYPE='filesystem',
		SESSION_FILE_DIR=os.path.join(app.instance_path,'incremental_sessions'),
	)
	Session(app)

	if test_config is None:
		#load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		#load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass



	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, world!'

	from . import db # import flaskr/db.py
	db.init_app(app)

	from . import auth # import flaskr/auth.py
	app.register_blueprint(auth.bp) #gives views to register new users and log them in and out

	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	return app