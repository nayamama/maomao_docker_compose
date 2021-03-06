# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, DateField, BooleanField, DecimalField, SelectField, TextAreaField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Employee


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('部门名称', validators=[DataRequired()])
    description = StringField('部门描述', validators=[DataRequired()])
    submit = SubmitField('提交')

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
        
class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('岗位名称', validators=[DataRequired()])
    description = StringField('岗位描述', validators=[DataRequired()])
    submit = SubmitField('提交')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    is_admin = BooleanField("是否管理员", default=False)
    submit = SubmitField('提交')

class AnchorForm(FlaskForm):
    """
    Form for detailed employee information
    """
    name = StringField('姓名', validators=[DataRequired()])
    entry_time = DateField('入职日期', format='%Y-%m-%d', validators=[validators.Optional()])
    address = StringField('住址', validators=[validators.Optional()])
    momo_number = StringField('陌陌号', validators=[DataRequired()])
    mobile_number = StringField('手机号', validators=[validators.Optional()])
    id_number = StringField('身份证号', validators=[validators.Optional(), Length(min=18, max=18, message='The length should be 18 digits.')])
    basic_salary_or_not = BooleanField('是否有保底工资', validators=[validators.Optional()])
    basic_salary = DecimalField('保底工资', validators=[validators.Optional()])
    live_time = DecimalField('直播时长', validators=[validators.Optional()])
    live_session = SelectField(
        '直播时段',
        choices=[('', '---'),('morning', '上午'), ('afternoon', '下午'), ('evening', '夜间'), ('night', '凌晨')]
    )
    percentage = DecimalField('提成', validators=[validators.Optional(), NumberRange(min=0, max=1, message="提成数字应在0-1之间。")])
    ace_anchor_or_not = BooleanField('是否王牌主播', validators=[validators.Optional()])
    agent = StringField('所属经纪人', validators=[validators.optional()])
    photo = FileField()
    submit = SubmitField('提交')


class PayrollForm(FlaskForm):
    """
    Form to get information of payrolls
    """
    date = DateField('日期', format='%Y-%m-%d')
    name = StringField('播主姓名', validators=[DataRequired()])
    momo_number = StringField('陌陌号', validators=[DataRequired()])
    coins = DecimalField('总陌币', validators=[validators.optional()])
    guild_division = DecimalField('公会分成', validators=[validators.optional()])
    anchor_reward = DecimalField('播主奖励', validators=[validators.optional()])
    profit = DecimalField('实际收入', validators=[validators.optional()])
    basic_salary = DecimalField('保底金额', validators=[validators.optional()])
    percentage = DecimalField('提成', validators=[validators.optional()])
    ace_anchor_or_not = BooleanField('是否王牌主播', validators=[validators.Optional()])


class UploadForm(FlaskForm):
    """
    Form to upload monthly report
    """
    upload_file = FileField()
    submit = SubmitField('上传')

class SearchForm(FlaskForm):
    """
    Form for searching anchor information
    """
    search = StringField('请输入主播陌陌号')
    submit1 = SubmitField('提交')


class SearchPayrollForm(FlaskForm):
    """
    Form for searching payroll information from momo_number and specific month
    """
    search = StringField('请输入主播陌陌号')
    date = SelectField(
        '月份',
        coerce=int,
    )
    submit2 = SubmitField('提交')


class SearchPayrollByMonthForm(FlaskForm):
    """
    Form for searching payroll information from momo_number and specific month
    """
    date = SelectField(
        '月份',
        coerce=int,
    )
    submit3 = SubmitField('提交')


class SearchPayrollByAnchorForm(FlaskForm):
    """
    Form for searching payroll information from momo_number and specific month
    """
    anchor = StringField('请输入主播陌陌号')
    submit4 = SubmitField('提交')


class PenaltyForm(FlaskForm):
    """
    Form to input penalty amount
    """
    momo_number = StringField(u'陌陌号', validators=[DataRequired()])
    amount = DecimalField(u'数额', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class CommentForm(FlaskForm):
    """
    Form to input for comment for a specific anchor
    """
    momo_number = StringField(u'陌陌号', validators=[DataRequired()])
    comment = StringField(u'备注', validators=[DataRequired()])
    submit = SubmitField(u'提交')


