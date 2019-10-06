from flask import flash, redirect, render_template, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message

from . import auth
from .forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from .. import db, mail
from ..models import Employee
from ..admin.helper import add_log


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('你已成功登记，现在你可以登录。')

        add_log(employee.username, "Add", 
                target_id=employee.id, target_table="employees")

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    name =  current_user.username
    logout_user()

    add_log(name, "Logout")

    flash('你已成功退出')

    # redirect to the login page
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # log action to db
            add_log(employee.username, "Login")

            # redirect to the appropriate dashboard page
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            add_log(form.email.data, "Login", status="F")
            flash('邮箱或密码错误。')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

def send_reset_email(employee):
    token = employee.get_reset_token()
    msg = Message('密码重置请求', 
                sender='noreply@mail.xuanpin.ltd',
                recipients=[employee.email])
    msg.body = f'''请访问以下链接去重置密码：
{url_for('auth.reset_password', token=token, _external=True)}

如果不是您发出的请求，请忽略此邮件。
'''
    mail.send(msg)

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        send_reset_email(employee)
        flash('密码重置邮件已发送，请检查邮箱。', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title="Reset Request", form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    employee = Employee.verify_reset_token(token)
    if employee is None:
        flash('这是一个无效或过期的令牌', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        employee.password = password
        db.session.commit()
        flash('你已成功重置密码，现在你可以登录。', 'success')

        add_log(employee.username, "Update password", 
                target_id=employee.id, target_table="employees")

        # redirect to the login page
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title="Reset Password", form=form)
