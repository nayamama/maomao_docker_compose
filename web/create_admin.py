from app.models import Employee
from app import create_app, db
import os

config_name = os.getenv('FLASK_CONFIG')

def create_admin():
    app = create_app(config_name)
    with app.app_context():
        admin = Employee(email="admin@admin.com",username="admin",password="admin2016",is_admin=True)
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    create_admin()

