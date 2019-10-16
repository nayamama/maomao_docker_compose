# -*- coding: UTF-8 -*-
import os
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import datetime
import string
import pandas as pd
from sqlalchemy import create_engine, exc, desc
import psycopg2
import re
from bokeh.embed import components

from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm, AnchorForm, \
    SearchForm, UploadForm, SearchPayrollForm, SearchPayrollByAnchorForm, \
    SearchPayrollByMonthForm, PayrollForm, CommentForm, RegistrationForm
from .. import db
from ..models import Department, Role, Employee, Anchor, Payroll, Comment
from .helper import get_system_info, create_line_chart, add_log

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

@admin.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    check_admin()

    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)

        # add employee to the database
        try:
            db.session.add(employee)
            db.session.commit()
            flash('该员工成功登记', 'success')

            add_log(current_user.username, "Add", 
                    target_id=employee.id, target_table="employees")
        except exc.SQLAlchemyError as e:
            #flash('该邮箱已被使用， 请更换邮箱或用原邮箱索回密码。', 'error')
            error = str(e.__dict__['orig'])
            flash(error, 'error')
            db.session.rollback()
            add_log(current_user.username, "Add", target_table="employees", 
                    status="F")

        # redirect to the login page
        return redirect(url_for('admin.list_employees'))

    # load registration template
    return render_template('admin/register.html', form=form, title='Register')

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

            add_log(current_user.username, "Add", target_id=department.id, 
                    target_table="departments")
        except:
            # in case department name already exists
            flash('Error: department name already exists.', 'error')
            db.session.rollback()
            add_log(current_user.username, "Add", target_table="departments", 
                    status="F")

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

        add_log(current_user.username, "Update", target_id=id, 
                target_table="departments")

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
    d_name = department.name
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    add_log(current_user.username, "Delete", target_id=d_name, target_table="departments")
    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))


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

            add_log(current_user.username, "Add", target_id=role.id, 
                    target_table="roles")
        except:
            # in case role name already exists
            flash('Error: role name already exists.', 'error')
            db.session.rollback()
            add_log(current_user.username, "Add",
                    target_table="departments", status="F")

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

        add_log(current_user.username, "Update", target_id=id, 
                    target_table="roles")

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
    r_name = role.name
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    add_log(current_user.username, "Delete", target_id=r_name, 
                    target_table="roles")

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))


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
        employee.is_admin = form.is_admin.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        add_log(current_user.username, "Update", target_id=id, 
                    target_table="employees")

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

    if form.validate_on_submit():
        anchor = Anchor(
            name=form.name.data,
            entry_time=datetime.datetime.today().strftime("%Y-%m-%d"),
            address=form.address.data,
            momo_number=form.momo_number.data.strip(),
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

            upload_folder = os.getenv('UPLOAD_FOLDER')
            directory = upload_folder + "/" + form.momo_number.data

            if not os.path.exists(directory):
                os.mkdir(directory)

            flash('你已成功加入一个主播记录。')

            add_log(current_user.username, 
                    "Add", target_id = anchor.id, target_table="anchors")

        except:
            flash('错误:主播陌陌号已在数据库中。', 'error')
            db.session.rollback()

            add_log(current_user.username, 
                    "Add", target_id = form.momo_number.data, target_table="anchors", status="F")

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

        # save binary file
        if form.photo.data:
            f = form.photo.data
            filename = secure_filename(f.filename)
            upload_folder = os.getenv('UPLOAD_FOLDER')
            f.save(os.path.join(upload_folder, form.momo_number.data, filename))

        db.session.add(anchor)
        db.session.commit()
        flash('你已成功修改一个主播记录。')

        add_log(current_user.username, 
                "Update", target_id=id, target_table="anchors")

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

        add_log(current_user.username, 
                "Delete", target_id=id, target_table="anchors")
        flash('You have successfully deleted the anchor.')

    # redirect to the roles page
    return redirect(url_for('admin.list_anchors'))


@admin.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    """
    upload monthly report to local host
    """
    check_admin()

    form = UploadForm()

    # retrieve all existing dates in payrolls table
    existing_dates = Payroll.query.with_entities(Payroll.date).distinct().all()
    dates_list = [d[0] for d in existing_dates]

    # retrieve all momo_numbers in anchors table
    momo_numbers = Anchor.query.with_entities(Anchor.momo_number).all()
    nm_list = [n[0] for n in momo_numbers]

    if form.validate_on_submit():
        f = form.upload_file.data
        filename = f.filename
        filename = filename.replace('-', '')

        upload_folder = os.getenv('UPLOAD_FOLDER')
        path_name = os.path.join(upload_folder, filename)
        if not os.path.exists(path_name):
            f.save(path_name)
            df = pd.read_excel(path_name, encoding = "utf-8")

            # date cleaning
            df = df.rename(columns=lambda x: re.sub(u'\(元\)', '', x))

            # python 2 cannot deal with 'str' and 'unicode' comparision in pandas, but python 3 can handle it
            df = df.drop(df[df["结算方式"] == "对私"].index)

            # check date
            date_object = datetime.datetime.strptime(df.iloc[0]['月份'], "%Y-%m")

            # check if all momo_number of raw data is available in anchor table
            df_numbers = list(df['陌陌号'])
            invalid_number = []
            for num in df_numbers:
                if str(num) not in nm_list:
                    invalid_number.append(str(num))

            if date_object in dates_list:
                msg = str(date_object.year) + '年' + str(date_object.month) + "月的工资表已在数据库, 请检查日期重新上传."
                os.remove(path_name)
                flash(msg, 'error')
            elif invalid_number:
                nums = ",	".join(invalid_number)
                os.remove(path_name)
                msg = nums + " 不存在主播数据库中, 请检查陌陌号是否正确或添加新的主播。"
                flash(msg, 'error')
            else:
                engine = db.engine

                tablename = 'raw_data_' + datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
                df.to_sql(tablename, engine)

                connection = engine.connect()
                trans = connection.begin()
                try:
                    query = """insert into payrolls (date, anchor_reward, coins, guild_division, anchor_momo, profit) 
                                select  date_trunc('month', to_date(月份, 'YYYY-MM')), 播主奖励, 总陌币, 公会分成金额, 陌陌号, 实际收入 
                                from {}""".format(tablename)
                    connection.execute(query)
                    trans.commit()

                    # update salary and penalty for newly added records
                    for payroll in Payroll.query.filter_by(date=date_object).all():
                        penalties = payroll.host.penalties
                        penalty_sum = 0
                        for p in penalties:
                            if p.date.year == date_object.year and p.date.month == date_object.month:
                                penalty_sum += p.amount

                        payroll.penalty = penalty_sum
                        if payroll.host.ace_anchor_or_not:
                            payroll.salary = round(payroll.coins * payroll.host.percentage * 0.1 - penalty_sum, 2)
                        else:
                            payroll.salary = round(payroll.coins * payroll.host.percentage * 0.1 * 0.94 - penalty_sum, 2)
                    db.session.commit()

                    add_log(current_user.username, "Upload", target_table=tablename)

                    flash('该文件已成功上传。')

                except exc.SQLAlchemyError as e:
                    trans.rollback()
                    db.session.rollback()
                    add_log(current_user.username, "Upload", target_table=tablename, status="F")
                    error = str(e.__dict__['orig'])
                    flash(error, 'error')

                finally:
                    os.remove(path_name)
                    connection.close()
        else:
            flash("该文件已存在。", 'error')
    return render_template('admin/upload.html', form=form,  title="Upload")


@admin.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    To provide all search function
    """
    check_admin()

    # form to search the anchor information
    anchor_form = SearchForm(request.form)
    if anchor_form.submit1.data and anchor_form.validate_on_submit():
        return redirect((url_for('admin.anchor_search_result', query=anchor_form.search.data.strip())))

    # form to search the anchor salary information on a specific month
    anchor_payroll_form = SearchPayrollForm(request.form)
    anchor_payroll_form.date.choices = [(int(d[0].strftime('%Y%m')), int(d[0].strftime('%Y%m'))) for d in Payroll.query.with_entities(Payroll.date).order_by(Payroll.date).distinct()]
    if anchor_payroll_form.submit2.data and anchor_payroll_form.validate_on_submit():
        return redirect((url_for('admin.search_payroll_result', 
                        query=anchor_payroll_form.search.data.strip(), date=anchor_payroll_form.date.data)))

    # form to search the monthly payroll table for all anchors
    monthly_payroll_form = SearchPayrollByMonthForm(request.form)
    monthly_payroll_form.date.choices = [(int(d[0].strftime('%Y%m')), int(d[0].strftime('%Y%m'))) for d in Payroll.query.with_entities(Payroll.date).order_by(Payroll.date).distinct()]
    if monthly_payroll_form.submit3.data and monthly_payroll_form.validate_on_submit():
        date = datetime.datetime.strptime(str(monthly_payroll_form.date.data), "%Y%m")
        return redirect((url_for('admin.list_payrolls_by_month',
                        date=date)))

    # form to search all payrolls for a specific anchor
    anchor_all_pay_form = SearchPayrollByAnchorForm(request.form)
    if anchor_all_pay_form.submit4.data and anchor_all_pay_form.validate_on_submit():
        return redirect((url_for('admin.search_by_anchor', query=anchor_all_pay_form.anchor.data.strip())))

    return render_template('admin/search/search.html', anchor_form=anchor_form, title="Search", 
                            anchor_payroll_form=anchor_payroll_form,
                            monthly_payroll_form=monthly_payroll_form,
                            anchor_all_pay_form=anchor_all_pay_form)


@admin.route('/anchor_results/<query>')
@login_required
def anchor_search_result(query):
    result = Anchor.query.filter_by(momo_number=query).first()
    if not result:
        flash('该陌陌号在主播表中没有记录')
        return redirect(url_for('admin.search'))
    else:
        form = AnchorForm(obj=result)
        name = form.name.data
        del form.submit
        del form.photo
        return render_template('admin/search/results/result.html', query=query, form=form, name=name)


@admin.route('/search_payroll/<query>/<date>', methods=['GET', 'POST'])
@login_required
def search_payroll_result(query, date):
    """
    calculate the salary of an anchor in a specific month
    """
    check_admin()

    date = datetime.datetime.strptime(date, '%Y%m')
    payroll = Payroll.query.filter_by(anchor_momo=query).filter_by(date=date).first()
    if not payroll:
        flash('没有相关检索结果, 请检查主播陌陌号和其工作月份是否相符。')
        return redirect(url_for('admin.search'))
    else:
        form = PayrollForm(obj=payroll)
        form.date.data = payroll.date
        form.name.data = payroll.host.name
        form.momo_number.data = payroll.anchor_momo
        form.coins.data = payroll.coins
        form.guild_division.data = payroll.guild_division
        form.anchor_reward.data = payroll.anchor_reward
        form.profit.data = payroll.profit
        form.basic_salary.data = payroll.host.basic_salary
        form.percentage.data = payroll.host.percentage
        form.ace_anchor_or_not.data = payroll.host.ace_anchor_or_not

        penalties = payroll.host.penalties
        ps = []
        for p in penalties:
            if p.date.year == date.year and p.date.month == date.month:
                ps.append((p.date, p.amount))

        comments = payroll.host.comments
        cms = []
        for c in comments:
            if c.date.year == date.year and c.date.month == date.month:
                cms.append((c.date, c.comment))

        salary = payroll.salary
    return render_template('admin/search/results/result.html', query=query, form=form, 
                            salary=salary, penalty_list=ps, comments=cms)


@admin.route('/payrolls/<date>')
@login_required
def list_payrolls_by_month(date):
    check_admin()
    """
    List all payrolls on a specific month
    """
    payrolls = Payroll.query.filter_by(date=date).order_by(desc(Payroll.date)).all()
    salary_total = round(sum([p.salary for p in payrolls]), 2)

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") 
    year = date_obj.year
    month = date_obj.month
    return render_template('admin/search/results/payrolls.html',
                           payrolls=payrolls, year=year, month=month, 
                           salary_total=salary_total, title='Payrolls')


@admin.route('/search_by_anchor/<query>')
@login_required
def search_by_anchor(query):
    result = Payroll.query.filter_by(anchor_momo=query).order_by(desc(Payroll.date)).all()

    if not result:
        flash('该陌陌号在工资表中没有记录')
        return redirect(url_for('admin.search'))

    # plot a chart for the payroll history of an anchor
    name = Anchor.query.filter_by(momo_number=query).first().name
    engine = db.engine
    query = "select date, salary from payrolls where anchor_momo = {}::varchar(30) order by date;".format(query)
    df = pd.read_sql_query(query, engine)
    engine.dispose()

    title = name + "工资历史纪录"
    plot = create_line_chart(df, title)
    script, div = components(plot)
    
    return render_template('admin/search/results/all_payrolls_anchor.html', 
                            pays=result, name=name, 
                            the_div=div, the_script=script)


@admin.route('/comments')
@login_required
def list_comments():
    """
    List all anchors
    """
    check_admin()

    comments = Comment.query.order_by(Comment.date.desc()).all()
    return render_template('admin/comments/comments.html',
                           comments=comments, title='备注')


@admin.route('/add_comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    """
    Add a comment input
    """
    check_admin()

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            anchor_momo=form.momo_number.data.strip(),
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            comment=form.comment.data
        )
        try:
            db.session.add(comment)
            db.session.commit()

            flash(u'此备注记录已成功录入')

            add_log(current_user.username, 
                    "Add", target_id = comment.id, target_table="comments")
        except:
            flash(u'错误:此陌陌号不存在, 请验证输入的陌陌号重试', 'error')

            db.session.rollback()
            add_log(current_user.username, 
                    "Add", target_table="comments", status="F")

        return redirect(url_for('admin.list_comments'))

    return render_template('admin/comments/add_comment.html', form=form,
                            title="Add Comment")


@admin.route('/system')
@login_required
def system_info():
    used_cpu_percent, used_disk_percent, free_disk_size = get_system_info()
    return render_template('admin/system.html', cpu=used_cpu_percent, disk=used_disk_percent, free=free_disk_size)
