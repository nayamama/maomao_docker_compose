import os
import datetime
from flask import render_template, abort, flash, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import home
from ..admin.forms import AnchorForm
from ..models import Anchor
from .. import db


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/dashboard/add_anchor', methods=['GET', 'POST'])
@login_required
def add_anchor():
    """
    Add an anchor 
    """

    add_anchor = True

    form = AnchorForm()
    del form.photo
    del form.entry_time

    if form.validate_on_submit():
        anchor = Anchor(
            name=form.name.data,
            entry_time=datetime.datetime.now().strftime("%Y-%m-%d"),
            address=form.address.data,
            mobile_number=form.mobile_number.data,
            id_number=form.id_number.data,
            basic_salary_or_not=form.basic_salary_or_not.data,
            basic_salary=form.basic_salary.data,
            live_time=form.live_time.data,
            live_session=form.live_session.data,
            percentage=form.percentage.data,
            ace_anchor_or_not=form.ace_anchor_or_not.data,
            agent=form.agent.data
        )
        try:
            db.session.add(anchor)
            db.session.commit()

            directory = '/home/qi/projects/maomao_files/' + form.name.data
            if not os.path.exists(directory):
                os.mkdir(directory)

            flash('You have successfully added a new anchor.')
        except:
            flash('Error: anchor name already exists.')

        return redirect(url_for('home.dashboard'))

    return render_template('admin/anchors/anchor.html', action="Add", form=form,
                           add_anchor=add_anchor, title="Add Anchor")

