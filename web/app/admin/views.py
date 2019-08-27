# -*- coding: UTF-8 -*-
import os
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import datetime
import string
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import re

from . import admin
from forms import DepartmentForm, RoleForm, EmployeeAssignForm, AnchorForm, SearchForm, UploadForm, SearchPayrollForm, PayrollForm
from .. import db
from ..models import Department, Role, Employee, Anchor, Payroll
from helper import get_system_info


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

@admin.route('/anchors')
@login_required
def list_anchors():
    check_admin()
    """
    List all anchors
    """
    anchors = Anchor.query.all()
    return render_template('admin/anchors/anchors.html',
                           anchors=anchors, title='Anchors')
"""
@admin.route('/anchors/add_salary_anchor', methods=['GET', 'POST'])
@login_required
def add_salary_anchor():
    
    check_admin()

    add_anchor = "anchor_with_salary"

    form = AnchorForm()

    # remove no-relative fields
    del form.basic_salary_or_not
    del form.percentage
    del form.photo

    if form.validate_on_submit():
        anchor = Anchor(name=form.name.data,
                        entry_time=form.entry_time.data,
                        #basic_salary_or_not=form.basic_salary_or_not.data
                        basic_salary_or_not=True,
                        basic_salary=form.basic_salary.data)
                        #percentage=form.percentage.data
                        #total_paid=form.total_paid.data,
                        #owned_salary=form.owned_salary.data

        try:
            db.session.add(anchor)
            db.session.commit()

            # create folder to store personal image files
            directory = '/home/qi/projects/maomao_files/' + form.name.data
            if not os.path.exists(directory):
                os.mkdir(directory)
            flash('You have successfully added a new anchor.')
        except:
            flash('Error: anchor name already exists.')

        return redirect(url_for('admin.list_anchors'))

    # load anchor template
    return render_template('admin/anchors/anchor.html', action="Add",
                           add_anchor=add_anchor, form=form,
                           title="Add Anchor with Salary")

@admin.route('/anchors/add_commission_anchor', methods=['GET', 'POST'])
@login_required
def add_commission_anchor():
    
    check_admin()

    add_anchor = "anchor_with_commission"

    form = AnchorForm()
    del form.basic_salary
    del form.basic_salary_or_not
    del form.photo

    if form.validate_on_submit():
        anchor = Anchor(
            name=form.name.data,
            entry_time=form.entry_time.data,
            basic_salary_or_not=False,
            percentage=form.percentage.data
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

        return redirect(url_for('admin.list_anchors'))

    return render_template('admin/anchors/anchor.html', action="Add",
                           add_anchor=add_anchor, form=form,
                           title="Add Anchor with Commission")
"""

@admin.route('/anchors/add_anchor', methods=['GET', 'POST'])
@login_required
def add_anchor():
    """
    Add an anchor to the database
    """
    check_admin()

    add_anchor = True

    form = AnchorForm()
    del form.photo
    del form.entry_time
    #del form.live_session

    if form.validate_on_submit():
        anchor = Anchor(
            name=form.name.data,
            entry_time=datetime.datetime.today().strftime("%Y-%m-%d"),
            address=form.address.data,
            momo_number=form.momo_number.data,
            mobile_number=form.mobile_number.data,
            id_number=form.id_number.data,
            basic_salary_or_not=form.basic_salary_or_not.data,
            basic_salary=form.basic_salary.data,
            live_time=form.live_time.data,
            live_session=form.live_session.data,
            percentage=form.percentage.data,
            ace_anchor_or_not=form.ace_anchor_or_not.data,
            agent = form.agent.data
        )
        try:
            db.session.add(anchor)
            db.session.commit()

            directory = '/home/qi/projects/maomao_files/' + form.momo_number.data
            if not os.path.exists(directory):
                os.mkdir(directory)

            flash('You have successfully added a new anchor.')
        except Exception as e:
            #flash('Error: anchor name already exists.')
            flash(e)

        return redirect(url_for('admin.list_anchors'))

    return render_template('admin/anchors/anchor.html', action="Add",
                           add_anchor=add_anchor, form=form,
                           title="Add Anchor")

