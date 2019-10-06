from app import create_app
import os

config_name = os.getenv('FLASK_CONFIG', 'default')
application = create_app(config_name)

if __name__ == "__main__":
    # uwsgi expect a variable called "application" 
    application.run()
