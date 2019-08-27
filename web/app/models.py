from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#from flask_appbuilder import Model
#from flask_appbuilder.models.mixins import ImageColumn

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Anchor(db.Model):
    """
    Create an Anchor table
    """

    __tablename__ = 'anchors'

    id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(60), index=True, unique=True)
    name = db.Column(db.String(60), index=True, nullable=False)
    entry_time = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String(120))
    momo_number = db.Column(db.String(60), index=True, nullable=True, unique=True)
    mobile_number = db.Column(db.String(60), nullable=True)
    id_number = db.Column(db.String(60), nullable=True)
    basic_salary_or_not = db.Column(db.Boolean)
    basic_salary = db.Column(db.Float, nullable=True)
    live_time = db.Column(db.Float, nullable=True)
    live_session = db.Column(db.String(60), nullable=True)
    percentage = db.Column(db.Float, default=0.0, nullable=True)
    #total_paid = db.Column(db.Float, default=0.0)
    #owned_salary = db.Column(db.Float, default=0.0)
    ace_anchor_or_not = db.Column(db.Boolean)
    agent = db.Column(db.String(60), nullable=True)
    #payroll_id = db.Column(db.Integer, db.ForeignKey('payrolls.id'))
    payrolls = db.relationship('Payroll', backref='host', lazy='dynamic')

    def __repr__(self):
        return '<Anchor: {}>'.format(self.name)

class Payroll(db.Model):
    """
    Create a payroll table
    """
    __tablename__ = "payrolls"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    #name = db.Column(db.String(60), index=True, nullable=False)
    #momo_number = db.Column(db.String(60), nullable=True)
    coins = db.Column(db.Float, default=0.0, nullable=True)
    guild_division = db.Column(db.Float, default=0.0, nullable=True)
    anchor_reward = db.Column(db.Float, default=0.0, nullable=True)
    profit = db.Column(db.Float, default=0.0, nullable=True)
    penalty = db.Column(db.Float, default=0.0, nullable=True)
    #basic_salary = db.Column(db.Float, nullable=True)
    #percentage = db.Column(db.Float, default=0.0, nullable=True)
    #ace_anchor_or_not = db.Column(db.Boolean)
    salary = db.Column(db.Float, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    #employees = db.relationship('Anchor', backref='payroll', lazy='dynamic')
    anchor_momo = db.Column(db.String(60), db.ForeignKey('anchors.momo_number'))

    def __repr__(self):
        return '<Payroll: {}: {}>'.format(self.anchor_id, self.date)

