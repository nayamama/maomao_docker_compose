# -*- coding: UTF-8 -*-
import os
import datetime
from flask import render_template, abort, flash, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import home
from ..admin.forms import AnchorForm, PenaltyForm
from ..models import Anchor, Penalty
from .. import db
from ..admin.helper import add_log


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
            momo_number=form.momo_number.data,
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

            upload_folder = os.getenv('UPLOAD_FOLDER')
            directory = upload_folder + "/" + form.momo_number.data
            
            if not os.path.exists(directory):
                os.mkdir(directory)

            flash('你已成功加入一个新主播记录。')

            add_log(current_user.username, 
                    "Add", target_id = anchor.id, target_table="anchors")
        except:
            flash('错误:主播陌陌号已在数据库中。')
            db.session.rollback()
            add_log(current_user.username, 
                    "Add", target_table="anchors", status="F")

        return redirect(url_for('home.dashboard'))

    return render_template('admin/anchors/anchor.html', action="Add", form=form,
                           add_anchor=add_anchor, title="Add Anchor")


@home.route('/dashboard/penalty_form', methods=['GET', 'POST'])
@login_required
def add_penalty():
    """
    Add a penalty input
    """
    form = PenaltyForm()

    if form.validate_on_submit():
        penalty = Penalty(
            anchor_momo=form.momo_number.data,
            date=datetime.date.today().strftime("%Y-%m-%d"),
            amount=form.amount.data
        )
        try:
            db.session.add(penalty)
            db.session.commit()

            flash(u'此罚款记录已成功录入')

            add_log(current_user.username, 
                    "Add", target_id=penalty.id, 
                    target_table="penalties")
        except:
            flash(u'错误:此陌陌号不存在, 请验证输入的陌陌号重试')
            
            db.session.rollback()
            add_log(current_user.username,
                    "Add", target_table="penalties", status="F")

        return redirect(url_for('home.dashboard'))

    return render_template('home/add_penalty.html', form=form,
                            title="Add Penalty")
