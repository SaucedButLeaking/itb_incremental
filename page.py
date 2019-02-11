from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
	)
from werkzeug.exceptions import abort

from itb_incremental.auth import login_required
from itb_incremental.db import get_db
import itb_incremental.engine

bp = Blueprint('page',__name__)

@bp.route('/')
@login_required
def index():
	db = get_db()

	jobs = db.execute('SELECT id, name, type, reward, length, description, level FROM jobs WHERE available="true"').fetchall()
	return render_template('page/index.html', jobs=jobs)

	# posts = db.execute('SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC').fetchall()
	# return render_template('blog/index.html', posts=posts)














########everything below is from when this was a blog tutorial. Keeping the bones for reference, but will need to remove prior to release
''' #comment this line out to get syntax highlighting
@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None

		if not title:
			error = 'Title is required'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute('INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)',(title, body, g.user['id']))
			db.commit()
			return redirect(url_for('blog.index'))
	return render_template('blog/create.html')


def get_post(id, check_author=True):
	post = get_db().execute('SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?', (id,)).fetchone()

	if post is None:
		abort(404, "Post id {0} doesn't exist".format(id))

	if check_author and post['author_id'] != g.user['id']:
		abort(403)

	return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required

# <int:id> will capture an integer from the position between the two slashes in a relevant URL
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)



@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
'''
