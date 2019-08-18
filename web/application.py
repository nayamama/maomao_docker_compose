import os
from app import create_app, db
from app.models import Employee
from flask_script import Manager


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
manager = Manager(app)

@manager.command
def add_admin_user():
    admin = Employee(email="admin@admin.com",
                     username="admin",
                     password="password",
                     is_admin=True)
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    manager.run()