@admin.route('/anchors/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_anchor(id):
    """
    Edit an anchor
    """
    check_admin()

    add_anchor = False

    anchor = Anchor.query.get_or_404(id)
    form = AnchorForm(obj=anchor)
    if form.validate_on_submit():
        anchor.name = form.name.data
        anchor.entry_time = form.entry_time.data
        anchor.address = form.address.data
        anchor.momo_number = form.momo_number.data
        anchor.mobile_number = form.mobile_number.data
        anchor.id_number = form.id_number.data
        anchor.basic_salary_or_not = form.basic_salary_or_not.data
        anchor.basic_salary = form.basic_salary.data
        anchor.live_time=form.live_time.data
        anchor.live_session=form.live_session.data
        anchor.percentage=form.percentage.data
        anchor.ace_anchor_or_not=form.ace_anchor_or_not.data
        anchor.agent = form.agent.data

        # save image file
        if form.photo.data:
            f = form.photo.data
            filename = secure_filename(f.filename)
            UPLOAD_FOLDER = '/home/qi/projects/maomao_files'
            f.save(os.path.join(UPLOAD_FOLDER, form.name.data, filename))

        db.session.add(anchor)
        db.session.commit()
        flash('You have successfully edited the anchor.')

        # redirect to the anchors page
        return redirect(url_for('admin.list_anchors'))

    form.name.data = anchor.name
    form.entry_time.data = anchor.entry_time
    form.address.data = anchor.address
    form.momo_number.data = anchor.momo_number
    form.mobile_number.data = anchor.mobile_number
    form.id_number.data = anchor.id_number
    form.basic_salary_or_not.data = anchor.basic_salary_or_not
    form.basic_salary.data = anchor.basic_salary
    form.live_time.data = anchor.live_time
    form.live_session.data = anchor.live_session
    form.percentage.data = anchor.percentage
    form.ace_anchor_or_not.data = anchor.ace_anchor_or_not
    form.agent.data = anchor.agent
    
    return render_template('admin/anchors/anchor.html', add_anchor=add_anchor,
                           form=form, title="Edit Anchor")


@admin.route('/anchors/delete/<int:id>/<string:name>/<string:action>', methods=['GET', 'POST'])
@login_required
def delete_anchor(id, action, name):
    """
    Delete an anchor from the database
    """
    check_admin()

    if action == "request":
        return render_template('admin/confirmation.html', id=id, name=name)
    if action == "confirm":
        anchor = Anchor.query.get_or_404(id)
        db.session.delete(anchor)
        db.session.commit()
        flash('You have successfully deleted the anchor.')

    # redirect to the roles page
    return redirect(url_for('admin.list_anchors'))

@admin.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    Search the anchor information
    """
    check_admin()
    form = SearchForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        return redirect((url_for('admin.search_result', query=form.search.data)))
    return render_template('admin/search/search.html', form=form)


@admin.route('/results/<query>')
@login_required
def search_result(query):
    result = Anchor.query.filter_by(momo_number=query).first()
    if not result:
        flash('No results found.')
        return redirect(url_for('admin.search'))
    else:
        form = AnchorForm(obj=result)
        name = form.name.data
        del form.submit
        del form.photo
        return render_template('admin/search/result.html', query=query, form=form, name=name)

@admin.route('/system')
@login_required
def system_info():
    used_cpu_percent, used_disk_percent, free_disk_size = get_system_info()
    return render_template('admin/system.html', cpu=used_cpu_percent, disk=used_disk_percent, free=free_disk_size)

@admin.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    """
    upload monthly report to local host
    """
    check_admin()
    
    form = UploadForm()
    if form.validate_on_submit():
        f = form.upload_file.data
        filename = f.filename
        filename = filename.replace('-', '')
        UPLOAD_FOLDER = '/home/qi/projects/maomao_files'
        path_name = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(path_name):
            f.save(path_name)
            df = pd.read_excel(path_name, encoding = "utf-8")
            df = df.rename(columns=lambda x: re.sub(u'\(元\)', '', x))
            engine = create_engine('postgresql://stage_test:1234abcd@192.168.1.76:5432/stage_db')

            tablename = 'raw_data_' + datetime.datetime.today().strftime('%Y%m')
            df.to_sql(tablename, engine)

            connection = engine.connect()
            trans = connection.begin()
            try:
                query = """insert into payrolls (date, anchor_reward, coins, guild_division, anchor_momo) 
                            select  date_trunc('month', to_date(月份, 'YYYY-MM')), 播主奖励, 总陌币, 公会分成金额, 陌陌号 
                            from {}""".format(tablename)
                connection.execute(query)
                trans.commit()
                flash('You have successfully upload the file.')
            except Exception as e:
                trans.rollback()
                raise
            finally:
                connection.close()
        else:
            flash("The file already exists.")
            #return render_template('admin/upload.html', form=form)
    return render_template('admin/upload.html', form=form)

@admin.route('/search_payroll', methods=['GET', 'POST'])
@login_required
def search_payroll():
    """
    Search the payroll information of the anchor
    """
    check_admin()
    form = SearchPayrollForm(request.form)
    """
    for d in Payroll.query.with_entities(Payroll.date).distinct():
        print d[0]
        print type(d[0])
    """
    form.date.choices = [(int(d[0].strftime('%Y%m')), int(d[0].strftime('%Y%m'))) for d in Payroll.query.with_entities(Payroll.date).distinct()]
    if request.method == "POST" and form.validate_on_submit():
        #print type(form.date.data)
        return redirect((url_for('admin.search_payroll_result', query=form.search.data, date=form.date.data)))
    return render_template('admin/search/search.html', form=form)


@admin.route('/search_payroll/<query>/<date>', methods=['GET', 'POST'])
@login_required
def search_payroll_result(query, date):
    date = datetime.datetime.strptime(date, '%Y%m')
    payroll = Payroll.query.filter_by(anchor_momo=query).filter_by(date=date).first()
    if not payroll:
        flash('No results found.')
        return redirect(url_for('admin.search_payroll'))
    else:
        form = PayrollForm(obj=payroll)
        if form.validate_on_submit():
            payroll.comment = form.comment.data
            db.session.add(payroll)
            db.session.commit()

        form.date.data = payroll.date
        form.name.data = payroll.host.name
        form.momo_number.data = payroll.anchor_momo
        form.coins.data = payroll.coins
        form.guild_division.data = payroll.guild_division
        form.anchor_reward.data = payroll.anchor_reward
        form.profit.data = payroll.profit
        form.penalty.data = payroll.penalty
        form.basic_salary.data = payroll.host.basic_salary
        form.percentage.data = payroll.host.percentage
        form.ace_anchor_or_not.data = payroll.host.ace_anchor_or_not
        
    return render_template('admin/search/result.html', query=query, form=form)
