import itb_incremental.db

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
	if request.method == 'POST':
		submit = dict()
		for key, val in request.form:
			submit[key] = val
		# submit['name'] = request.form['name']
		# submit['description'] = request.form['description']
		error = None

		if not any(x for x in submit):
			#I _think_ this will evaluate true if any of the fields were blank
			error = 'All fields are required'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			keys = list()
			vals = list()
			for key,val in submit:
				keys = keys.append(key)
				vals = vals.append(val)
			cols = tuple(keys)
			vals = tuple(vals)
			db.execute('INSERT INTO jobs ? VALUES ?',cols,rows)
			# db.execute('INSERT INTO jobs (title, body, author_id) VALUES (?, ?, ?)',(title, body, g.user['id']))
			db.commit()
			return redirect(url_for('admin.create'))
	# get lists of column names to dynamically generate forms for manual content addition
	db = get_db()
	cursorJobs = db.execute('select * from jobs')
	colsJobs = [description[0] for description in cursorJobs.description] #.description is a method in sqlite
	cursorShips = db.execute('select * from ships')
	colsShips = [description[0] for description in cursorShips.description]
	cursorCrew = db.execute('select * from crew')
	colsCrew = [description[0] for description in cursorCrew.description]
	fields = { "colsJobs" : colsJobs, "colsShips" : colsShips, "colsCrew" : colsCrew }

	return render_template('admin/create.html',fields=fields)