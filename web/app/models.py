from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    ace_anchor_or_not = db.Column(db.Boolean)
    agent = db.Column(db.String(60), nullable=True)
    payrolls = db.relationship('Payroll', backref='host', lazy='dynamic')
    penalties = db.relationship('Penalty', backref='host', lazy='dynamic')
    comments = db.relationship('Comment', backref='host', lazy='dynamic')

    def __repr__(self):
        return '<Anchor: {}>'.format(self.name)

class Payroll(db.Model):
    """
    Create a payroll table
    """
    __tablename__ = "payrolls"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    coins = db.Column(db.Float, default=0.0, nullable=True)
    guild_division = db.Column(db.Float, default=0.0, nullable=True)
    anchor_reward = db.Column(db.Float, default=0.0, nullable=True)
    profit = db.Column(db.Float, default=0.0, nullable=True)
    penalty = db.Column(db.Float, default=0.0, nullable=True)
    salary = db.Column(db.Float, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    anchor_momo = db.Column(db.String(60), db.ForeignKey('anchors.momo_number'))

    def __repr__(self):
        return '<Payroll: {}: {}>'.format(self.anchor_momo, self.date)

class Penalty(db.Model):
    """
    Create a penalty table
    """
    __tablename__ = "penalties"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    anchor_momo = db.Column(db.String(60), db.ForeignKey('anchors.momo_number'))
    amount = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return 'Penalty: {}: {} on {}'.format(self.anchor_momo, self.amount, self.date)

class Comment(db.Model):
    """
    Create a comment table 
    """
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    anchor_momo = db.Column(db.String(60), db.ForeignKey('anchors.momo_number'))
    comment = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return 'Comment: {} on {}'.format(self.comment, self.anchor_momo)


class Log(db.Model):
    """
    Create an action table to record logged-in user's action against app.
    """
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.String(20), nullable=False)
    target_table = db.Column(db.String(120), nullable=True)
    target_id = db.Column(db.String(20), nullable=True)
    user = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(5), nullable=True)

    def __repr__(self):
        return 'Log: {} {} {} of {}'.format(self.user, self.action, self.target_id, self.target_table)

