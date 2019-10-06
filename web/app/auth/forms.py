from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('确认密码')
    submit = SubmitField('登记')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被登记。')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('此用户名已被登记。')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class RequestResetForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('请求密码重置')

    def validate_email(self, email):
        employee = Employee.query.filter_by(email=email.data).first()
        if employee is None:
            raise ValidationError('无账户使用此邮箱，请检查邮箱或登录后重试')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('确认密码')
    submit = SubmitField('密码重置')