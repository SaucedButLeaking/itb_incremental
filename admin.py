@bp.route('/createJob', methods=('GET','POST'))
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
			for key,val in submit:
				db.execute('INSERT INTO jobs (?) VALUES (?)',key,val)
			# db.execute('INSERT INTO jobs (title, body, author_id) VALUES (?, ?, ?)',(title, body, g.user['id']))
			db.commit()
			return redirect(url_for('page.index'))
	return render_template('admin/createJob.html')