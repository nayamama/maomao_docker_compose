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
    #first_name = StringField('First Name', validators=[DataRequired()])
    #last_name = StringField('Last Name', validators=[DataRequired()])
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
